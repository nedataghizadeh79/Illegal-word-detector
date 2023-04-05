from typing import List
import hazm
from strsimpy.weighted_levenshtein import WeightedLevenshtein
import regex
import re
import yaml

ILLEGAL_EDIT_DISTANCE_THRESHOLD = 3
NON_PERSIAN_CHARS_REGEX = r'[^\u0621-\u064A|\u0686|\u0698|\u06A9|\u06af|\u06be|\u06c1|\u06c3]'


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


def get_illegal_regex_from_words(illegal_words_list: list[str]) -> list[str]:
    word_regex_list = []
    non_persian_characters_regex = '[^\u0600-\u06FF]*'
    for illegal in illegal_words_list:
        word_regex = non_persian_characters_regex + \
                     '.*'.join(illegal) + non_persian_characters_regex
        word_regex_list.append(word_regex)
    return word_regex_list


def detect_bad_formed_words(word_list: list, illegal_words: list) -> list:  # [(str, str, (int, int))]:
    dubiouses = []  # format --> [(illegal, found, (start, end))]
    illegal_regexes = get_illegal_regex_from_words(illegal_words)

    # Combine regexes
    regex_combination = "(" + ")|(".join(illegal_regexes) + ")"

    for word in word_list:
        bad_word_match = re.search(regex_combination, word[0])
        if bad_word_match:
            captured_groups = bad_word_match.groups()
            for i, group in enumerate(captured_groups):
                if group is not None:
                    dubiouses.append((illegal_words[i], word[0], (word[1][0], word[1][1])))
    return dubiouses


def edit_distance(s1, s2):
    def insertion_cost(char):
        if not re.match(NON_PERSIAN_CHARS_REGEX, char):
            return 2.0
        return 0.1

    def deletion_cost(char):
        if not re.match(NON_PERSIAN_CHARS_REGEX, char):
            return 2.0
        return 0.1

    def substitution_cost(char_a, char_b):
        cost = 0.1
        if re.match(NON_PERSIAN_CHARS_REGEX, char_a):
            cost += 2.0
        if re.match(NON_PERSIAN_CHARS_REGEX, char_b):
            cost += 2.0
        return cost

    weighted_levenshtein = WeightedLevenshtein(
        substitution_cost_fn=substitution_cost,
        insertion_cost_fn=insertion_cost,
        deletion_cost_fn=deletion_cost)

    return weighted_levenshtein.distance(s1, s2)


def is_false_positive(token: str, illegal_word: str, persian_words: set) -> bool:
    # check if word exists in the persian dictionary
    if token not in persian_words and \
            edit_distance(token, illegal_word) < ILLEGAL_EDIT_DISTANCE_THRESHOLD:
        print("True positive: ", token)
        return False  # not false positive

    return True


def clean_false_positives(dubiouses: List[str], persian_dictionary: set):
    return [dubious for dubious in dubiouses if is_false_positive(dubious[1], dubious[0], persian_dictionary)]


def dubiouses_to_output(dubiouses):
    output = {}  # format --> {'illegal':[(start, end)]}
    for dubious in dubiouses:
        # todo --> make set
        output.setdefault(dubious[0], []).append(dubious[2])
    return output


def make_integrated_string(input_string):
    integrated_string = ''
    integrated_spans = []
    counter = 0
    for char in input_string:
        if re.match(r'[\u0621-\u064A|\u0686|\u0698|\u06A9|\u06af|\u06be|\u06c1|\u06c3|\u06CC]', char):
            integrated_string += char
            integrated_spans.append(counter)
            counter += 1
        else:
            counter += 1
    return integrated_string, integrated_spans


def detect_bad_formed_integrated(integrated_string: str, integrated_spans, illegal_words: list[str]) -> list[
    (str, str, (int, int))]:
    dubiouses = []  # format --> [(illegal, found, (start, end))]
    illegal_regexes = get_illegal_regex_from_words(illegal_words)

    # Combine regexes
    regex_combination = "(" + ")|(".join(illegal_regexes) + ")"

    bad_word_match = re.search(regex_combination, integrated_string)
    if bad_word_match:
        captured_groups = bad_word_match.groups()
        for i, group in enumerate(captured_groups):
            if group:
                span = bad_word_match.span(i + 1)
                dubiouses.append((illegal_words[i], '', (integrated_spans[span[0]], integrated_spans[span[1]])))
    return dubiouses


def get_illegal_regex_for_integrated(illegal_words_list: list[str]) -> list[str]:
    word_regex_list = []
    for illegal in illegal_words_list:
        word_regex = '+'.join(illegal) + '+'
        word_regex_list.append(word_regex)
    return word_regex_list


# def clean_fp_integrated(dubiouses):
#     return [dubious for dubious in dubiouses if is_false_positive(dubious[1], dubious[0])]


def run(text: str, illegal_words: List[str]):
    persian_dictionary = get_persian_words_dictionary()
    word_list = tokenize(text)
    normal_word_list = hazm_normalize(word_list)
    dubiouses = detect_bad_formed_words(normal_word_list, illegal_words)
    dubiouses = clean_false_positives(dubiouses, persian_dictionary)
    integrated_string, integrated_spans = make_integrated_string(text)
    integrated_dubiouses = detect_bad_formed_integrated(integrated_string, integrated_spans, illegal_words)
    # TODO cleanup false positive for integrated!
    output = dubiouses_to_output(dubiouses + integrated_dubiouses)
    return output


def run_tests():
    tests = [
        'من تر۲۲۲شی دوست دارم.'
        # [3,9]
        , 'من ترش23432ی دوست دارم'
        # [3,11]
        , 'من ت٫ریال^٪ریال&آٖۤآلبدذ رشی دوست دارم'
        # ok
        , 'من ت#$@رشی          دوست دارم'
        # [3,19]
        , 'من       ت                      ر                ش                      ی           دوست دارم'
        # [3,83]
        , 'من تررررررررررررررررررشششششی دوست دارم'
        # [3,27]
        , 'من ترش و شیرین دوست دارم'
        # ok
        , 'من ترشک دوست دارم'
        # ok
        , 'مراقب باش که سرمانخوری'
        # ok
        , 'سرمان به باد رفت'
        # ok
          'سر‌‌‌‌ما بد است!'  # multiple nim faseles!!
        # [0, 9]
        , 'سررررررررررمامان داد نزن'
        # ok
        , 'سرمامانداد نزن'
        # ok
        , 'من در سررم٫ااا میخواهم که تررر٪ش۰ی سییییـــــــر بخورم '
        # [  [35,48] , [26,34] , [6,14] ]
        , 'من#ترشی٫دوست@دارم'
        , 'میخواهم برم به س‌ی‌ر‌ج‌ا‌ن.'
        # [15,20]
        , 'بیا بریم یه سSSیSerرجاfن'
        # [12,22]
        , 'من تف‌نگ میخوام.'
        # [3,6]
        , 'من تفنگ دوست دارم'
        # [3,7]
        , 'من منتلیمخنخر خحهنخشهتهتاییلا دوست دارم'
        # ok
        , 'من منتلیمخنخرخحهنخشهتهتاییلا دوست دارم'
        # [4,29]
    ]

    illegals_test = [
        'تفنگ',
        'سیر',
        'سیرجان',
        'بی ادب',
        'بی‌تربیت',
        'چنگال',
        'سرما',
        'ترشی',
        'ممد'
    ]

    for test in tests:
        print('\n**', test, '**')
        out = run(test, illegals_test)
        for item in out:
            print(repr(item), ':', out[item])


if __name__ == '__main__':
    # run_tests()
    # print(get_persian_similar_characters())
    print(edit_distance("آقا", "آبا"))
    # print(re.match(ACCEPTABLE_PERSIAN_CHARS_REGEX, "!"))
    # print(ACCEPTABLE_PERSIAN_CHARS_REGEX)
