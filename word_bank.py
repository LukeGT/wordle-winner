from typing import *

import functools

import lib


with open('answers.txt', 'r') as file:
  answers = [line.strip() for line in file]
with open('non-answers.txt', 'r') as file:
  non_answers = [line.strip() for line in file]

words = sorted(answers + non_answers)


@functools.cache
def get_possibilities_for_words(clues: Tuple[lib.Clue]) -> List[str]:
  global words
  return [ word for word in words if lib.matches_clues(word, clues) ]


def get_possibilities(clues: Tuple[lib.Clue], words: List[str]) -> List[str]:
  valid = set(words)
  return [ word for word in get_possibilities_for_words(clues) if word in valid ]


def get_possibilities_num(clues: Tuple[lib.Clue], words: List[str]) -> int:
  return len(get_possibilities(clues, words))


def get_worst_case(guess: str, words: List[str]) -> Tuple[int, str]:
  return max(
    get_possibilities_num(lib.get_clues(guess, word), words)
    for word in words
  )