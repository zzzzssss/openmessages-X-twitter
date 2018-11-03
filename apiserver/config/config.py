from configparser import ConfigParser

class Config:
    def __init__(self, filename, section):
        # config file's file name
        self.filename = filename
        # section name in config file
        self.section = section
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.filename)
        # get section, default to postgresql
        config = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                config[param[0]] = param[1]
            self.config = config
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))

    def getConfig(self):
        print self.config
        return self.config
