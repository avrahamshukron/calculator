__author__ = "avraham.shukron@gmail.com"


import math
import re

CARET_SIGN = "^"
SLASH_SIGN = "/"
STAR_SIGN = "*"
MINUS_SIGN = "-"
PLUS_SIGN = "+"


class TokenType(object):
    TOKEN_TYPE_NUMBER = "Number"
    TOKEN_TYPE_OPERATOR = "Operator"
    OPEN_PARENTHESIS = "Open Parenthesis"
    CLOSE_PARENTHESIS = "Close Parenthesis"

    NUMBER_PATTERN = r"\d+"
    NUMBER_REGEX = re.compile(NUMBER_PATTERN, re.VERBOSE)

    BINARY_OP_PATTERN = r"[\+\-\*/%$]"
    BINARY_OP_REGEX = re.compile(BINARY_OP_PATTERN, re.VERBOSE)

    UNARY_PREFIX_OP_PATTERN = r"[~]"
    UNARY_PREFIX_OP_REGEX = re.compile(UNARY_PREFIX_OP_PATTERN, re.VERBOSE)

    UNARY_SUFFIX_OP_PATTERN = r"[!]"
    UNARY_SUFFIX_OP_REGEX = re.compile(UNARY_SUFFIX_OP_PATTERN, re.VERBOSE)

    OPEN_PARENTHESIS_PATTERN = r"\("
    OPEN_PARENTHESIS_REGEX = re.compile(OPEN_PARENTHESIS_PATTERN, re.VERBOSE)

    CLOSE_PARENTHESIS_PATTERN = r"\)"
    CLOSE_PARENTHESIS_REGEX = re.compile(CLOSE_PARENTHESIS_PATTERN, re.VERBOSE)

    REGEX_MAP = {
        NUMBER_REGEX: TOKEN_TYPE_NUMBER,
        BINARY_OP_REGEX: TOKEN_TYPE_OPERATOR,
        OPEN_PARENTHESIS_REGEX: OPEN_PARENTHESIS,
        CLOSE_PARENTHESIS_REGEX: CLOSE_PARENTHESIS
    }

    REGEX_LIST = [
        NUMBER_REGEX,
        BINARY_OP_REGEX,
        UNARY_PREFIX_OP_REGEX,
        UNARY_SUFFIX_OP_REGEX,
        OPEN_PARENTHESIS_REGEX,
        CLOSE_PARENTHESIS_REGEX,
    ]

    @classmethod
    def of_regex(cls, regex):
        return cls.REGEX_MAP[regex]


class Token(object):

    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def __str__(self):
        return "%s: '%s'" % (self.token_type, self.lexeme)

    def __repr__(self):
        return "%s('%s', '%s')" % (self.__class__.__name__, self.token_type, self.lexeme)


class Operator(Token):

    def __init__(self, symbol, priority, func):
        Token.__init__(self, TokenType.TOKEN_TYPE_OPERATOR, symbol)
        self.priority = priority
        self.func = func

    def __cmp__(self, other):
        return self.priority.__cmp__(other.priority)

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


class Operators(object):

    @staticmethod
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

    PLUS = Operator(PLUS_SIGN, 1, lambda x, y: x + y)
    MINUS = Operator(MINUS_SIGN, 1, subtract)
    MULTIPLY = Operator(STAR_SIGN, 2, lambda x, y: x * y)
    DIVIDE = Operator(SLASH_SIGN, 2, lambda x, y: x / y)
    POWER = Operator(CARET_SIGN, 3, math.pow)

    MAP = {
        PLUS_SIGN: PLUS,
        MINUS_SIGN: MINUS,
        STAR_SIGN: MULTIPLY,
        SLASH_SIGN: DIVIDE,
        CARET_SIGN: POWER,
    }
