from unittest import mock

import pytest

from wordguess import wordguess


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
        result = wordguess.load_words(4, 15)

    assert result == test_words


def test_load_words_file_not_found(tmpdir, capsys):
    tf = tmpdir.join("words.txt")
    with mock.patch.object(wordguess, "WORD_LIST_FILE", tf.strpath):
        with pytest.raises(wordguess.WordGuessError):
            wordguess.load_words(4, 15)
            captured = capsys.readouterr().err
            assert "Error words.txt file not found" in captured


@pytest.mark.parametrize("test_length, expected_result", [
    (10, ["TEST", "FISHER", "PRODUCE", "INSTRUMENT", "LIGHT", "SHIELD"]),
    (8, ["TEST", "FISHER", "PRODUCE", "LIGHT", "SHIELD"]),
])
def test_load_words_max_length(tmpdir, test_length, expected_result):
    test_words = ["TEST", "FISHER", "PRODUCE", "INSTRUMENT", "TEMPERATURE",
                  "CONSTRUCTION", "SUBSCRIPTIONS", "LIGHT", "SHIELD",
                  "IDENTIFICATION"]
    tf = tmpdir.join("words.txt")
    tf.write("\n".join(test_words))
    with mock.patch.object(wordguess, "WORD_LIST_FILE", tf.strpath):
        result = wordguess.load_words(4, test_length)
    assert result == expected_result


@pytest.mark.parametrize("test_length, expected_result", [
    (10, ["INSTRUMENT", "TEMPERATURE", "CONSTRUCTION", "SUBSCRIPTIONS",
          "IDENTIFICATION"]),
    (12, ["CONSTRUCTION", "SUBSCRIPTIONS", "IDENTIFICATION"]),
])
def test_load_words_min_length(tmpdir, test_length, expected_result):
    test_words = ["TEST", "FISHER", "PRODUCE", "INSTRUMENT", "TEMPERATURE",
                  "CONSTRUCTION", "SUBSCRIPTIONS", "LIGHT", "SHIELD",
                  "IDENTIFICATION"]
    tf = tmpdir.join("words.txt")
    tf.write("\n".join(test_words))
    with mock.patch.object(wordguess, "WORD_LIST_FILE", tf.strpath):
        result = wordguess.load_words(test_length, 15)
    assert result == expected_result


def test_load_words_min_max_length(tmpdir):
    test_words = ["TEST", "FISHER", "PRODUCE", "INSTRUMENT", "TEMPERATURE",
                  "CONSTRUCTION", "SUBSCRIPTIONS", "LIGHT", "SHIELD",
                  "IDENTIFICATION"]
    tf = tmpdir.join("words.txt")
    tf.write("\n".join(test_words))
    with mock.patch.object(wordguess, "WORD_LIST_FILE", tf.strpath):
        result = wordguess.load_words(10, 10)
    assert result == ["INSTRUMENT"]


def test_random_word():
    with mock.patch.object(wordguess, "choice", return_value="COMMIT"):
        result = wordguess.random_word(["CHOICE", "ENTERPRISE", "COMMIT"])
        assert result == "COMMIT"


def test_setup_word():
    test_word = "MISSION"
    result = wordguess.setup_word(test_word)
    assert result == (["M", "I", "S", "S", "I", "O", "N"],
                      ["_", "_", "_", "_", "_", "_", "_"])


def test_display_start_no_color(capsys):
    num_wrong_guesses = wordguess.DEFAULT_NUM_WRONG_GUESSES
    expected_capture = f"""Word Guess

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

_ _ _ _ _ _

Wrong Guesses 1 out of {num_wrong_guesses}
"""
    l = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    b = ["_", "_", "_", "_", "_", "_"]
    wordguess.display(l, b, 1, num_wrong_guesses, False)
    captured = capsys.readouterr().out
    assert captured == expected_capture


def test_display_start_color(capsys):
    num_wrong_guesses = wordguess.DEFAULT_NUM_WRONG_GUESSES
    expected_capture = f"""\033[1;37;40mWord Guess\033[m

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

_ _ _ _ _ _

Wrong Guesses 1 out of {num_wrong_guesses}
"""
    l = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    b = ["_", "_", "_", "_", "_", "_"]
    wordguess.display(l, b, 1, num_wrong_guesses, True)
    captured = capsys.readouterr().out
    assert captured == expected_capture


@pytest.mark.parametrize("color_mode", [True, False])
def test_play_quit(capsys, color_mode):
    wordguess.input = mock_input("quit")
    wordguess.play("LETTER", 6, color_mode)
    captured = capsys.readouterr().out
    assert "quitting" in captured


def test_play_win_no_color(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("L", "T", "E", "R")
        wordguess.play("LETTER", 6, False)
        captured = capsys.readouterr().out
        assert "You Won! You got the word" in captured


def test_play_win_color(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("L", "T", "E", "R")
        wordguess.play("LETTER", 6, True)
        captured = capsys.readouterr().out
        assert "\033[1;32mYou Won! You got the word\033[m" in captured


def test_play_wrong_guess(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("L", "T", "W", "quit")
        wordguess.play("LETTER", 6, False)
        captured = capsys.readouterr().out
        assert "Letter W not in the word" in captured


def test_play_out_of_guesses_no_color(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("K", "i", "l", "a", "s", "W", "z", "U")
        wordguess.play("LETTER", 6, False)
        captured = capsys.readouterr().out
        assert "Out of guesses\nThe word was  LETTER" in captured


def test_play_out_of_guesses_color(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("K", "i", "l", "a", "s", "W", "z", "U")
        wordguess.play("LETTER", 6, True)
        captured = capsys.readouterr().out
        expected = "\033[1;31mOut of guesses\033[m\nThe word was  LETTER"
        assert expected in captured


def test_play_letter_already_guessed(capsys):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("s", "t", "a", "R", "t", "quit")
        wordguess.play("LETTER", 6, False)
        captured = capsys.readouterr().out
        assert "Letter already been picked try again" in captured


@pytest.mark.parametrize("test_input", [
    "1", "90909", "test", "3R", "?", "#", " ", "R9",
])
def test_play_invalid_input(capsys, test_input):
    with mock.patch.object(wordguess, "SLEEP_TIME", 0):
        wordguess.input = mock_input("s", test_input, "quit")
        wordguess.play("LETTER", 6, False)
        captured = capsys.readouterr().out
        assert "Invalid input please try again" in captured


@pytest.mark.parametrize("test_value, expected_result", [
    ([], wordguess.DEFAULT_NUM_WRONG_GUESSES),
    (["-W", "10"], 10),
])
def test_argument_parser_num_wrong_guess(test_value, expected_result):
    result = wordguess.argument_parser(test_value)
    assert result.num_wrong_guesses == expected_result


@pytest.mark.parametrize("test_length, expected_result", [
    ("10", 10), ("15", 15), ("4", 4), ("8", 8)
])
def test_argument_parser_max_word_length(test_length, expected_result):
    result = wordguess.argument_parser(["--max", test_length])
    assert result.max == expected_result


@pytest.mark.parametrize("test_length", [
    "-20", "-1", "0", "1", "3", "16", "200",
    "test", "f5", "8.8",
])
def test_argument_parser_max_word_length_error(test_length):
    with pytest.raises(SystemExit):
        wordguess.argument_parser(["--max", test_length])


@pytest.mark.parametrize("test_length, expected_result", [
    ("10", 10), ("15", 15), ("4", 4), ("8", 8)
])
def test_argument_parser_min_word_length(test_length, expected_result):
    result = wordguess.argument_parser(["--min", test_length])
    assert result.min == expected_result


@pytest.mark.parametrize("test_length", [
    "-20", "-1", "0", "1", "3", "16", "200",
    "test", "f5", "8.8",
])
def test_argument_parser_min_word_length_error(test_length):
    with pytest.raises(SystemExit):
        wordguess.argument_parser(["--min", test_length])


@pytest.mark.parametrize("test_input, expected_result", [
    ([], True), (["--no_color"], False),
])
def test_argument_parser_no_color(test_input, expected_result):
    result = wordguess.argument_parser(test_input)
    assert result.no_color == expected_result


def test_display_version(capsys):
    with pytest.raises(SystemExit):
        wordguess.argument_parser(["--version"])
    captured = capsys.readouterr().out
    assert f"{wordguess.version}\n" == captured


def test_main_min_max_invalid(capsys):
    result = wordguess.main(["--min", "8", "--max", "6"])
    captured = capsys.readouterr().out
    assert result == 1
    assert "Error min can't be larger than max" in captured

