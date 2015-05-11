import log_utils
from lexer import LexicalAnalyzer
from math_token import Number, Operator, OpenParenthesis, CloseParenthesis


class ShuntingYardParser(object):

    def __init__(self, expression, logger):
        self.logger = logger
        self.operators_stack = []
        self.output_queue = []
        self.lexer = LexicalAnalyzer(expression)

        self.ops_map = {
            Number: self.handle_number,
            Operator: self.handle_operator,
            OpenParenthesis: self.handle_open_parenthesis,
            CloseParenthesis: self.handle_close_parenthesis,
        }

    def parse(self):
        for token in self.lexer:
            self.ops_map[type(token)](token)

        # Add the remaining operators to the output queue.
        while len(self.operators_stack) > 0:
            top = self.operators_stack.pop()
            if isinstance(top, OpenParenthesis):
                raise SyntaxError("Unbalanced parenthesis")
            self.output_queue.append(top)

        return self.output_queue[:]

    def handle_number(self, token):
        self.output_queue.append(token)

    def peek(self):
        """
        Retrieve the topmost token from the operators stack, without popping it.

        :return: The top operator on stack, or None if the stack is empty.
        """
        return self.operators_stack[-1] if len(self.operators_stack) > 0 else None

    def handle_operator(self, operator):
        top = self.peek()
        while (top is not None
               and isinstance(top, Operator)
               and top.priority > operator.priority):
            self.output_queue.append(self.operators_stack.pop())
            top = self.peek()
        self.operators_stack.append(operator)

    def handle_open_parenthesis(self, open_parenthesis):
        self.operators_stack.append(open_parenthesis)

    # noinspection PyUnusedLocal
    def handle_close_parenthesis(self, token):
        while len(self.operators_stack) > 0:
            top = self.operators_stack.pop()
            if isinstance(top, OpenParenthesis):
                self.logger.debug("Found balancing open parenthesis - discarding both")
                return

            self.output_queue.append(top)

        raise SyntaxError("Unbalanced parenthesis - Missing open parenthesis")


def test():
    logger = log_utils.get_logger("ShuntingYardParser")
    parser = ShuntingYardParser("(2+1)*7", logger)
    print [str(token) for token in parser.parse()]


if __name__ == '__main__':
    test()