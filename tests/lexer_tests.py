__author__ = "avraham.shukron@gmail.com"

import sys
import unittest

from calculator.lexer import LexicalAnalyzer
from calculator.math_token import IntegerNumber, FloatingPointNumber


class LexerTest(unittest.TestCase):

    def check_numbers(self, expected_token_class, lexemes, number_type):
        lexer = LexicalAnalyzer(" ".join([str(i) for i in lexemes]))
        tokens = lexer.parse_all()
        for t, lexeme in zip(tokens, lexemes):
            self.assertIsInstance(t, expected_token_class)
            self.assertEqual(t.value, number_type(lexeme))

    def test_valid_integers(self):
        lexemes = ["1", "44", "666", "0465", "0000", sys.maxint]
        self.check_numbers(IntegerNumber, lexemes, int)

    def test_valid_floats(self):
        lexemes = [".1", ".443444", "34253.666", ".0465", "0.0000000000001"]
        self.check_numbers(FloatingPointNumber, lexemes, float)


if __name__ == "__main__":
    unittest.main()
