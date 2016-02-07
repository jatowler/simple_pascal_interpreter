#!/usr/bin/env python3

import token
import lexer
import parser
import interpreter

def main():
    while True:
        try:
            text = raw_input('spi> ')
        except EOFError:
            break

        if not text:
            continue

        l = lexer.Lexer(text)
        p = parser.Parser(l)
        i = interpreter.Interpreter(p)
        result = i.interpret()
        print(result)

if __name__ == "__main__":
    main()
