from unittest import mock

import pytest

import wordguess


def mock_input(*args):
    input_values = list(args)

    def mock_input2(s):
        print(s, end="")
        return input_values.pop(0)

    return mock_input2


def test_load_words(tmpdir):
    test_words = ["TESTING", "PYTHON", "FINISH", "YELLOW", "ORANGE"]
    tf = tmpdir.join("words.txt")
    tf.write("\n".join(test_words))
    with mock.patch.object(wordguess, "WORD_LIST_FILE", tf.strpath):
        result = wordguess.load_words()

    assert result == test_words


def test_load_words_file_not_found(tmpdir, capsys):
    tf = tmpdir.join("words.txt")
    with mock.patch.object(wordguess, "WORD_LIST_FILE", tf.strpath):
        with pytest.raises(wordguess.WordGuessError):
            wordguess.load_words()
            captured = capsys.readouterr().err
            assert "Error words.txt file not found" in captured


def test_random_word():
    with mock.patch.object(wordguess, "choice", return_value="COMMIT"):
        result = wordguess.random_word(["CHOICE", "ENTERPRISE", "COMMIT"])
        assert result == "COMMIT"


def test_setup_word():
    test_word = "MISSION"
    result = wordguess.setup_word(test_word)
    assert result == (["M", "I", "S", "S", "I", "O", "N"],
                      ["_", "_", "_", "_", "_", "_", "_"])


def test_display_start(capsys):
    num_wrong_guesses = wordguess.DEFAULT_NUM_WRONG_GUESSES
    expected_capture = f"""Word Guess

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

_ _ _ _ _ _

Wrong Guesses 1 out of {num_wrong_guesses}
"""
    l = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    wordguess.display(l, ["_", "_", "_", "_", "_", "_"], 1, num_wrong_guesses)
    captured = capsys.readouterr().out
    assert captured == expected_capture


def test_play_quit(capsys):
    wordguess.input = mock_input("quit")
    wordguess.play("LETTER", 6)
    captured = capsys.readouterr().out
    assert "quitting" in captured


def test_play_win(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("L", "T", "E", "R")
        wordguess.play("LETTER", 6)
        captured = capsys.readouterr().out
        assert "You Won! You got the word" in captured


def test_play_wrong_guess(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("L", "T", "W", "quit")
        wordguess.play("LETTER", 6)
        captured = capsys.readouterr().out
        assert "Letter W not in the word" in captured


def test_play_out_of_guesses(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("K", "i", "l", "a", "s", "W", "z", "U")
        wordguess.play("LETTER", 6)
        captured = capsys.readouterr().out
        assert "Out of guesses\nThe word was  LETTER" in captured


def test_play_letter_already_guessed(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("s", "t", "a", "R", "t", "quit")
        wordguess.play("LETTER", 6)
        captured = capsys.readouterr().out
        assert "Letter already been picked try again" in captured


@pytest.mark.parametrize("test_input", [
    "1", "90909", "test", "3R", "?", "#", " ", "R9",
])
def test_play_invalid_input(capsys, test_input):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("s", test_input, "quit")
        wordguess.play("LETTER", 6)
        captured = capsys.readouterr().out
        assert "Invalid input please try again" in captured


@pytest.mark.parametrize("test_value, expected_result", [
    ([], wordguess.DEFAULT_NUM_WRONG_GUESSES),
    (["-W", "10"], 10),
])
def test_argument_parser_num_wrong_guess(test_value, expected_result):
    result = wordguess.argument_parser(test_value)
    assert result.num_wrong_guesses == expected_result

