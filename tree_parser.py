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
        # parentheses:
        #   find leftmost ")"
        #   find rightmost "("
        #   parse everything in between and replace it with the result
        while True:
            for close_index, t in enumerate(tokens):
                if (isinstance(t, Token) and
                        t.token_type is TokenType.CLOSE_PARENTHESIS):
                    break
            else:  # no closing parenthesis
                break
            for open_index in range(close_index - 1, -1, -1):
                t = tokens[open_index]
                if (isinstance(t, Token) and
                        t.token_type is TokenType.OPEN_PARENTHESIS):
                    break
            else:  # open parenthesis not found, unbalanced parentheses
                msg = ("No closing parenthesis for closing parenthesis at index %s" %
                       (close_index,))
                raise ValueError(msg)
            tree = cls.parse(tokens[open_index + 1:close_index])
            tokens = tokens[:open_index] + [tree] + tokens[close_index + 1:]

        for priority_group in BinTreeParser.OPERATOR_PRIORITY:
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
                tree = BinTree(operator, tokens[index - 1], tokens[index + 1])
                tokens = tokens[:index - 1] + [tree] + tokens[index + 2:]
        assert len(tokens) == 1, ("%s did not consume all tokens" %
                                  (cls.__name__,))
        return tokens[0]

    @classmethod
    def solve(cls, tree):
        if isinstance(tree, Token):  # a number
            return float(tree.lexeme)
        left = cls.solve(tree.left)
        right = cls.solve(tree.right)
        return tree.value.func(left, right)


if __name__ == '__main__':
    lexer = LexicalAnalyzer("2*(1+1)+1")
    tokens = [t for t in lexer]
    t = BinTreeParser.parse(tokens)
    print t
    print BinTreeParser.solve(t)
