#!/usr/bin/env python3

import token as spi_token

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.token = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        '''factor : INTEGER | LPAREN expr RPAREN'''
        token = self.current_token
        if token.type == spi_token.INTEGER:
            self.eat(spi_token.INTEGER)
            return Num(token)
        elif token.type == spi_token.LPAREN:
            self.eat(spi_token.LPAREN)
            node = self.expr()
            self.eat(spi_token.RPAREN)
            return node
    
    def term(self):
        '''term: factor ((MUL | DIV) factor)*'''
        node = self.factor()

        while self.current_token.type in (spi_token.MUL, spi_token.DIV):
            token = self.current_token
            self.eat(token.type)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        '''
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        '''
        node = self.term()

        while self.current_token.type in (spi_token.PLUS, spi_token.MINUS):
            token = self.current_token
            self.eat(token.type)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()
