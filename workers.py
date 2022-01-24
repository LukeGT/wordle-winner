from turtle import pos
from typing import *

from tqdm import tqdm
import multiprocessing

import lib
import word_bank


def process(args):
  guess, possibilities = args
  return word_bank.get_worst_case(guess, possibilities), guess


def play(clues: Tuple[lib.Clue], words: List[str], hard_mode=True) -> str:
  possibilities = list(word_bank.get_possibilities(clues, words))
  possibility_set = set(possibilities)

  # if len(possibilities) < 20:
  #   print(possibilities)

  if len(possibilities) == 1:
    return possibilities[0], 1

  min_poss = float('inf')
  best_guess = None

  word_list = possibilities + (
    [word for word in word_bank.answers if word not in possibility_set]
    if not hard_mode else []
  )
  args = [(word, possibilities) for word in word_list]

  with multiprocessing.Pool() as pool:
    for max_poss, guess in tqdm(pool.imap_unordered(process, args), total=len(args)):
      if max_poss < min_poss or max_poss == min_poss and guess in possibility_set:
        min_poss = max_poss
        best_guess = guess
      if min_poss == 1:
        break

  return best_guess, min_poss

