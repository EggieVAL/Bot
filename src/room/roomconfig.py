import config as cfg

cfg_file = 'room.cfg'
'The configuration file for a room.'

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
            'Private',
            'Invitable',
            'AutoArchiveDuration',
            'SlowmodeDelay'
        ]
    }
)
'The configuration for a room.'

class DefaultConfig:
    """
    The default configuration for a room.
    """
    
    cfg = config['DEFAULT']
    'The default configuration for a room.'
    
    @staticmethod
    def get(key: str) -> str:
        """
        Returns the value of the key.
        """
        return DefaultConfig.cfg[key]
    
    @staticmethod
    def private() -> bool:
        """
        Returns the 'Private' key value.
        """
        return DefaultConfig.cfg.getboolean('Private')
    
    @staticmethod
    def invitable() -> bool:
        """
        Returns the 'Invitable' key value.
        """
        return DefaultConfig.cfg.getboolean('Invitable')
    
    @staticmethod
    def auto_archive_duration() -> int:
        """
        Returns the 'AutoArchiveDuration' key value.
        """
        return DefaultConfig.cfg.getint('AutoArchiveDuration')
    
    @staticmethod
    def slowmode_delay() -> int:
        """
        Returns the 'SlowmodeDelay' key value.
        """
        return DefaultConfig.cfg.getint('SlowmodeDelay')