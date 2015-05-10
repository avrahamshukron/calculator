#! /usr/bin/python

__author__ = "tal.shorer@gmail.com"


from lexer import LexicalAnalyzer
from math_token import TokenType, Token, Operators
import log_utils


class BinTree(object):

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s, %s)" % (
            self.__class__.__name__,
            self.value,
            self.left,
            self.right,
        )


class BinTreeParser(object):

    _logger = log_utils.get_logger("bt_parser")

    OPERATOR_PRIORITY = (
        (Operators.POWER,),
        (Operators.MULTIPLY, Operators.DIVIDE),
        (Operators.PLUS, Operators.MINUS),
    )

    @classmethod
    def _search_in_group(cls, t, priority_group):
        for operator in priority_group:
            if (t.token_type == operator.token_type and
                    t.lexeme == operator.lexeme):
                return operator
        return None

    @classmethod
    def parse(cls, tokens):
        # TODO parentheses
        for priority_group in BinTreeParser.OPERATOR_PRIORITY:
            cls._logger.debug("starting priority group %s", priority_group)
            while True:
                operator = None
                for index, t in enumerate(tokens):
                    if (not isinstance(t, Token) or t.token_type is not
                            TokenType.TOKEN_TYPE_OPERATOR):
                        continue
                    operator = cls._search_in_group(t, priority_group)
                    if operator is not None:
                        break
                if operator is None:
                    break
                cls._logger.debug("found operator %s at index %s", operator,
                                  index)
                tree = BinTree(operator, tokens[index - 1], tokens[index + 1])
                tokens = tokens[:index - 1] + [tree] + tokens[index + 2:]
        assert len(tokens) == 1, ("%s did not consume all tokens" %
                                  (cls.__name__,))
        return tokens[0]


if __name__ == '__main__':
    lexer = LexicalAnalyzer("2+3*4")
    tokens = [t for t in lexer]
    t = BinTreeParser.parse(tokens)
    print t
