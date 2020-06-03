# Word guessing game by selecting letters one at a time.
import argparse
import os
import sys
from random import choice
from time import sleep

import argparse_types

from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

WORD_LIST_FILE = "words.txt"
DEFAULT_NUM_WRONG_GUESSES = 6
SLEEP_TIME = 3


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


def display(letters: List[str],
            blank_word: List[str],
            guess_num: int,
            num_wrong_guesses: int) -> None:
    clear_screen()
    print("Word Guess")
    print()
    print(*letters)
    print()
    print(*blank_word)
    print()
    print(f"Wrong Guesses {guess_num} out of {num_wrong_guesses}")


def play(word: str, num_wrong_guesses: int) -> None:
    split_word, blank_word = setup_word(word)
    letters = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    number_of_guesses = 0
    while number_of_guesses < num_wrong_guesses:
        display(letters, blank_word, number_of_guesses, num_wrong_guesses)
        user_input = input("Enter a letter or 'quit' to quit: ").upper()

        if user_input == "QUIT":
            print("quitting")
            return

        elif len(user_input) > 1 or not user_input.isalpha():
            print("Invalid input please try again")
            sleep(SLEEP_TIME)
            continue

        if user_input not in letters:  # already been guessed
            print("Letter already been picked try again")
            sleep(SLEEP_TIME)
            continue

        else:
            # replace letter with space
            for i, letter in enumerate(letters):
                if letter == user_input:
                    letters[i] = " "
                    break

            if user_input in split_word:
                # replace blank with letter
                for i, letter in enumerate(split_word):
                    if letter == user_input:
                        blank_word[i] = letter

                if blank_word == split_word:
                    display(letters, blank_word,
                            number_of_guesses, num_wrong_guesses)

                    print("You Won! You got the word")
                    sleep(SLEEP_TIME)
                    return

            else:  # not in word
                print(f"Letter {user_input} not in the word")
                sleep(SLEEP_TIME)
                number_of_guesses += 1

    display(letters, blank_word, number_of_guesses, num_wrong_guesses)
    print("Out of guesses")
    print(f"The word was  {word}")
    sleep(SLEEP_TIME)
    return


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", dest="num_wrong_guesses",
                        type=argparse_types.pos_int,
                        default=DEFAULT_NUM_WRONG_GUESSES,
                        help="Number of wrong guess default: %(default)s"),

    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = argument_parser(argv)
    word_list = load_words()
    rand_word = random_word(word_list)
    play(rand_word, args.num_wrong_guesses)
    return 0


if __name__ == "__main__":
    exit(main)
