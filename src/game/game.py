import discord
import enchant
import graphics
import player
import time
import wordle

from abc import abstractmethod

class Game:
    """
    This is an extension to the Wordle game. It allows for the creation of Wordle variants.
    There can only be one player playing a game instance. These games are timed to elevate
    a competitive environment.
    
    The game class also adds extra functionality that the Wordle class does not offer. And
    that is explicitly stating whether the player has won, lost, or forfeited the game.
    """
    
    def __init__(
        self,
        *,
        hidden_word: str,
        player: player.Player,
        mode: str,
        language: enchant.Dict | None = None
    ) -> None:
        self.player = player
        'The player who is playing this game.'
        self.mode = mode
        'The mode of this game.'
        
        self.wordle = wordle.Wordle(
            hidden_word = hidden_word,
            max_attempts = wordle.GamemodeConfig.max_attempts(mode),
            language = wordle.GamemodeConfig.language(mode) if language is None and wordle.GamemodeConfig.valid_words_only(mode) else language
        )
        
        self.start_time: float | None = None
        'The time the game has started.'
        self.end_time: float | None = None
        'The time the game has ended.'
        
        self.game_embed = self.create_game_embed()
        'The embed for the Wordle game.'
        self.embeds = [self.game_embed]
        'All embeds for this game.'
        self.message: discord.Message | None = None
        'The message the embeds are displayed in.'
        
        self.player.in_game = self
    
    @abstractmethod
    def rules(self) -> str:
        """
        These are the rules for this Wordle game. Different types of Wordle games may have
        different rules.
        """
        pass
    
    async def display_rules(self) -> None:
        """
        Displays the rules in an embed, and sends it to Discord.
        """
        await graphics.display_msg_embed(
            obj = self.player.room,
            title = self.mode,
            description = self.rules(),
            color = discord.Color.blurple()
        )
        
    async def run(self, interaction: discord.Interaction) -> None:
        """
        Runs the game until the player has ran out of attempts, has guess the word, or has
        forfeited.
        """
        print(f'{self.player.user} started a Wordle game (mode:{self.mode}, hidden_word={self.wordle.hidden_word})')
        self.start_time = time.time()
        
        await self.display_rules()
        while not self.wordle.is_terminated():
            guess = await self.wait_for_guess(interaction)
            await self.make_guess(guess)

        if self.player.in_game == self:
            self.player.in_game = None

        if not self.has_forfeited():
            self.update_stats()

    async def wait_for_guess(self, interaction: discord.Interaction) -> str:
        """
        Waits for a guess from the player. After they have made a guess, return the guess
        in the form of a string.
        """
        def check_guess(message: discord.Message) -> discord.Message | None:
            if self.player.room is None:
                return
            if message.channel.id == self.player.room.thread.id and message.author == self.player.user:
                return message
            
        guess: discord.Message = await interaction.client.wait_for('message', check=check_guess)
        if not self.wordle.is_terminated():
            await guess.delete()
            return guess.content

    async def make_guess(self, guess: str) -> None:
        """
        Simulates the standard Wordle game by making a guess. Warns the player if they
        provided with a bad guess. This does not use up an attempt.
        """
        try:
            squares = self.wordle.make_guess(guess)
            if squares is not None:
                await self.update_game_embed(squares)
                if self.message is None:
                    self.message = await self.player.room.thread.send(embeds=self.embeds)
                else:
                    self.message = await self.message.edit(embeds=self.embeds)
        except wordle.InvalidGuess as e:
            await graphics.display_msg_embed(
                obj = self.player.room,
                title = 'Invalid Guess',
                description = e.message,
                color = discord.Color.yellow()
            )
    
    async def update_game_embed(self, squares: list[wordle.SquareLetter]) -> None:
        """
        Updates the embed of the Wordle game. This is called every time a guess is made.
        """
        emojis = ''.join(letter.emoji() for letter in squares)
        self.game_embed.set_field_at(
            index = self.wordle.attempt_number - 1,
            name = '',
            value = emojis,
            inline = False
        )
        
        if self.wordle.is_terminated():
            self.game_embed.color = discord.Color.green() if self.has_won() else discord.Color.red()
            [self.game_embed.remove_field(self.wordle.max_attempts) for _ in range(3)]
        else:
            keyboard = self.build_keyboard()
            for i in range(3):
                self.game_embed.set_field_at(
                    index = self.wordle.max_attempts + i,
                    name = '',
                    value = keyboard[i],
                    inline = False
                )
        
    def update_stats(self) -> None:
        """
        Updates the player's statistics.
        """
        stats = self.player.data['stats'][self.mode]
        
        if self.has_won():
            stats['wins'] += 1
            self.player.update_fastest_guess(self.mode, self.elapsed_time())
        elif self.has_lost():
            stats['losses'] += 1
        elif self.has_forfeited():
            stats['forfeits'] += 1
            
        stats['total_guesses'] += len(self.wordle.history)
        for word in self.wordle.history:
            for letter in word:
                match letter.state:
                    case wordle.LetterState.GRAY:
                        stats['gray_tiles'] += 1
                    case wordle.LetterState.YELLOW:
                        stats['yellow_tiles'] += 1
                    case wordle.LetterState.GREEN:
                        stats['green_tiles'] += 1
        
        self.player.update_data_file()
    
    def build_keyboard(self) -> list[str]:
        """
        Builds a keyboard representation of all the letters used and their states. This
        keyboard shows the player what letters they should use, letters they should try,
        to use, and letters they should avoid.
        """
        qwerty_keyboard = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m"]
        ]
        return [''.join(self.wordle.letters_used[letter].emoji() for letter in keys) for keys in qwerty_keyboard]
    
    def create_game_embed(self, color: discord.Color = discord.Color.yellow()) -> discord.Embed:
        """
        Creates a blank game state of this Wordle game. This is updated after every guess
        made.
        """
        embed = discord.Embed(title=self.mode, color=color)
        embed.set_author(
            name = self.player.user.display_name,
            icon_url = self.player.user.avatar.url
        )
        
        blank_word = wordle.SquareLetter.blank_square * len(self.wordle.hidden_word)
        keyboard = self.build_keyboard()
        
        [embed.add_field(name='', value=blank_word, inline=False) for _ in range(self.wordle.max_attempts)]
        [embed.add_field(name='', value=keys, inline=False) for keys in keyboard]
        return embed
    
    def elapsed_time(self) -> float:
        """
        The time it has elapsed since the start of the game. This is usually used to measure
        the time it took to end the game. However, if the game has not ended yet, it will
        return the time it has been alive.
        """
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time
    
    def terminate(self) -> None:
        """
        Forcefully terminates the game.
        """
        self.wordle.terminate()
        self.update_stats()
        self.player.in_game = None
        
    def has_won(self) -> bool:
        """
        Returns whether the player has won.
        """
        return self.wordle.has_guessed_word
    
    def has_lost(self) -> bool:
        """
        Returns whether the player has lost.
        """
        return self.wordle.has_guessed_word is False and self.wordle.attempt_number == self.wordle.max_attempts
    
    def has_forfeited(self) -> bool:
        """
        Returns whether the player has forfeited.
        """
        return self.wordle.has_guessed_word is False and self.wordle.attempt_number < self.wordle.max_attempts