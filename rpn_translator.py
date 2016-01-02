#!/usr/bin/env python3

import lexer
import parser

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class RpnTranslator(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        return '{} {} {}'.format(
                self.visit(node.left),
                self.visit(node.right),
                node.op.value)

    def visit_Num(self, node):
        return str(node.value)

    def translate(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while True:
        try:
            text = raw_input('rpnt> ')
        except EOFError:
            break

        if not text:
            continue

        l = lexer.Lexer(text)
        p = parser.Parser(l)
        t = RpnTranslator(p)
        result = t.translate()
        print(result)

if __name__ == '__main__':
    main()
