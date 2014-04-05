import random


class QuotePicker(object):
    "Picks a quote from whatshesaid.txt"
    def __init__(self, quotesfile="whatshesaid.txt"):
        """Initialize our QuotationPicker class"""
        with open(quotesfile) as f:
            self.quotes = f.readlines()

    def pick(self):
        """Return a random quote."""
        return random.choice(self.quotes).strip()

def main():
    q = QuotePicker()
    q.pick()
