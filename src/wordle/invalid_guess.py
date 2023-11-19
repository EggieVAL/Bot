class InvalidGuess(Exception):
    """
    An invalid guess is raised when a player submits an invalid word for a guess.
    
    A few things that can or will invoke an InvalidGuess exception are:
    - The guess is too long or short.
    - The guess is not a word in a particular language.
    - The guess contains special characters.
    """
    def __init__(
        self,
        guess: str,
        message: str
    ) -> None:
        super().__init__(message)
        self.guess = guess
        'The guess that invoked the exception.'
        self.message = message
        'The reason the guess raised the exception.'