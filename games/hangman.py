#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian
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

def create_list(difficulty="easy"):
    easy, medium, hard = get_words()
    if difficulty == "hard":
        shuffle(hard)
        return hard
    elif difficulty == "medium":
        shuffle(medium)
        return medium
    else:
        shuffle(easy)
        return easy

def update_guessed_word(word, char):

    return [i for i, ltr in enumerate(word) if ltr == char]

def main():
    difficulty = choose_difficulty()
    words = create_list(difficulty)
    mistakes = 0
    word = [i for i in choice(words)]
    guessed_word = ["_" for i in range(len(word))]
    guesses = set()
    print gallow[0]

    while word != guessed_word:
        if mistakes == 6:
            print "you lose! the word was", "".join(word)
            main()
        
        sys.stdout.flush()
        print " ".join(guessed_word)
        
        guess = raw_input(" ")
        
        if guess in guesses:
            print "you've already guessed", guess
        elif guess not in word:
            mistakes += 1
            print gallow[mistakes]
        else:
            guessed_word = update_guessed_word(guess, word, guessed_word)
            word = [i for i in word if i != guess]
            print word
            
        guesses.add(guess)

    print "congrats! you've won!"
    
if __name__ == "__main__":
    main()
