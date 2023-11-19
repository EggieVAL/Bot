import os
import shutil

from configparser import ConfigParser
from pathlib import Path

path = 'src/assets/config'
hidden_path = 'src/assets/.config'

def has_required_items(
    *,
    path: str,
    file: str,
    settings: dict[str, list[str]]
) -> ConfigParser:
    """
    Checks if the config file has the required items it needs to function.
    If it is missing an item, then this function will raise an error stating
    the missing requirement.
    
    Returns:
        The config parser for the specified file.
    """
    
    target_file = os.path.join(path, file)
    config = ConfigParser()
    config.read(target_file)
    
    for section in settings:
        if section not in config:
            raise ValueError(f'Missing [{section}] in {file}')
        for key in settings[section]:
            if key not in config[section]:
                raise ValueError(f"Missing '{key}' under [{section}] in {file}")
    
    return config
    
def file_exists(
    *,
    path: str,
    file: str,
    copy_path: str = '',
    copy_file: str | None = None
) -> str:
    """
    Checks if the file exists. If it does not exist, then create it.
    
    Returns:
        The target file.
    """
    
    Path(path).mkdir(parents=True, exist_ok=True)
    target_file = os.path.join(path, file)
    
    if copy_file and not os.path.isfile(target_file):
        copy_file = os.path.join(copy_path, copy_file)
        try: shutil.copy(copy_file, target_file)
        except: pass
    else:
        Path(target_file).touch(exist_ok=True)
    
    return target_file