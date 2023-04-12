import re
from typing import List
import tools

EDIT_DISTANCE_THRESHOLD = 4


def process_illegals(illegal_words: List[str]):
    regexes = {}
    similar_chars = tools.get_persian_similar_characters()

    char_groups = {}
    for char_list in similar_chars:
        for char in char_list:
            char_groups.setdefault(char, set()).update(char_list)
    for illegal in illegal_words:
        regex = r'.*'
        for char in illegal:
            if char in char_groups:
                regex += rf'[{"".join([c for c in char_groups[char]])}]+.*\s*{tools.NIM_FASELE_REGEX}*'
            else:
                regex += rf'{char}+.*\s*{tools.NIM_FASELE_REGEX}*'
        regexes[illegal] = regex

    return regexes


def is_false_positive(illegal_word: str, token: str) -> bool:
    # print(illegal_word, '  VS   ', token, end=' ')
    if token == illegal_word:
        return False
    if token in tools.persian_words_dictionary:
        return True
    simple_illegal_word = tools.custom_simplifier(illegal_word)
    simple_token = tools.custom_simplifier(token)
    edit_distance = tools.edit_distance(simple_token, simple_illegal_word)
    # print(' -> ', edit_distance)
    return edit_distance > EDIT_DISTANCE_THRESHOLD


def run(text: str, illegal_words: List[str]):
    word_list = tools.tokenize(text)
    normal_word_list = tools.hazm_normalize(word_list)

    illegal_regexes = process_illegals(illegal_words)
    dubious = {}

    regex_combination = "(" + ")|(".join(illegal_regexes.values()) + ")"

    for token_count in range(1, 6):

        token_values, token_ranges = [list(i) for i in zip(*normal_word_list)]
        for i in range(len(token_values) - token_count + 1):
            word = ''.join(token_values[i:i + token_count])
            span = token_ranges[i][0], token_ranges[i + token_count - 1][1]

            # for word, span in normal_word_list:
            # for illegal, regex in illegal_regexes.items():
            #     if re.search(regex, word):
            #         print(word, illegal, span)
            bad_word_match = re.search(regex_combination, word)
            if bad_word_match:
                captured_groups = bad_word_match.groups()
                for index, group in enumerate(captured_groups):
                    if group and not is_false_positive(illegal_words[index], word):
                        dubious.setdefault(illegal_words[index], []).append((word, span))

    # Handle overlapping spans -> choose the smallest one
    for word, spans in dubious.items():
        spans.sort(key=lambda x: x[1][1] - x[1][0])
        new_spans = []
        for span in spans:
            if not new_spans:
                new_spans.append(span)
            else:
                if new_spans[-1][1][1] >= span[1][0]:
                    new_spans[-1] = (new_spans[-1][0], (new_spans[-1][1][0], span[1][1]))
                else:
                    new_spans.append(span)
        dubious[word] = new_spans

    return dubious
