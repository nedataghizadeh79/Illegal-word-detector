from typing import List
import re

from illegal_word_finder import tokenize, hazm_normalize, VALID_PERSIAN_CHARS_REGEX


def custom_simplifier(tokens: List[str]):
    result = []
    recurrent_pattern = rf'({VALID_PERSIAN_CHARS_REGEX})\1+'
    for token in tokens:
        result.append(re.sub(recurrent_pattern, r'\1', token[0]))
    return result


def run(text: str, illegals: List[str]):
    tokens = hazm_normalize(tokenize(text))
    tokens = custom_simplifier(tokens)
    # TODO: simplify the illegal words

    # TODO: check if tokens are illegal

    # TODO: check for false positives

    # return result


if __name__ == '__main__':
    t = "سلاااااام گلابی مکرر چطوری داداچ؟"
    il = ["گل", "جطور", "دادا", "سلام"]
    run(t, il)
