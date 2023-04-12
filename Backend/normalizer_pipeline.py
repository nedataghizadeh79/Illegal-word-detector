from typing import List, Tuple, Set, Dict
import re

import tools
from tools import tokenize, hazm_normalize, RECURRENT_PATTERN_REGEX, INVALID_PERSIAN_CHARS_REGEX


def custom_simplifier(token: str):
    pure_persian = re.sub(INVALID_PERSIAN_CHARS_REGEX, '', token)
    denumbered = re.sub(r'\d', '', pure_persian)
    lemmatized = tools.hazm_lemmatize(denumbered).split("#")[0]
    return re.sub(RECURRENT_PATTERN_REGEX, r'\1', lemmatized)


def run_for_token(token: Tuple[str, Tuple], illegals: Set[str], simplified_illegals: Dict[str, str]):
    token = (token[0], token[1], custom_simplifier(token[0]))
    print(token)
    # print(token)
    if token[2] in simplified_illegals:
        if (token[0] in illegals) or (token[0] not in tools.persian_words_dictionary):
            return simplified_illegals[token[2]], token
    else:
        for illegal in illegals:
            if (illegal in token[2]) and (token[0] not in tools.persian_words_dictionary):
                return illegal, token

    return None, None


def run(text: str, illegals: List[str]):
    dubious = dict()
    tokens = hazm_normalize(tokenize(text))
    simplified_illegals = {custom_simplifier(illegal): illegal for illegal in illegals}
    illegals_set = set(illegals)

    # in case a single word is split into multiple tokens, we will reattach them together and scan for illegal words.
    for token_count in range(1, 6):
        if not tokens:
            break

        token_values, token_ranges = [list(i) for i in zip(*tokens)]
        for i in range(len(token_values) - token_count + 1):
            if i >= len(tokens):
                break

            if token_count == 1:
                # If the token is straight up an illegal word, just report it, delete it and continue
                if token_values[i] in illegals:
                    dubious[token_values[i]] = token_ranges[i]
                    del tokens[i]
                    del token_values[i]
                    del token_ranges[i]
                    continue
                else:
                    token = tokens[i]

            # Joined tokens
            else:
                for partial_token in token_values[i:i+token_count]:
                    if len(partial_token) < 2 or partial_token not in tools.persian_words_dictionary:
                        # meaningless word! suspicious!
                        token = (
                            ''.join(token_values[i:i + token_count]),
                            (token_ranges[i][0], token_ranges[i + token_count - 1][1])
                        )
                        break
                else:
                    # all tokens inside the gap were actual words and were not meaningless!
                    # so we don't have to check further
                    continue

            illegal_word, illegal_token = run_for_token(token, illegals_set, simplified_illegals)
            if illegal_word:
                dubious[illegal_word] = illegal_token[1]
                for t in tokens[i: i + token_count]:
                    tokens.remove(t)

        # dubious.update(result)
        # delete the tokens that are already found
        # tokens = list(filter(lambda t: t[0] not in bad_tokens, tokens))
        # if not tokens:
        #     break

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

    # tests = [
    #     'من#ترشی٫دوست@دارمگپچجژ',
    # ]

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
