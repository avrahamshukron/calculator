__author__ = "avraham.shukron@gmail.com"


class Calculator(object):

    def __init__(self):
        self._stack = []
        self._token_list = []

    def evaluate(self):
