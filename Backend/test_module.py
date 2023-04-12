import json
from normalizer_pipeline import run as p1_run
from illegal_word_finder import run as p2_run
from tools import check_overlap


class TestRunner:
    def __init__(self, illegal_words):
        self.illegal_words = illegal_words

    def test_one_sentence(self, sentence):
        out1 = p1_run(sentence, self.illegal_words)
        out2 = p2_run(sentence, self.illegal_words)
        sum_out = out1.copy()
        for item in out2:
            for span in out2[item]:
                if span not in sum_out[item]:
                    sum_out[item].append(span)
        return sum_out

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
        ]

        for test in tests:
            print('\n**', test, '**')
            out = run(test, illegals_test)
            for item in out:
                print(repr(item), ':', out[item])


if __name__ == "__main__":
    test_runner = TestRunner([
        'تفنگ',
        'سیر',
        'سیرجان',
        'بی ادب',
        'بی‌تربیت',
        'چنگال',
        'سرما',
        'ترشی',
        'ممد'
    ])
    print(test_runner.test_one_sentence('من ت#فنگ دوست دارم.'))
