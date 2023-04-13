import re
from typing import List, Dict, Tuple
import tools

EDIT_DISTANCE_THRESHOLD = 4


def process_illegals(illegal_words: List[str]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    This function turns each illegal word into a regex that can be used to find it in a text.
    Args:
        illegal_words: list of all the illegal words

    Returns:

    """
    regexes = {}
    shuffled_regexes = {}
    similar_chars = tools.persian_char_groups
    optional_chars = set(tools.persian_optional_chars)

    char_groups = {}
    for char_list in similar_chars:
        for char in char_list:
            char_groups.setdefault(char, set()).update(char_list)
    for illegal in illegal_words:
        regex = r'.*'
        for char in illegal:
            if char in char_groups:
                regex += rf'[' \
                         rf'{"".join([c for c in char_groups[char]])}' \
                         rf']{"*" if char in optional_chars else "+"}' \
                         rf'.*\s*{tools.NIM_FASELE_REGEX}*'
            elif char in optional_chars:
                regex += rf'{char}*.*\s*{tools.NIM_FASELE_REGEX}*'
            else:
                regex += rf'{char}+.*\s*{tools.NIM_FASELE_REGEX}*'
        regexes[illegal] = regex

        second_regex = rf'.*[{illegal}]{{{len(illegal)}}}.*'
        shuffled_regexes[illegal] = second_regex

    return regexes, shuffled_regexes


def is_false_positive(illegal_word: str, token: str, is_shuffled: bool = False) -> bool:
    """
    This function checks if a token has been recognized as an illegal word by mistake or not.
    It does so by checking if the token is a correct persian word or not.
    If it is, and it's lemma isn't the same as the illegal word's lemma, then it is a false positive.
    otherwise, We'll check the edit distance between the token and the illegal word and compare it to our EDIT
    DISTANCE THRESHOLD which can be adjusted to be as precise as we want it.
    Args:
        illegal_word: illegal_word: The illegal word that has been recognized
        token: token: The token that has been recognized as the illegal word

    Returns: True if the token is a false positive, False otherwise

    """
    if tools.hazm_lemmatize(token) == tools.hazm_lemmatize(illegal_word):
        return False
    if token in tools.persian_words_dictionary:
        return True
    simple_illegal_word = tools.custom_simplifier(illegal_word)
    simple_token = tools.custom_simplifier(token)
    edit_distance = tools.edit_distance(simple_token, simple_illegal_word)
    return edit_distance > (len(illegal_word) * 2 if is_shuffled else EDIT_DISTANCE_THRESHOLD)


def run(text: str, illegal_words: List[str]):
    # Tokenize the text
    word_list = tools.tokenize(text)

    # Normalize each token. Normalization must take place after tokenization to keep track of the original spans
    normal_word_list = tools.hazm_normalize(word_list)

    # Turn each illegal word into a regex
    illegal_regexes, illegal_shuffled_regexes = process_illegals(illegal_words)

    # Final output
    dubious = {}

    regex_combination = "(" + ")|(".join(illegal_regexes.values()) + ")"
    shuffled_regex_combination = "(" + ")|(".join(illegal_shuffled_regexes.values()) + ")"

    for token_count in range(1, 6):

        token_values, token_ranges = [list(i) for i in zip(*normal_word_list)]
        for i in range(len(token_values) - token_count + 1):
            word = ''.join(token_values[i:i + token_count])
            span = token_ranges[i][0], token_ranges[i + token_count - 1][1]

            captured_groups = None
            is_shuffled = False

            bad_word_match = re.search(regex_combination, word)
            if bad_word_match:
                captured_groups = bad_word_match.groups()
            else:
                bad_word_match = re.search(shuffled_regex_combination, word)
                if bad_word_match:  # if the word is shuffled
                    captured_groups = bad_word_match.groups()
                    is_shuffled = True

            if captured_groups:
                for index, group in enumerate(captured_groups):
                    if group and not is_false_positive(illegal_words[index], word, is_shuffled):
                        # check if the span is already captured
                        if illegal_words[index] in dubious:
                            for captured_span in [x[1] for x in dubious[illegal_words[index]]]:
                                if captured_span[0] <= span[0] <= captured_span[1] or \
                                        captured_span[0] <= span[1] <= captured_span[1]:
                                    # if the span is already captured, then we don't need to add it again
                                    break
                            else:
                                dubious.setdefault(illegal_words[index], []).append((word, span))
                        else:
                            dubious.setdefault(illegal_words[index], []).append((word, span))

    return dubious
