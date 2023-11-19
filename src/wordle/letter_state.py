from enum import Enum

class LetterState(Enum):
    """
    A letter state is a numerical representation of the states a Wordle square can be.
    - A black square means the letter has not been used.
    - A gray square means the letter is not in the word.
    - A yellow square means the letter is in the word but in the wrong place.
    - A green square means the letter is in the word and in the right place.
    """
    BLACK = 0
    'Black means the letter has not been used.'
    GRAY = 1
    'Gray means the letter is not in the word.'
    YELLOW = 2
    'Yellow means the letter is in the word but in the wrong place.'
    GREEN = 3
    'Green means the letter is in the word and in the right place.'