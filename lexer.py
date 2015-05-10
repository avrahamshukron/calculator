__author__ = 'avraham.shukron@gmail.com'

import log_utils

from token import TokenType, Token


class LexicalError(Exception):
    pass


class LexicalAnalyzer(object):

    READ_CHUNK_SIZE = 1024

    def __init__(self, input_string, logger=None):
        self._input_string = input_string
        self._logger = logger if logger is not None else log_utils.get_logger("lexer")

    @staticmethod
    def find_next_match(input_string):
        """
        Scan for the next valid token.
        Upon success, returns a tuple of the next token in the string, and the remainder of
        the string without the token

        :param input_string: The string to scan.
        :type input_string: str
        :return: (Token | None, str | None)
        """
        for regex in TokenType.REGEX_LIST:
            match = regex.match(input_string)
            if match is not None:
                lexeme = match.group()
                token_type = TokenType.of_regex(regex)
                remaining_string = input_string[match.end():]
                return Token(token_type, lexeme), remaining_string

        return None, input_string

    def __iter__(self):
        return self

    def next(self):
        """
        :return: The next token, or raise LexicalError if the next token is invalid.
        """
        if self._input_string is None or len(self._input_string) == 0:
            self._logger.debug("No more data to parse. Stopping")
            # Nothing to parse.
            raise StopIteration

        next_token, remaining_string = self.find_next_match(self._input_string)
        if next_token is not None:
            self._input_string = remaining_string
            return next_token

        invalid_part = ""
        while next_token is None and len(remaining_string) > 0:
            invalid_part += remaining_string[:1]
            remaining_string = remaining_string[1:]
            next_token, remaining_string = self.find_next_match(remaining_string)

        self._input_string = remaining_string
        message = "Invalid syntax: %s" % (invalid_part,)
        self._logger.error(message)
        raise LexicalError(message)


if __name__ == '__main__':
    lexer = LexicalAnalyzer("23(55)*+")
    for token in lexer:
        print token
