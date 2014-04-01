#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian

    Note: To display it in a non-maddening way, you'd have to use a
    console interface library like urwid.
"""


from random import shuffle, choice
import sys

gallow = [
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
\t|   \o/
\t|    |
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
    indices =  [i for i, c in enumerate(word) if c == guess]
    guessed_word = list(guessed_word)
    for i in indices:
        guessed_word[i] = guess
    return "".join(guessed_word)

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
        guesses = set()
        mistakes = 0
        print gallow[0]
        print "".join(word)
        
        # Main loop.
        while word != guessed_word and mistakes < 6:
            # Add spaces when displaying the words to see the length.
            print " ".join(guessed_word)

            guess = raw_input(" ")

            if guess in guesses:
                print "you've already guessed", guess
            elif guess not in word:
                mistakes += 1
                print gallow[mistakes]
            else:
                guessed_word = update_guessed_word(guess, word, guessed_word)
                
            guesses.add(guess)

        # Check for victory.
        print guessed_word
        if mistakes == 6:
            print "-"*10
            print "sorry mate, you've lost."
            print "the word was '{}'".format(word)
            print "-"*10
        else:
            print "-"*10
            print "congrats! you've won!"
            print "-"*10


if __name__ == "__main__":
    main()
