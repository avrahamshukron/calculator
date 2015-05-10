#! /usr/bin/python

__author__ = "tal.shorer@gmail.com"


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
