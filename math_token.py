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

    # REGEX is set in Operators

    def __init__(self, lexeme, func=None, priority=None):
        Token.__init__(self, lexeme)
        # if func is not provided, we are initialized as a standard Token and
        # should look for our func and priority in Operators
        if func is None:
            op = Operators.find_op(lexeme)
            priority = op.priority
            func = op.func
        self.priority = priority
        self.func = func

    def __cmp__(self, other):
        return self.priority.__cmp__(other.priority)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Operators(object):

    # Initialize all priority values to None. They will be set dynamically by
    # a for loop after priority groups are defined

    ADD = Operator(PLUS_SIGN, lambda x, y: x + y)
    SUBTRACT = Operator(MINUS_SIGN, subtract)
    MULTIPLY = Operator(STAR_SIGN, lambda x, y: x * y)
    DIVIDE = Operator(SLASH_SIGN, lambda x, y: x / y)
    POWER = Operator(CARET_SIGN, math.pow)

    PRIORITY_GROUPS = (
        (POWER,),
        (MULTIPLY, DIVIDE),
        (ADD, SUBTRACT),
    )

    ALL_OPERATORS = ("".join("".join(operator.lexeme for operator in group)
                     for group in PRIORITY_GROUPS))
    Operator.REGEX = re.compile("[%s]" % (re.escape(ALL_OPERATORS)))

    for priority, group in enumerate(PRIORITY_GROUPS):
        for operator in group:
            operator.priority = priority

    @classmethod
    def find_op(cls, lexeme):
        for group in cls.PRIORITY_GROUPS:
            for operator in group:
                if operator.lexeme == lexeme:
                    return operator
        raise ValueError("No operator with lexeme %s" % (lexeme,))


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
