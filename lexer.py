__author__ = 'avraham.shukron@gmail.com'

import log_utils

from math_token import Tokens


class LexicalError(Exception):
    pass


class LexicalAnalyzer(object):

    READ_CHUNK_SIZE = 1024

    def __init__(self, input_string, logger=None):
        self._input_string = input_string.strip()
        self._logger = (logger if logger is not None
                        else log_utils.get_logger("lexer"))

    @staticmethod
    def find_next_match(input_string):
        """
        Scan for the next valid token.
        Upon success, returns a tuple of the next token in the string, and the
        remainder of the string without the token

        :param input_string: The string to scan.
        :type input_string: str
        :return: (Token | None, str | None) The token found, and the remaining
        string.
        """
        # Try and match all the possible tokens.
        results = [(cls.match(input_string), cls)
                   for cls in Tokens.ALL_TOKENS]

        # Filter only the tokens that matches the beginning of the string.
        matches = [r for r in results if r[0] is not None]

        # Get the longest match.
        if len(matches) > 0:
            _, token_cls = sorted(matches,
                                  key=lambda r: r[0].end(),
                                  reverse=True)[0]
            return token_cls.tokenize(input_string)

        return None, input_string

    def __iter__(self):
        return self

    def next(self):
        """
        :return: The next token, or raise LexicalError if the next token is
        invalid.
        """
        if self._input_string is None or len(self._input_string) == 0:
            self._logger.debug("No more data to parse. Stopping")
            # Nothing to parse.
            raise StopIteration

        next_token, remainder = self.find_next_match(self._input_string)
        if next_token is not None:
            self._input_string = remainder.strip()
            return next_token

        invalid_part = ""
        while next_token is None and len(remainder) > 0:
            invalid_part += remainder[:1]
            remainder = remainder[1:]
            next_token, remainder = self.find_next_match(remainder)

        self._input_string = remainder.strip()
        message = "Invalid syntax: %s" % (invalid_part,)
        self._logger.error(message)
        raise LexicalError(message)

    def parse_all(self):
        return [t for t in self]


if __name__ == '__main__':
    lexer = LexicalAnalyzer("23 ( 55 ) * +             66 ")
    for token in lexer:
        print token
