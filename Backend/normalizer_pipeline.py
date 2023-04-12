from typing import List
import re

import tools
from tools import tokenize, hazm_normalize, RECURRENT_PATTERN_REGEX, NON_PERSIAN_CHARS_REGEX


def custom_simplifier(token: str):
    pure_persian = re.sub(NON_PERSIAN_CHARS_REGEX, '', token)
    return re.sub(RECURRENT_PATTERN_REGEX, r'\1', pure_persian)


def run_for_tokens(tokens, illegals: List[str]):
    tokens = list(
        map(
            lambda tkn: (tkn[0], tkn[1], custom_simplifier(tkn[0])),
            tokens
        )
    )

    dubious = dict()
    illegals_set = set(illegals)
    simplified_illegals = {custom_simplifier(illegal): illegal for illegal in illegals}

    for token in tokens:
        if token[2] in simplified_illegals:
            # print(token[0])
            if (token[0] in illegals_set) or (token[0] not in tools.persian_words_dictionary):
                dubious.setdefault(simplified_illegals[token[2]], []).append(token[1])

    return dubious


def run(text: str, illegals: List[str]):
    dubious = dict()
    tokens = hazm_normalize(tokenize(text))
    token_values = list(map(lambda tkn: tkn[0], tokens))
    token_ranges = list(map(lambda tkn: tkn[1], tokens))

    for token_count in range(1, 4):
        joined_tokens = [(''.join(token_values[i:i + token_count]),
                          (token_ranges[i][0], token_ranges[i + token_count - 1][1]))
                         for i in range(len(token_values) - token_count + 1)]
        dubious.update(run_for_tokens(joined_tokens, illegals))
    return dubious



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
    # t = "سلاااا!!!ام گ         ل سلام ابی مکرر چطوری  سلاام دادااااااا؟"
    # il = ["گل", "مکر", "دادا", "سلام"]
    # res = run(t, il)
    # for k in res:
    #     print(k, res[k])
    run_tests()