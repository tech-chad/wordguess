# Word guessing game by selecting letters one at a time.
import argparse
import os
import sys
from random import choice
from time import sleep

import argparse_types
import argparse_custom_types

from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

if sys.version_info >= (3, 7):
    from importlib.resources import read_text
else:
    from importlib_resources import read_text

version = importlib_metadata.version("wordguess")

WORD_LIST_FILE = "words.txt"
DEFAULT_NUM_WRONG_GUESSES = 6
DEFAULT_MAX_LENGTH = 15
DEFAULT_MIN_LENGTH = 4
SLEEP_TIME = 3


def clear_screen() -> None:
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


class Color:
    red = "\033[1;31m"
    green = "\033[1;32m"
    white = "\033[1;37;40m"
    reset = "\033[m"


def load_words(min_length: int, max_length: int) -> List[str]:
    # load words from file return list of capitalized words
    words = []
    data = read_text("wordguess", WORD_LIST_FILE)
    for w in data.split():
        if min_length <= len(w) <= max_length:
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
            num_wrong_guesses: int,
            color: bool) -> None:
    clear_screen()
    if color:
        print(f"{Color.white}Word Guess{Color.reset}")
    else:
        print("Word Guess")
    print()
    print(*letters)
    print()
    print(*blank_word)
    print()
    print(f"Wrong Guesses {guess_num} out of {num_wrong_guesses}")


def play(word: str, num_wrong_guesses: int, color: bool) -> int:
    # clr = Color()
    split_word, blank_word = setup_word(word)
    letters = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    num_of_guesses = 0
    while num_of_guesses < num_wrong_guesses:
        display(letters, blank_word, num_of_guesses, num_wrong_guesses, color)
        user_input = input("Enter a letter or 'quit' to quit: ").upper()

        if user_input == "QUIT":
            print("quitting")
            return -1

        elif len(user_input) > 1 or not user_input.isalpha():
            if color:
                print(f"{Color.red}Invalid input please try again{Color.reset}")
            else:
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
                            num_of_guesses, num_wrong_guesses, color)
                    msg = "You Won! You got the word"
                    if color:
                        print(f"{Color.green}{msg}{Color.reset}")
                    else:
                        print(msg)
                    sleep(SLEEP_TIME)
                    return 0

            else:  # not in word
                print(f"Letter {user_input} not in the word")
                sleep(SLEEP_TIME)
                num_of_guesses += 1

    display(letters, blank_word, num_of_guesses, num_wrong_guesses, color)
    if color:
        print(f"{Color.red}Out of guesses{Color.reset}")
    else:
        print("Out of guesses")
    print(f"The word was  {word}")
    sleep(SLEEP_TIME)
    return 0


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    word_length = argparse_custom_types.int_range(4, 16)
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", dest="num_wrong_guesses",
                        type=argparse_types.pos_int,
                        default=DEFAULT_NUM_WRONG_GUESSES,
                        help="Number of wrong guess default: %(default)s")
    parser.add_argument("-s", dest="single_play", action="store_true",
                        help="single play then exit")
    parser.add_argument("-a", dest="auto_play", action="store_true",
                        help="continues game play until 'quit' is entered")
    parser.add_argument("--max", type=word_length, default=DEFAULT_MAX_LENGTH,
                        help="Max word length between 4 and 15")
    parser.add_argument("--min", type=word_length, default=DEFAULT_MIN_LENGTH,
                        help="Min word length between 4 and 15")
    parser.add_argument("--no_color", action="store_false",
                        help="No color mode")
    parser.add_argument("--version", action="version", version=version)

    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = argument_parser(argv)
    if args.min > args.max:
        print("Error min can't be larger than max")
        return 1
    word_list = load_words(args.min, args.max)
    while True:
        rand_word = random_word(word_list)
        return_value = play(rand_word, args.num_wrong_guesses, args.no_color)
        if args.single_play or args.auto_play and return_value == -1:
            break
        elif args.auto_play:
            continue
        else:
            user_input = input("Would you like to play again? (Yes or no): ")
            if user_input.upper() in ["YES", "Y"]:
                continue
            else:
                break
    return 0


if __name__ == "__main__":
    exit(main)
