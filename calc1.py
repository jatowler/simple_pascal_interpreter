#!/usr/bin/env python3

INTEGER = 'INTEGER'
PLUS = 'PLUS'
EOF = 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, EOF
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

class Interpreter(object):
    def __init__(self, text):
        # client string input
        self.text = text

        # index into self.text
        self.pos = 0

        # current token
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        '''Lexical analyzer (tokenizer)

        Break a sentence apart into tokens, one at a time.
        '''
        text = self.text

        # if self.pos beyond the end of self.text,
        # return EOF
        if self.pos > (len(text) - 1):
            return Token(EOF, None)

        # get the current character and decide what to do with it
        current_char = text[self.pos]

        while current_char.isspace():
            self.pos += 1
            if self.pos > (len(text) - 1):
                return Token(EOF, None)
            current_char = text[self.pos]

        if current_char.isdigit():
            num_string = ''
            while current_char.isdigit():
                num_string += current_char
                self.pos += 1
                if self.pos > (len(text) - 1):
                    break
                current_char = text[self.pos]

            token = Token(INTEGER, int(num_string))
            return token
        
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        # We didn't recognize this token
        self.error()

    def eat(self, token_type):
        '''Eat a token of the expected type, or die.'''
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        '''expr -> INTEGER PLUS INTEGER'''
        # set current token to first token from input
        self.current_token = self.get_next_token()

        # expect current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # then expect a '+' token
        op = self.current_token
        self.eat(PLUS)

        # then expect a single-digit integer
        right = self.current_token
        self.eat(INTEGER)

        # self.current_token should now be EOF

        # Now we know we're adding, so just do it
        result = left.value + right.value
        return result

def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == "__main__":
    main()
