#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian

    Note: To display it in a non-maddening way, you'd have to use a
    console interface library like urwid.
"""


from random import shuffle, choice
import sys

gallows = [
"""
\t______
\t|    |
\t|
\t|
\t|
\t|
""",
"""
\t______
\t|    |
\t|    o
\t|
\t|
\t|
""",
"""
\t______
\t|    |
\t|    o
\t|    |
\t|
\t|
""",
"""
\t______
\t|    |
\t|    o/
\t|    |
\t|
\t|
""",
"""
\t______
\t|    |
\t|   \o/
\t|    |
\t|
\t|
""",
"""
\t______
\t|    |
\t|   \o/
\t|    |
\t|   /
\t|
""",
"""
\t______
\t|    |
\t|    O
\t|   /|\\
\t|   / \\
\t|
"""]

def get_words():
    with open("wordlist.txt") as f:
        # Split the file at "EASY:", "MEDIUM:" and "HARD:".
        s = f.read().strip().split(":")
        easy = [i for i in s[1].split("\n") if i]
        medium = [i for i in s[2].split("\n") if i and i != "HARD"]
        hard = [i for i in s[3].split("\n") if i]

    return easy, medium, hard

def choose_difficulty():
    difficulty = ""
    difficulties = ["easy", "medium", "hard"]
    print difficulties
    while difficulty not in difficulties:
        difficulty = raw_input("Choose your difficulty: ")
    return difficulty

def create_wordlist(difficulty="easy"):
    easy, medium, hard = get_words()
    if difficulty == "hard":
        shuffle(hard)
        return hard
    elif difficulty == "medium":
        shuffle(medium)
        return medium
    else:  # Return easy even if not explicitly picked - as failsafe.
        shuffle(easy)
        return easy

def update_guessed_word(guess, word, guessed_word):
    "Update guessed_word to reflect correctly guessed characters"
    indices = [i for i, c in enumerate(word) if c == guess]
    guessed_word = list(guessed_word)
    for i in indices:
        guessed_word[i] = guess
    return "".join(guessed_word)


def check_endstate(mistakes, word, guessed_word):
    if word == guessed_word:
        print "\nYou've correctly guessed '{}'.".format(word)
        print "Congrats! You've won!"
        print "-"*10
    else:
        print "\nThe word was '{}'\nYou guessed  '{}'.".format(word,
                                                              guessed_word)
        print "Sorry mate, you've lost."
        print "-"*10
    print "\nNew Game!"


def main():
    used_words = set()
    while True:
        difficulty = choose_difficulty()
        words = set(create_wordlist(difficulty))
        # Get the symmetric difference of words and used_words.
        # Gotta love python syntax.
        words = list(words ^ used_words)
        word = choice(words)
        used_words.add(word)

        guessed_word = "".join(["_" for i in range(len(word))])
        guesses, wrong_guesses = set(), set()
        mistakes = 0

        # Main loop.
        while word != guessed_word and mistakes < 6:
            # Add spaces when displaying the words to see the length.
            print gallows[mistakes]
            print "missed:\t{}".format(" ".join(sorted(wrong_guesses)))
            print "word:\t{}".format(" ".join(guessed_word))

            # Guess until we have a unique lowercase string character.
            guess = ""
            while len(guess) != 1 or guess in guesses or not guess.islower():
                guess = raw_input("guess:\t")

            if guess not in word:
                mistakes += 1
                wrong_guesses.add(guess)
            else:
                guessed_word = update_guessed_word(guess, word, guessed_word)

            guesses.add(guess)

        # Check for victory.
        check_endstate(mistakes, word, guessed_word)



if __name__ == "__main__":
    print "\nWelcome to Hangman!"
    print "Guess the word before the man is hung and you win!"
    raw_input("\n\t---Enter to Continue---\n")
    main()
