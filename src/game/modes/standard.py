import enchant
import random
import wordle

from ..game import Game, player

class Standard(Game):
    """
    This class represents a standard Wordle game.
    """
    
    def __init__(
        self,
        *,
        player: player.Player,
        language: enchant.Dict | None = None
    ) -> None:
        super().__init__(
            hidden_word = Standard.random_word(),
            player = player,
            mode = 'Standard',
            language = language
        )
        
    @staticmethod
    def random_word() -> str:
        """
        Generates a random word.
        """
        return random.choice(wordle.GamemodeConfig.dictionary('Standard'))
    
    def rules(self) -> str:
        """
        The rules of a standard Wordle game.
        """
        length = str(len(self.wordle.hidden_word))
        a = 'an' if length == '10' or length[0] == '1' or length[0] == '8' else 'a'
        
        return f"""
                **How to play?**
                You have {self.wordle.max_attempts} attempts to guess the word.

                **Green** indicates that the letter is in the correct spot.
                **Yellow** indicates that the letter is in the wrong spot.
                **Gray** indicates that the letter is not in the word.

                Type {a} {length}-letter word to start playing.
                """