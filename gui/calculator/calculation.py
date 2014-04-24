from string import digits, letters
import ast
import token


class AddToken(object):

    priority = 10

    def led(self, left):
        right = Calculation().parse(10)
        return left + right

class Calculation(object):

    def evaluate(self, s):
        invalids = letters + "!#$&\',:;<=>?@[\\]_`{|}~"
        if any(c in invalids for c in s) or not any(c in digits for c in s):
            return
        return eval(s)

    def parse(self, s):
        return s

    def dostuff(self):
        return AddToken().led(5)


if __name__ == "__main__":
    c = Calculation()
    print c.evaluate("-+10")
    print c.dostuff()

