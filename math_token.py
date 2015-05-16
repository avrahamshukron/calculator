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
    def match(cls, string):
        return cls.REGEX.match(string)

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

    KNOWN_OPERATORS = (
        {
            CARET_SIGN: math.pow,
        },
        {
            STAR_SIGN: lambda x, y: x * y,
            SLASH_SIGN: lambda x, y: x / y,
        },
        {
            PLUS_SIGN: lambda x, y: x + y,
            MINUS_SIGN: subtract,
        },
    )

    SYMBOLS = ("".join("".join(group.keys()) for group in KNOWN_OPERATORS))
    REGEX = re.compile("[%s]" % (re.escape(SYMBOLS)))

    @classmethod
    def get_known_operator_data(cls, lexeme):
        for priority, group in enumerate(cls.KNOWN_OPERATORS):
            for lexeme in group:
                return priority, group[lexeme]
        return None, None

    def __init__(self, lexeme, func=None, priority=None):
        Token.__init__(self, lexeme)

        known_priority, known_func = self.get_known_operator_data(lexeme)
        self.func = func if func is not None else known_func
        self.priority = (priority if priority is not None
                         else known_priority)
        if self.priority is None:
            raise ValueError("Unspecified priority")

        if self.func is None:
            raise ValueError("Unspecified operator func")

    def __cmp__(self, other):
        return self.priority.__cmp__(other.priority)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Operators(object):
    # All the operators, ordered by their priority, from top to bottom.
    ALL_OPERATORS = sorted([Operator(symbol) for symbol
                            in [group.keys() for group
                                in Operator.KNOWN_OPERATORS]],
                           key=lambda o: o.priority, reverse=True)


class Number(Token):

    NUMBER_TYPE = None

    def __init__(self, lexeme):
        Token.__init__(self, lexeme)
        self.value = self.NUMBER_TYPE(lexeme)

    def __repr__(self):
        return "%s" % (self.value,)


class IntegerNumber(Number):
    """
    Represents an integer number.
    Integer number is a series of digits that DOES NOT followed by a dot.
    """
    REGEX = re.compile(r"\d+")
    NUMBER_TYPE = int


class FloatingPointNumber(Number):
    """
    Represents a floating-point number.
    Floating point number is written with 0 or more leading digits representing
    the integer part, followed by a dot, followed by 0 or more digits
    representing the fraction.
    """
    REGEX = re.compile(r"\d*\.\d+")
    NUMBER_TYPE = float


class OpenParenthesis(Token):
    REGEX = re.compile(r"\(")


class CloseParenthesis(Token):
    REGEX = re.compile(r"\)")


class Tokens(object):

    ALL_TOKENS = [
        IntegerNumber,
        FloatingPointNumber,
        Operator,
        OpenParenthesis,
        CloseParenthesis,
    ]
