from unittest import mock

import pytest

import wordguess


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
