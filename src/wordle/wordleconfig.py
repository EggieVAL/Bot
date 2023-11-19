import config as cfg
import enchant
import os

cfg_file = 'wordle.cfg'
'The configuration file for a Wordle game.'

cfg.file_exists(
    path = cfg.path,
    file = cfg_file,
    copy_path = cfg.hidden_path,
    copy_file = cfg_file
)

config = cfg.has_required_items(
    path = cfg.path,
    file = cfg_file,
    settings = {
        'DICTIONARY': [
            'Path',
            'FiveLetter',
            'Feudle'
        ],
        'EMOJI': [
            'Path',
            'SquareLetters'
        ],
        'Gamemode.Standard': [
            'Dictionary',
            'MaxAttempts',
            'ValidWordsOnly',
            'Language'
        ],
        'Gamemode.Daily': [
            'Dictionary',
            'MaxAttempts',
            'ValidWordsOnly',
            'Language'
        ],
        'Gamemode.Feudle': [
            'Dictionary',
            'MaxAttempts',
            'ValidWordsOnly',
            'Language'
        ]
    }
)
'The configuration for a Wordle game.'

class DictionaryConfig:
    """
    The dictionary configuration for a Wordle game.
    """
    
    cfg = config['DICTIONARY']
    'The dictionary configuration for a Wordle game.'
    
    @staticmethod
    def get(key: str) -> str:
        """
        Returns the value of the key.
        """
        return DictionaryConfig.cfg[key]
    
    @staticmethod
    def path() -> str:
        """
        Returns the 'Path' key value.
        """
        return DictionaryConfig.cfg['Path']
    
    @staticmethod
    def five_letter() -> str:
        """
        Returns the 'FiveLetter' key value.
        """
        return DictionaryConfig.cfg['FiveLetter']
    
    @staticmethod
    def feudle() -> str:
        """
        Returns the 'Fath' key value.
        """
        return DictionaryConfig.cfg['Feudle']
    
class EmojiConfig:
    """
    The emoji configuration for a Wordle game.
    """
    
    cfg = config['EMOJI']
    'The emoji configuration for a Wordle game.'
    
    @staticmethod
    def get(key: str) -> str:
        """
        Returns the value of the key.
        """
        return EmojiConfig.cfg[key]
    
    @staticmethod
    def path() -> str:
        """
        Returns the 'Path' key value.
        """
        return EmojiConfig.cfg['Path']
    
    @staticmethod
    def square_letters() -> str:
        """
        Returns the 'SquareLetters' key value.
        """
        return EmojiConfig.cfg['SquareLetters']
    
class GamemodeConfig:
    """
    The configuration for a specific Wordle game.
    """
    
    @staticmethod
    def get(mode: str, key: str) -> str:
        """
        Returns the value of the key.
        """
        return config[f'Gamemode.{mode}'][key]
    
    @staticmethod
    def dictionary(mode: str) -> list[str]:
        """
        Returns the 'Dictionary' key value.
        """
        
        dictionary = config[f'Gamemode.{mode}']['Dictionary']
        dictionary = os.path.join(DictionaryConfig.path(), DictionaryConfig.get(dictionary))
        
        with open(dictionary, 'r', encoding='utf-8') as file:
            return file.readlines()
    
    @staticmethod
    def max_attempts(mode: str) -> int:
        """
        Returns the 'MaxAttempts' key value.
        """
        return config[f'Gamemode.{mode}'].getint('MaxAttempts')
    
    @staticmethod
    def valid_words_only(mode: str) -> bool:
        """
        Returns the 'ValidWordsOnly' key value.
        """
        return config[f'Gamemode.{mode}'].getboolean('ValidWordsOnly')
    
    @staticmethod
    def language(mode: str) -> enchant.Dict:
        """
        Returns the 'Language' key value.
        """
        return enchant.Dict(config[f'Gamemode.{mode}']['Language'])