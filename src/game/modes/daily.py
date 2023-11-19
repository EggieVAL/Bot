import enchant
import random
import time
import wordle

from ..game import Game, player

class Daily(Game):
    """
    This class represents the daily Wordle challenge.
    """
    
    def __init__(
        self,
        *,
        player: player.Player,
        language: enchant.Dict | None = None
    ) -> None:
        super().__init__(
            hidden_word = Daily.random_word(),
            player = player,
            mode = 'Daily',
            language = language
        )
        
    @staticmethod
    def random_word() -> str:
        """
        Generates a random word.
        """
        seed = time.strftime('%d/%m/%Y')
        rand = random.Random(seed)
        return rand.choice(wordle.GamemodeConfig.dictionary('Daily'))
        
    def rules(self) -> str:
        """
        The rules of the daily Wordle challenge.
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