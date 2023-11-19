import config as cfg
import os

from dotenv import load_dotenv

cfg_file = 'bot.cfg'
'The configuration file for BOTTLE.'

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
        'DEFAULT': [
            'EnableCommandPrefix',
            'CommandPrefix'
        ],
        'TOKEN': [
            'Path',
            'File',
            'Key'
        ]
    }
)
'The configuration for BOTTLE.'

class DefaultConfig:
    """
    The default configuration for BOTTLE.
    """
    
    cfg = config['DEFAULT']
    'The default configuration for BOTTLE.'
    
    @staticmethod
    def get(key: str) -> str:
        """
        Returns the value of the key.
        """
        return DefaultConfig.cfg[key]
    
    @staticmethod
    def enable_command_prefix() -> bool:
        """
        Returns the 'EnableCommandPrefix' key value.
        """
        return DefaultConfig.cfg.getboolean('EnableCommandPrefix')
    
    @staticmethod
    def command_prefix() -> str:
        """
        Returns the 'CommandPrefix' key value.
        """
        return DefaultConfig.cfg['CommandPrefix']
    
class TokenConfig:
    """
    The token configuration for BOTTLE.
    """
    
    cfg = config['TOKEN']
    'The token configuration for BOTTLE.'
    
    @staticmethod
    def get(key: str) -> str:
        """
        Returns the value of the key.
        """
        return TokenConfig.cfg[key]
    
    @staticmethod
    def path() -> str:
        """
        Returns the 'Path' key value.
        """
        return TokenConfig.cfg['Path']
    
    @staticmethod
    def file() -> str:
        """
        Returns the 'File' key value.
        """
        return TokenConfig.cfg['File']
    
    @staticmethod
    def key() -> str:
        """
        Returns the 'Key' key value.
        """
        return TokenConfig.cfg['Key']

load_dotenv(os.path.join(TokenConfig.path(), TokenConfig.file()))
TOKEN = os.getenv(TokenConfig.key())
'The token key for BOTTLE.'