import discord
import enchant
import random
import requests
import wordle

from ..game import Game, player

class Feudle(Game):
    """
    This class represents a Feudle game.
    """
    
    def __init__(
        self,
        *,
        player: player.Player,
        language: enchant.Dict | None = None
    ) -> None:
        hidden_word = Feudle.random_word()
        self.phrase = Feudle.random_phrase(hidden_word)
        'The phrase this game is using.'
        self.phrase_embed = self.build_phrase_embed()
        'The phrase in an embed.'
        
        super().__init__(
            hidden_word = hidden_word,
            player = player,
            mode = 'Feudle',
            language = language
        )
        
    @staticmethod
    def random_word() -> str:
        """
        Generates a random word.
        """
        return random.choice(wordle.GamemodeConfig.dictionary('Feudle'))
    
    def random_phrase(word: str) -> str | None:
        """
        Generates a random phrase for a game.
        """
        word = word.strip().lower()
        try:
            url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
            meanings = requests.get(url).json()[0]['meanings']
            
            phrases = []
            for meaning in meanings:
                for definition in meaning['definitions']:
                    if 'example' not in definition:
                        continue
                    phrase = f" {definition['example']}"
                    index = phrase.find(f' {word}')
                    if index == -1:
                        continue
                    phrase = phrase[1:index+1] + (wordle.SquareLetter.blank_square * len(word)) + phrase[index + len(word) + 1:]
                    phrases.append(phrase)
            if phrases:
                return random.choice(phrases)
        except: pass
    
    def build_phrase_embed(self) -> discord.Embed:
        """
        Creates an embed that contains the phrase of a game.
        """
        return discord.Embed(
            title = '',
            description = self.phrase,
            color = discord.Color.yellow()
        )
    
    def rules(self) -> str:
        """
        The rules of a Feudle game.
        """
        length = str(len(self.wordle.hidden_word))
        a = 'an' if length == '10' or length[0] == '1' or length[0] == '8' else 'a'
        
        return f"""
                **How to play?**
                You have {self.wordle.max_attempts} attempts to guess the word.

                **Green** indicates that the letter is in the correct spot.
                **Yellow** indicates that the letter is in the wrong spot.
                **Gray** indicates that the letter is not in the word.
                
                *{self.phrase}*
                
                Type {a} {length}-letter word to start playing.
                """