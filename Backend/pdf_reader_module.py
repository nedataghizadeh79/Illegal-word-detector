import textract
import codecs
import re


class Pdf2txt:

    def __init__(self):
        self.raw_txt = ''
        self.good_txt = ''

    def pdf2txt(self, pdf_path):
        textracted = textract.process(pdf_path)
        print(textracted, "\n\n\n\n")
        self.raw_txt = codecs.decode(textracted)
        print(self.raw_txt, "\n\n\n\n")
        self.good_txt = self.raw_txt
        self.correct_unicodes()
        return self.good_txt

    def replace_str(self, x, withx):
        for i in x:
            self.good_txt = re.sub(re.escape(i), withx, self.good_txt)

    def correct_unicodes(self):
        self.replace_str([u'\ufe81'], 'آ')
        self.replace_str([u'\u0623', u'\ufe8e', u'\ufe84'], 'ا')
        self.replace_str([u'\ufe91', u'\ufe92'], 'ب')
        self.replace_str([u'\ufe90'], 'ب‌')
        self.replace_str([u'\ufb58', u'\ufb59'], 'پ')
        self.replace_str([u'\ufb57'], 'پ‌')
        self.replace_str([u'\ufe97', u'\ufe98'], 'ت')
        self.replace_str([u'\ufe96', u'\ufe94'], 'ت‌')
        self.replace_str([u'\ufe9b', u'\ufe9c'], 'ث')
        self.replace_str([u'\ufe9a'], 'ث‌')
        self.replace_str([u'\ufe9f', u'\ufea0'], 'ج')
        self.replace_str([u'\ufe9e'], 'ج‌')
        self.replace_str([u'\ufb7c', u'\ufb7d'], 'چ')
        self.replace_str([u'\ufb7b'], 'چ‌')
        self.replace_str([u'\ufea3', u'\ufea4'], 'ح')
        self.replace_str([u'\ufea2'], 'ح‌')
        self.replace_str([u'\ufea7', u'\ufea8'], 'خ')
        self.replace_str([u'\ufea6'], 'خ‌')
        self.replace_str([u'\ufeaa'], 'د')
        self.replace_str([u'\ufeac'], 'ذ')
        self.replace_str([u'\ufeae'], 'ر')
        self.replace_str([u'\ufeb0'], 'ز')
        self.replace_str([u'\ufb8b'], 'ژ')
        self.replace_str([u'\ufeb3', u'\ufeb4'], 'س')
        self.replace_str([u'\ufeb2'], 'س‌')
        self.replace_str([u'\ufeb7', u'\ufeb8'], 'ش')
        self.replace_str([u'\ufeb6'], 'ش‌')
        self.replace_str([u'\ufebb', u'\ufebc'], 'ص')
        self.replace_str([u'\ufeba'], 'ص‌')
        self.replace_str([u'\ufebf', u'\ufec0'], 'ض')
        self.replace_str([u'\ufebe'], 'ض‌')
        self.replace_str([u'\ufec3', u'\ufec4'], 'ط')
        self.replace_str([u'\ufec2'], 'ط‌')
        self.replace_str([u'\ufec7', u'\ufec8'], 'ظ')
        self.replace_str([u'\ufec6'], 'ظ‌')
        self.replace_str([u'\ufecb', u'\ufecc'], 'ع')
        self.replace_str([u'\ufeca'], 'ع‌')
        self.replace_str([u'\ufecf', u'\ufed0'], 'غ')
        self.replace_str([u'\ufece'], 'غ‌')
        self.replace_str([u'\ufed3', u'\ufed4'], 'ف')
        self.replace_str([u'\ufed2'], 'ف‌')
        self.replace_str([u'\ufed7', u'\ufed8'], 'ق')
        self.replace_str([u'\ufed6'], 'ق‌')
        self.replace_str([u'\u0643', u'\ufb90', u'\ufedb', u'\ufedc'], 'ک')
        self.replace_str([u'\ufb8e', u'\ufeda'], 'ک‌')
        self.replace_str([u'\ufb94', u'\ufb95'], 'گ')
        self.replace_str([u'\ufb93'], 'گ‌')
        self.replace_str([u'\ufedf', u'\ufee0'], 'ل')
        self.replace_str([u'\ufede'], 'ل‌')
        self.replace_str([u'\ufee3', u'\ufee4'], 'م')
        self.replace_str([u'\ufee2'], 'م‌')
        self.replace_str([u'\ufee7', u'\ufee8'], 'ن')
        self.replace_str([u'\ufee6'], 'ن‌')
        self.replace_str([u'\ufeee', u'\ufe86'], 'و')
        self.replace_str([u'\ufeeb', u'\ufeec'], 'ه')
        self.replace_str([u'\ufee9', u'\ufeea'], 'ه‌')
        self.replace_str([u'\u064a', u'\ufef3', u'\ufef4'], 'ی')
        self.replace_str([u'\ufef2'], 'ی‌')
        self.replace_str([u'\ufe8b', u'\ufe8c'], 'ئ')
        self.replace_str([u'\ufefb', u'\ufefc'], 'لا')
        self.replace_str([u'\ufdf2'], 'لله‌')
        self.replace_str([u'\u202a', u'\u202b', u'\u202c', u'\x0c'], '')
        self.replace_str([r'\(', r'\)', r'\[', r'\]', r'\«', r'\»'], '"')

        # letters = 'آ|ا|ب|پ|ت|ث|ج|چ|ح|خ|د|ذ|ر|ز|ژ|س|ش|ص|ض|ط|ظ|ع|غ|ف|ق|ک|گ|ل|م|ن|و|ه|ی|ي'
        # unicode_corrected = re.sub(r'([' + letters + r'])‌([' + letters + '])', r'\1==\2', unicode_corrected)
        # replace_str(['‌'], '')
        # replace_str(['=='], '‌')
        # lines = normalized_main_text.split('\n')
        # line_joined_normalized_titled_text = re.sub('  ', ' ', ' '.join(lines))[3:]
