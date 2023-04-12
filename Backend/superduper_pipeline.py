import re
from typing import List, Tuple, Set, Dict

import tools


def process_illegals(illegal_words: List[str]):
    regexes = {}
    similar_chars = tools.get_persian_similar_characters()

    char_groups = {}
    for char_list in similar_chars:
        for char in char_list:
            char_groups.setdefault(char, []).append(char_list)
    # char_groups = {char: char_list for char_list in similar_chars for char in char_list}
    print(char_groups)
    for illegal in illegal_words:
        regex = r'.*'
        for char in illegal:
            if char in char_groups:
                regex += rf'[{"".join(char_groups[char])}]+.*'
            else:
                regex += rf'{char}+.*\s*'
                # regexes[illegal]
        regexes[illegal] = regex

    return regexes


def run(text: str, illegal_words: List[str]):
    persian_dictionary = tools.persian_words_dictionary

    word_list = tools.tokenize(text)
    normal_word_list = tools.hazm_normalize(word_list)

    illegal_regexes = process_illegals(illegal_words)
    fucks = {}

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
                for i, group in enumerate(captured_groups):
                    if group:
                        fucks.setdefault(illegal_words[i], []).append((word, span))

    return fucks


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
        , 'سر‌‌‌‌ما بد است!'  # multiple nim faseles!!
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
        , 'من تگنف دارم'
        # [3,7]
        , 'تفنگی دارم خوشگله ترش یکمی هست بهبه'
        # [0,5]
        , 'غستننتنیه شهر خیلی بدیه'
        , 'قیر غابل غبول است هرفت!'
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
        'ممد',
        'غیرقابلقبول',
        'قسطنتنیه',
    ]

    # tests = [
    #     'من#ترشی٫دوست@دارمگپچجژ',
    # ]

    # illegals_test = [
    #     'ترشی',
    # ]

    for test in tests:
        print('\n**', test, '**')
        out = run(test, illegals_test)
        for item in out:
            print(repr(item), ':', out[item])


if __name__ == '__main__':
    run_tests()
    # print(run('من ترشی دوست دارم', ['ترشی', 'سیر', 'سیرجان', 'بی ادب', 'بی‌تربیت', 'چنگال', 'سرما', 'ترشی', 'ممد']))
