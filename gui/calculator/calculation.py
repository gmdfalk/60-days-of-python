import ast
from string import letters


class Calculation(object):

    def evaluate(self, s):
        invalids = letters + "!#$&\',:;<=>?@[\\]_`{|}~"
        if any(char in invalids for char in s):
            return
        return eval(s)

if __name__ == "__main__":
    c = Calculation()
    print c.evaluate("10*3")