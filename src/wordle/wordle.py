import enchant

from .invalid_guess import *
from .square_letter import *
from typing import List

class Wordle:
    """
    The Wordle class simulates a Wordle game.
    
    Making a guess will use an attempt, and running out of attempts will end the game. To
    win, you need to guess the word before you run out of attempts.
    
    The class will keep track of some information and states important to a Wordle game:
    - The current attempt number.
    - The remaining attempts left.
    - Whether the word has been guessed.
    - Whether the game has been terminated.
    - The letters that have been used and their color states.
    - The history of guesses made.
    """
    def __init__(
        self,
        *,
        hidden_word: str,
        max_attempts: int,
        language: enchant.Dict | None = None
    ) -> None:
        """
        Constructs a Wordle game. To win this game, you need to guess the hidden word.
        You have a certain number of attempts to do so before the game ends.
        """
        self.hidden_word = hidden_word.strip().lower()
        self.max_attempts = max_attempts
        self.language = language
        
        self.attempt_number: int = 0
        self.has_guessed_word: bool | None = None
        self.letters_used: dict[str, SquareLetter] = dict()
        self.history: List[List[SquareLetter]] = list()
        
        for i in range(97, 123):
            self.letters_used[chr(i)] = SquareLetter(chr(i))
    
    def remaining_attempts(self) -> int:
        """
        Returns the remaining attempts left this game allows.
        """
        return self.max_attempts - self.attempt_number
    
    def is_terminated(self) -> bool:
        """
        Returns whether the game has been terminated. A terminated game is when the game ends
        naturally by guessing the word or by using up all your attempts. The game can also
        be terminated forcefully, which is considered as forfeiting.
        """
        return self.has_guessed_word is not None
    
    def terminate(self) -> None:
        """
        Terminates the game. A terminated game is when the game ends naturally by guessing the
        word or by using up all your attempts. The game can also be terminated forcefully,
        which is considered as forfeiting.
        """
        self.has_guessed_word = False if self.has_guessed_word is None else self.has_guessed_word
        
    def make_guess(self, guess: str) -> list[SquareLetter] | None:
        """
        Simulates a Wordle game by making a guess.
        
        An attempt will only be used if the guess passes a few checks:
        - The guess is the same length as the hidden word.
        - The guess does not contain any special characters.
        - The guess is a valid word in some language, if that language was specified.
        """
        if self.is_terminated() or guess is None:
            return None
        
        guess = guess.strip().lower()
        
        if len(guess) > len(self.hidden_word):
            raise InvalidGuess(guess, 'Guess is too long')
        if len(guess) < len(self.hidden_word):
            raise InvalidGuess(guess, 'Guess is too short')
        if not guess.isalpha():
            raise InvalidGuess(guess, 'Guess contains special characters')
        if not (self.language is None or self.language.check(guess) or guess == self.hidden_word):
            raise InvalidGuess(guess, f'Guess is not a word in the {self.language.tag} dictionary')
        
        return self.__make_guess(guess)
    
    def __make_guess(self, guess: str) -> list[SquareLetter]:
        squares = self.__color_code_guess(guess)
        self.history.append(squares)
        self.__update_letters_used(squares)
        self.__use_attempt()
        return squares
    
    def __color_code_guess(self, guess: str) -> list[SquareLetter]:
        if guess == self.hidden_word:
            self.has_guessed_word = True
            self.terminate()
            return [SquareLetter(letter, LetterState.GREEN) for letter in guess]
        
        squares = [SquareLetter(letter, LetterState.GRAY) for letter in guess]
        remaining = list(self.hidden_word)
        possible_yellows: List[tuple[str, int]] = list()
        removed = 0
        
        for guess_letter, hidden_letter, index in zip(guess, self.hidden_word, range(len(guess))):
            if guess_letter == hidden_letter:
                squares[index].state = LetterState.GREEN
                remaining.pop(index - removed)
                removed += 1
            elif guess_letter in remaining:
                possible_yellows.append((guess_letter, index))
        
        for letter, index in possible_yellows:
            try:
                found = remaining.index(letter)
                squares[index].state = LetterState.YELLOW
                remaining.pop(found)
            except: continue
        return squares
    
    def __update_letters_used(self, squares: list[SquareLetter]) -> None:
        for square in squares:
            letter = self.letters_used[square.value]
            if square.state.value > letter.state.value:
                letter.state = square.state
                
    def __use_attempt(self):
        self.attempt_number += 1
        if self.attempt_number == self.max_attempts:
            self.terminate()