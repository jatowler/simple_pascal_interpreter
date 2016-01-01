#!/usr/bin/env python3

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'TIMES'
DIV = 'DIVIDED_BY'
EOF = 'EOF'

OPS = {
        '+': PLUS,
        '-': MINUS,
        '*': MUL,
        '/': DIV
      }

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, EOF
        self.type = type
        # token value: [0-9+] or None
        self.value = value

    def __str__(self):
        '''String representation of the instance.'''
        return 'Token({type}, {value})'.format(
                type=self.type,
                value=repr(self.value)
                )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        '''Advance self.pos and set self.current_char.'''
        self.pos += 1

        if self.pos > (len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        '''Return a (potentially multidigit) integer'''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)
    
    def get_next_token(self):
        '''Lexical analyzer (tokenizer)

        Break a sentence apart into tokens, one at a time.
        '''
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char in OPS:
                token = Token(
                        OPS[self.current_char],
                        self.current_char)
                self.advance()
                return token

            self.error()

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        '''Eat a token of the expected type, or die.'''
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        '''factor : INTEGER'''
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
        '''term : factor ((MUL | DIV factor)*'''
        result = self.factor()
        
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(token.type)
            
            if token.type == MUL:
                result = result * self.factor()
            elif token.type == DIV:
                result = result / self.factor()

        return result

    def expr(self):
        '''Parser/interpreter
        
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        '''
        # set current token to first token from input
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            self.eat(op.type)

            if op.type == PLUS:
                result = result + self.term()
            elif op.type == MINUS:
                result = result - self.term()

        return result

def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break

        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == "__main__":
    main()
