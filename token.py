#!/usr/bin/env python3

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'TIMES'
DIV = 'DIVIDED_BY'
LPAREN = '('
RPAREN = ')'
EOF = 'EOF'

OPS = {
        '+': PLUS,
        '-': MINUS,
        '*': MUL,
        '/': DIV,
        '(': LPAREN,
        ')': RPAREN
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
