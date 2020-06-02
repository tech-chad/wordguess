# Word guessing game by selecting letters one at a time.
import os
import sys
from random import choice

from typing import List
from typing import Tuple

WORD_LIST_FILE = "words.txt"
MAX_GUESSES = 6


class WordGuessError(Exception):
    pass


def clear_screen() -> None:
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


def load_words() -> List[str]:
    # load words from file return list of capitalized words
    words = []
    try:
        with open(WORD_LIST_FILE, "r") as f:
            data = f.read()
    except FileNotFoundError:
        raise WordGuessError("Error words.txt file not found")
    else:
        for w in data.split():
            words.append(w)

        return words


def random_word(word_list: List[str]) -> str:
    word = choice(word_list)
    return word


def setup_word(word: str) -> Tuple[List[str], List[str]]:
    # split word into letters, make a blank word using _ for the letter
    split_word = [x for x in word]
    blank_word = ["_" for _ in word]
    return split_word, blank_word


def play(word: str) -> None:
    split_word, blank_word = setup_word(word)
    letters = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    number_of_guesses = 1
    while number_of_guesses <= MAX_GUESSES:
        clear_screen()
        print("Word Guess")
        print()
        print(*letters)
        print()
        print(*blank_word)
        print()
        print(f"Guess {number_of_guesses} out of {MAX_GUESSES}")
        user_input = input("Enter an unused letter or 'quit': ").upper()
        if user_input == "QUIT":
            return
        if user_input not in letters:  # already been guessed
            print("Letter already been picked try again")
            continue
        else:
            if user_input in split_word:
                # replace blank with letter
                for i, letter in enumerate(split_word):
                    if letter == user_input:
                        blank_word[i] = letter
                # replace letter with space
                for i, letter in enumerate(letters):
                    if letter == user_input:
                        letters[i] = " "
                        break
                if blank_word == split_word:
                    print("You got the word.  You Won!")
                    return
            else:  # not in word
                print("not in word")
                # replace letter with space
                for i, letter in enumerate(letters):
                    if letter == user_input:
                        letters[i] = " "
                        break
                number_of_guesses += 1
    print("out of guesses")
    print(f"The word was  {word}")
    return


def main() -> int:
    word_list = load_words()
    rand_word = random_word(word_list)
    play(rand_word)
    return 0


if __name__ == "__main__":
    exit(main)
