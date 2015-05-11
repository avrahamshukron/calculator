__author__ = "avraham.shukron@gmail.com"


import math
import re

CARET_SIGN = "^"
SLASH_SIGN = "/"
STAR_SIGN = "*"
MINUS_SIGN = "-"
PLUS_SIGN = "+"


class Token(object):

    REGEX = None  # For subclasses to override.

    @classmethod
    def is_a_match(cls, string):
        return cls.REGEX.match(string) is not None

    @classmethod
    def tokenize(cls, string):
        match = cls.REGEX.match(string)
        if match is not None:
            lexeme = match.group()
            remaining_string = string[match.end():]
            return cls(lexeme), remaining_string

        return None, string

    def __init__(self, lexeme, start_position=0, end_position=1):
        self.lexeme = lexeme
        self.start_position = start_position
        self.end_position = end_position

    def __str__(self):
        return "%s: '%s'" % (self.__class__.__name__, self.lexeme)


def subtract(x, y=None):
    """
    An implementation for the `"-"` operator. It supports both of its versions:
        - Binary operator: As expected.
        - Unary Prefix Operator: Adds an implicit `0` as the left operand.

    :param x: The first operand.
    :param y: The second operand. Can be omitted.
    :return: The result of `x - y` for binary operation, or `-x` for unary.
    """
    left = x if y is not None else 0
    right = y if y is not None else x
    return left - right


class Operator(Token):
    """
    Represents an operator.
    """
    MAP = {
        PLUS_SIGN: (1, lambda x, y: x + y),
        MINUS_SIGN: (1, subtract),
        STAR_SIGN: (2, lambda x, y: x * y),
        SLASH_SIGN: (2, lambda x, y: x / y),
        CARET_SIGN: (3, math.pow),
    }

    REGEX = re.compile("[%s]" % (re.escape("".join(MAP.keys()))))

    def __init__(self, lexeme):
        Token.__init__(self, lexeme)
        self.priority, self.func = self.MAP[lexeme]

    def __cmp__(self, other):
        return self.priority.__cmp__(other.priority)

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


class Number(Token):

    REGEX = re.compile(r"\d+")

    def __init__(self, lexeme):
        Token.__init__(self, lexeme)
        self.value = float(lexeme)


class OpenParenthesis(Token):
    REGEX = re.compile(r"\(")


class CloseParenthesis(Token):
    REGEX = re.compile(r"\)")


class Tokens(object):

    ALL_TOKENS = [
        Number,
        Operator,
        OpenParenthesis,
        CloseParenthesis,
    ]
