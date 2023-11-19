from .letter_state import *

class SquareLetter:
    """
    A square letter represents the Wordle square. It has a value (a letter) and a state
    (e.g. black, gray, yellow, green).
    """
    # These are all the Wordle Square emojis
    from ._letter_emoji import (
        blank_square,
        black_squares,
        gray_squares,
        yellow_squares,
        green_squares
    )
    
    def __init__(
        self,
        value: str,
        state: LetterState = LetterState.BLACK
    ) -> None:
        """
        Constructs a square letter with some value and state.
        """
        self.value = value
        self.state = state
        
    def emoji(self) -> str | None:
        """
        Returns the string representation of the emoji of this square letter.
        """
        match self.state:
            case LetterState.BLACK:
                return SquareLetter.black_squares[self.value]
            case LetterState.GRAY:
                return SquareLetter.gray_squares[self.value]
            case LetterState.YELLOW:
                return SquareLetter.yellow_squares[self.value]
            case LetterState.GREEN:
                return SquareLetter.green_squares[self.value]
    
    def __eq__(self, other) -> bool:
        return isinstance(other, SquareLetter) and self.value == other.value and self.state == other.state
    
    def __hash__(self) -> int:
        hash = 13
        hash = (hash * 7) + self.value.__hash__
        hash = (hash * 7) + self.state.__hash__
        return hash
    