from __future__ import division

from string import digits, letters
import re


class EndToken(object):

    lbp = 0

class OperatorAddToken(object):

    lbp = 10  # left binding power

    def nud(self):
        self.first = expression(100)
        self.second = None
        return self

    def led(self, left):
        self.first = left
        self.second = expression(10)
        return self.first + self.second

    def __repr__(self):
        return "(add {} {})".format(self.first, self.second)


class OperatorSubToken(object):
    lbp = 10

    def nud(self):
        self.first = -expression(100)
        self.second = None
        return self

    def led(self, left):
        self.first = left
        self.second = expression(10)
        return self.first - self.second

    def __repr__(self):
        return "(sub {} {})".format(self.first, self.second)


class OperatorMulToken(object):
    lbp = 20

    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self.first * self.second

    def __repr__(self):
        return "(mul {} {})".format(self.first, self.second)


class OperatorPowToken(object):
    lbp = 30

    def led(self, left):
        self.first = left
        self.second = expression(30 - 1)
        return self.first ** self.second

    def __repr__(self):
        return "(pow  {} {})".format(self.first, self.second)

class OperatorDivToken(object):
    lbp = 20

    def led(self, left):
        self.first = left
        self.second = expression(20)
        return self.first / self.second

    def __repr__(self):
        return "(div {} {})".format(self.first, self.second)


class LiteralToken(object):

    def __init__(self, value):
        self.digit = int(value)

    def nud(self):  # null denotation
        return self.digit

    def __repr__(self):
        return "(literal {})".format(self.digit)

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

token_pat = re.compile("\s*(?:(\d+)|(\*\*|.))")

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
        elif operator == "**":
            yield OperatorPowToken()
        else:
            raise SyntaxError("unknown operator")
    yield EndToken()


def parse(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()

# The cheap way, without a parse tree.
def evaluate(self, s):
    invalids = letters + "!#$&\',:;<=>?@[\\]_`{|}~"
    if any(c in invalids for c in s) or not any(c in digits for c in s):
        return
    return eval(s)



if __name__ == "__main__":
#     print parse("1+2-3")
    print parse("3+2*4/2**4")
#     print parse("10/4")
#     print parse("(10**2)**3")

