import config as cfg

cfg_file = 'player.cfg'
'The cofiguration file for a player.'

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
            'Path',
            'Template'
        ]
    }
)
'The configuration for a player.'

class DefaultConfig:
    """
    The default configuration for a player.
    """
    
    cfg = config['DEFAULT']
    'The default configuration for a player.'
    
    @staticmethod
    def get(key: str) -> str:
        """
        Returns the value of the key.
        """
        return DefaultConfig.cfg[key]
    
    @staticmethod
    def path() -> str:
        """
        Returns the 'Path' key value.
        """
        return DefaultConfig.cfg['Path']
    
    @staticmethod
    def template() -> str:
        """
        Returns the 'Template' key value.
        """
        return DefaultConfig.cfg['Template']