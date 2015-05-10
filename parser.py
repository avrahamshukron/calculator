from calculator.lexer import LexicalAnalyzer, TokenType


class ShuntingYardParser(object):

    def __init__(self, expression):
        self.operators_stack = []
        self.output_queue = []
        self.lexer = LexicalAnalyzer(expression)

        self.ops_map = {
            TokenType.TOKEN_TYPE_NUMBER: self.handle_number,
            TokenType.TOKEN_TYPE_OPERATOR: self.handle_binary_operator,
            TokenType.OPEN_PARENTHESIS: self.handle_open_parenthesis,
            TokenType.CLOSE_PARENTHESIS: self.handle_close_parenthesis,
        }

    def parse(self):
        for token in self.lexer:
            self.ops_map[token.token_type](token)

        while len(self.operators_stack) > 0:
            self.output_queue.append(self.operators_stack.pop())

        return self.output_queue[:]

    def handle_number(self, token):
        self.output_queue.append(token.lexeme)

    def handle_binary_operator(self, operator):
        current_top = self.operators_stack[0] if len(self.operators_stack) > 0 else None
        while current_top is not None and current_top.priority > operator.priority:
            self.output_queue.append(self.operators_stack.pop())
            current_top = self.operators_stack[0] if len(self.operators_stack) > 0 else None
        self.operators_stack.append(operator)

    def handle_open_parenthesis(self, open_parenthesis):
        self.operators_stack.append(open_parenthesis)

    def handle_close_parenthesis(self, token):
        if len(self.operators_stack) == 0:
            raise SyntaxError("Close parenthesis without matching open one")

        current_top = self.operators_stack.pop()
        while current_top.token_type != TokenType.OPEN_PARENTHESIS:
            self.output_queue.append(current_top)
