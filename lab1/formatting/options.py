import configparser
from pathlib import Path

configs_folder = Path("option_templates/")

class Options:
    """Class to keep formating options"""
    def __init__(self, configs_file):
        """Configs_file: filename of the template (without .ini)"""
        config = configparser.ConfigParser(delimiters=("@",))   #change delimiter because = and : needed in text
        config.read_file(open(configs_folder / (configs_file + ".ini"), "r"))

        self.config = config

    def __getitem__(self, index):
        return self.config[index]