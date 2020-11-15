import configparser

configs_folder = "option_templates\\"

class Options:
    """Class to keep formating options"""
    def __init__(self, configs_file):
        """Configs_file: filename of the template (without .ini)"""
        config = configparser.ConfigParser()
        config.read(configs_folder + configs_file + ".ini")
        print(config.sections())

        self.config = config