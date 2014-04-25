from __future__ import division

from string import digits, letters
import re


class EndToken(object):

    lbp = 0

class OperatorAddToken(object):

    lbp = 10  # left binding power

    def nud(self):
        return expression(100)

    def led(self, left):
        return left + expression(10)

class OperatorSubToken(object):
    lbp = 10

    def nud(self):
        return -expression(100)

    def led(self, left):
        return left - expression(10)

class OperatorMulToken(object):
    lbp = 20
    def led(self, left):
        return left * expression(20)

class OperatorDivToken(object):
    lbp = 20
    def led(self, left):
        return left / expression(20)


class LiteralToken(object):

    def __init__(self, value):
        self.digit = int(value)

    def nud(self):  # null denotation
        return self.digit

def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

token_pat = re.compile("\s*(?:(\d+)|(.))")

def tokenize(program):
    for number, operator in token_pat.findall(program):
        if number:
            yield LiteralToken(number)
        elif operator == "+":
            yield OperatorAddToken()
        elif operator == "-":
            yield OperatorSubToken()
        elif operator == "/":
            yield OperatorDivToken()
        elif operator == "*":
            yield OperatorMulToken()
        else:
            raise SyntaxError("unknown operator")
    yield EndToken()


def parse(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()

class Calculation(object):

    def evaluate(self, s):
        invalids = letters + "!#$&\',:;<=>?@[\\]_`{|}~"
        if any(c in invalids for c in s) or not any(c in digits for c in s):
            return
        return eval(s)



if __name__ == "__main__":
    c = Calculation()
    print parse("1+2")
    print parse("10/4")
    print parse("10*3+4/7-2")

