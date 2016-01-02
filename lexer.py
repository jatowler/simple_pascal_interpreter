#!/usr/bin/env python3

from token import Token, INTEGER, OPS, EOF

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
