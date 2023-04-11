import hazm
import regex
import yaml

NON_PERSIAN_CHARS_REGEX = r'[^\u0621-\u064A|\u0686|\u0698|\u06A9|\u06af|\u06be|\u06c1|\u06c3]'
VALID_PERSIAN_CHARS_REGEX = r'[\u0600-\u06FF\s]'


def get_persian_words_dictionary():
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


def get_persian_similar_characters():
    with open("assets/similar_persian_chars.yml", 'r') as f:
        chars_lists = yaml.safe_load(f)
        indices = {}

        for i, group in enumerate(chars_lists):
            for city in group:
                indices.setdefault(city, set()).add(i)


def common_groups(city1, city2, indices: dict):
    return indices.get(city1, set()) & indices.get(city2, set())


def hazm_normalize(word_list):
    normalizer = hazm.Normalizer()
    normal_word_list = []
    for word in word_list:
        normal_word_list.append((normalizer.normalize(word[0]), word[1]))
    return normal_word_list


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
