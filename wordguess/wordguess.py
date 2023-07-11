# Word guessing game by selecting letters one at a time.
import argparse
import importlib.resources
import os
import random
import sys
import time

from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

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
    yellow = "\033[1;93;93m"
    reset = "\033[m"


def load_words(min_length: int, max_length: int) -> List[str]:
    # load words from file return list of capitalized words
    words = []
    data = importlib.resources.read_text("wordguess", WORD_LIST_FILE)
    for w in data.split():
        if min_length <= len(w) <= max_length:
            words.append(w)

    return words


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


def play(word: str,
         num_wrong_guesses: int,
         color: bool,
         guess_word: bool) -> int:
    split_word, blank_word = setup_word(word)
    letters = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    num_of_guesses = 0
    while num_of_guesses < num_wrong_guesses:
        display(letters, blank_word, num_of_guesses, num_wrong_guesses, color)
        user_input = input("Enter a letter or 'quit' to quit: ").upper()

        if user_input == "QUIT":
            print("Quitting")
            return -1

        elif not user_input.isalpha():
            if color:
                print(f"{Color.red}Invalid input please try again{Color.reset}")
            else:
                print("Invalid input please try again")
            time.sleep(SLEEP_TIME)
            continue

        elif len(user_input) > 1:
            if guess_word and user_input == word:
                display(letters, split_word,
                        num_of_guesses, num_wrong_guesses, color)
                msg = "You Won! You guessed the word"
                if color:
                    print(f"{Color.green}{msg}{Color.reset}")
                else:
                    print(msg)
                time.sleep(SLEEP_TIME)
                return 0
            elif guess_word and user_input != word:
                print(f"{Color.yellow}{user_input} is not the correct "
                      f"word{Color.reset}")
                time.sleep(SLEEP_TIME)
                num_of_guesses += 1
            else:
                if color:
                    print(
                        f"{Color.red}Invalid input please try "
                        f"again{Color.reset}")
                else:
                    print("Invalid input please try again")
                time.sleep(SLEEP_TIME)
                continue

        elif user_input not in letters:  # already been guessed
            print(f"{Color.yellow}Letter already been picked try "
                  f"again{Color.reset}")
            time.sleep(SLEEP_TIME)
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
                    time.sleep(SLEEP_TIME)
                    return 0

            else:  # not in word
                print(f"{Color.yellow}Letter {user_input} not in the "
                      f"word{Color.reset}")
                time.sleep(SLEEP_TIME)
                num_of_guesses += 1

    display(letters, blank_word, num_of_guesses, num_wrong_guesses, color)
    if color:
        print(f"{Color.red}Out of guesses{Color.reset}")
    else:
        print("Out of guesses")
    print(f"The word was  {word}")
    time.sleep(SLEEP_TIME)
    return 0


def positive_int(value: str) -> int:
    """
    Used by argparse.
    Checks to see if the value is positive.
    """
    msg = f"{value} is an invalid positive int value"
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(msg)
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(msg)
    return int_value


def int_between_4_and_15(value: str) -> int:
    """
    Used by argparse. Checks to see if the value is between 4 and 15
    """
    msg = f"{value} is an invalid positive int between 4 and 15"
    try:
        int_value = int(value)
        if int_value < 4 or int_value > 15:
            raise argparse.ArgumentTypeError(msg)
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(msg)


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    # word_length = argparse_custom_types.int_range(4, 16)
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", dest="num_wrong_guesses",
                        type=positive_int,
                        default=DEFAULT_NUM_WRONG_GUESSES,
                        help="Number of wrong guess default: %(default)s")
    parser.add_argument("-s", dest="single_play", action="store_true",
                        help="single play then exit")
    parser.add_argument("-a", dest="auto_play", action="store_true",
                        help="continues game play until 'quit' is entered")
    parser.add_argument("--max", type=int_between_4_and_15,
                        default=DEFAULT_MAX_LENGTH,
                        help="Max word length between 4 and 15")
    parser.add_argument("--min", type=int_between_4_and_15,
                        default=DEFAULT_MIN_LENGTH,
                        help="Min word length between 4 and 15")
    parser.add_argument("-n", "--no_guess_word", dest="guess_word",
                        action="store_false",
                        help="Do not allow guessing of the whole word")
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
        rand_word = random.choice(word_list)
        return_value = play(rand_word,
                            args.num_wrong_guesses,
                            args.no_color,
                            args.guess_word)
        if args.single_play or args.auto_play and return_value == -1:
            break
        elif args.auto_play:
            continue
        else:
            print()
            user_input = input("Would you like to play again? (Yes or no): ")
            if user_input.upper() in ["YES", "Y"]:
                continue
            else:
                break
    return 0


if __name__ == "__main__":
    exit(main)
