#! /usr/bin/python

__author__ = "tal.shorer@gmail.com"


from lexer import LexicalAnalyzer
from math_token import (Number, OpenParenthesis, CloseParenthesis, Operators,
                        Operator)
from bintree import BinTree
import log_utils


class BinTreeParser(object):

    _logger = log_utils.get_logger("bt_parser")

    @classmethod
    def parse(cls, tokens):
        # parentheses:
        #   find leftmost ")"
        #   find rightmost "("
        #   parse everything in between and replace it with the result
        while True:
            for close_index, t in enumerate(tokens):
                if isinstance(t, CloseParenthesis):
                    break
            else:  # no closing parenthesis
                break
            for open_index in range(close_index - 1, -1, -1):
                t = tokens[open_index]
                if isinstance(t, OpenParenthesis):
                    break
            else:  # open parenthesis not found, unbalanced parentheses
                msg = ("No closing parenthesis for closing parenthesis at index %s" %
                       (close_index,))
                raise ValueError(msg)
            tree = cls.parse(tokens[open_index + 1:close_index])
            tokens = tokens[:open_index] + [tree] + tokens[close_index + 1:]

        for operator in Operators.ALL_OPERATORS:
            while True:
                hit = False
                for index, t in enumerate(tokens):
                    if not isinstance(t, Operator):
                        continue
                    if t == operator:
                        hit = True
                        break
                if not hit:
                    break
                tree = BinTree(operator, tokens[index - 1], tokens[index + 1])
                tokens = tokens[:index - 1] + [tree] + tokens[index + 2:]
        assert len(tokens) == 1, ("%s did not consume all tokens" %
                                  (cls.__name__,))
        return tokens[0]

    @classmethod
    def solve(cls, tree):
        if isinstance(tree, Number):  # a number
            return tree.value
        left = cls.solve(tree.left)
        right = cls.solve(tree.right)
        return tree.value(left, right)


def test_parser():
    lexer = LexicalAnalyzer("2*(1+1)+1")
    tokens = [t for t in lexer]
    t = BinTreeParser.parse(tokens)
    print t
    print BinTreeParser.solve(t)


if __name__ == '__main__':
    test_parser()
