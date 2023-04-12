"""
Common tools that all pipelines will share.
"""
import re
from typing import List

import hazm
import regex
import yaml
from strsimpy import WeightedLevenshtein

NON_PERSIAN_CHARS_REGEX = r'[^\u0621-\u064A|\u0686|\u0698|\u06A9|\u06af|\u06be|\u06c1|\u06c3]'
VALID_PERSIAN_CHARS_REGEX = r'[\u0600-\u06FF\uFB50-\uFDFF\s]'
INVALID_PERSIAN_CHARS_REGEX = r'[^\u0600-\u06FF\uFB50-\uFDFF\s]'
VALID_PERSIAN_CHARACTERS_REGEX = '[\u0621-\u064A|\u0686|\u0698|\u06A9|\u06af|\u06be|\u06c1|\u06c3|\u06CC]'
RECURRENT_PATTERN_REGEX = rf'({VALID_PERSIAN_CHARS_REGEX})\1+'

_normalizer = hazm.Normalizer()
_lemmatizer = hazm.Lemmatizer()


def _get_persian_words_dictionary():
    base_address = "assets/dictionaries"
    persian_words = set()

    with open(f'{base_address}/distinct_words.txt', encoding='utf-8') as f:  # 453158
        persian_words.update([x.strip() for x in f.readlines()])
    with open(f'{base_address}/word_collection_1.txt', encoding='utf-8') as f:  # 331792
        persian_words.update([x.strip() for x in f.readlines()])
    with open(f'{base_address}/words_with_bad_english.txt', encoding='utf-8') as f:  # 103923
        persian_words.update([x.split('/')[0].strip() for x in f.readlines()[1:]])
    with open(f'{base_address}/persian_verbs_list.txt', encoding='utf-8') as f:  # 32325
        persian_words.update([x.strip() for x in f.readlines()])
    with open(f'{base_address}/moin_key_words.txt', encoding='utf-8') as f:  # 25527
        persian_words.update([x.strip() for x in f.readlines()])
    with open(f'{base_address}/farhang_motaradef_motazad.txt', encoding='utf-8') as f:  # 19897
        persian_words.update([x.split(":")[0].strip() for x in f.readlines()[1:]])

    return persian_words


persian_words_dictionary = _get_persian_words_dictionary()


def get_persian_similar_characters():
    with open("assets/similar_persian_chars.yml", 'r', encoding='utf-8') as f:
        chars_lists = yaml.safe_load(f)
        return [set(cl) for cl in chars_lists]


def hazm_normalize(word_list):
    normal_word_list = []
    for word in word_list:
        normal_word_list.append((_normalizer.normalize(word[0]), word[1]))
    return normal_word_list


def hazm_lemmatize(word):
    return _lemmatizer.lemmatize(word)


def tokenize(normal_string):
    working_string1 = ' ' + normal_string + ' '
    tokenize_regex = r'[\s]([\S]+)[\s]'
    tokenize_match = regex.finditer(tokenize_regex, working_string1, overlapped=True)
    word_list = []
    for match_object in tokenize_match:
        word_list.append(
            (match_object.group(1), (match_object.start(1) - 1, match_object.end(1) - 1))
        )
    return word_list


def edit_distance(s1, s2):
    persian_similar_characters = get_persian_similar_characters()

    def insertion_cost(char):
        if not re.match(NON_PERSIAN_CHARS_REGEX, char):
            return 2.0
        return 0.1

    def deletion_cost(char):
        if not re.match(NON_PERSIAN_CHARS_REGEX, char):
            return 2.0
        return 0.1

    def substitution_cost(char_a, char_b):
        if re.match(NON_PERSIAN_CHARS_REGEX, char_a) or re.match(NON_PERSIAN_CHARS_REGEX, char_b):
            return 0.1
        subset = {char_a, char_b}
        for group in persian_similar_characters:
            if subset.issubset(group):
                return 1
        return 3

    weighted_levenshtein = WeightedLevenshtein(
        substitution_cost_fn=substitution_cost,
        insertion_cost_fn=insertion_cost,
        deletion_cost_fn=deletion_cost)

    return weighted_levenshtein.distance(s1, s2)


def check_overlap(span1, span2):
    if span2[0] >= span1[0] and span2[1] >= span1[1]:
        return (span1[0], span2[1])
    if span2[0] >= span1[0] and span2[1] <= span1[1]:
        return span1
    if span2[0] <= span1[0] and span2[1] >= span1[1]:
        return span2
    if span2[0] <= span1[0] and span2[1] <= span1[1]:
        return (span2[0], span1[1])
    return None


def custom_simplifier(token: str):
    pure_persian = re.sub(INVALID_PERSIAN_CHARS_REGEX, '', token)
    denumbered = re.sub(r'\d', '', pure_persian)
    lemmatized = hazm_lemmatize(denumbered).split("#")[0]
    return re.sub(RECURRENT_PATTERN_REGEX, r'\1', lemmatized)
