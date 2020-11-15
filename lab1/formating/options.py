import configparser
import sys

configs_folder = "..\\option_templates\\"

class Options:
    def __init__(self, configs_file):
        config = configparser.ConfigParser()
        config.read(configs_folder + configs_file + ".ini")
        print(config.sections())

        self.config = config

op = Options("default")