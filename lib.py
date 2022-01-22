from typing import Dict, Iterable, Tuple, List

from tqdm import tqdm
import collections
import dataclasses
import functools


@dataclasses.dataclass(frozen=True)
class Position:
  index: int
  place: bool
  exists: bool


@dataclasses.dataclass(frozen=True)
class Clue:
  letter: str
  positions: Tuple[Position]


@functools.cache
def get_letter_indices(word: str) -> Dict[str, Tuple[int]]:
  letter_indices = collections.defaultdict(tuple)
  for letter in set(word):
    letter_indices[letter] = tuple(index for index in range(5) if word[index] == letter)
  return letter_indices


def get_clues(guess: str, answer: str) -> Tuple[Clue]:
  return tuple(
    get_clue(answer, letter, indices)
    for letter, indices in sorted(get_letter_indices(guess).items(), key=lambda x: x[1])
  )


@functools.cache
def get_clue(answer: str, letter: str, indices: Tuple[int]) -> Clue:
  placed_count = sum(1 for index in indices if answer[index] == letter)
  misplaced_count = sum(1 for actual_letter in answer if actual_letter == letter) - placed_count

  positions = []
  for index in indices:
    if answer[index] == letter:
      positions.append(Position(index, True, True))
    elif misplaced_count > 0:
      misplaced_count -= 1
      positions.append(Position(index, False, True))
    else:
      positions.append(Position(index, False, False))

  return Clue(letter, tuple(positions))


def matches_clues(word: str, clues: Iterable[Clue]) -> bool:
  for clue in clues:
    indices = tuple(position.index for position in clue.positions)
    actual_clue = get_clue(word, clue.letter, indices)
    if actual_clue != clue:
      return False
  return True

