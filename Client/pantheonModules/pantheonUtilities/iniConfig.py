import os

class AteneaConfig():

    def __init__(self, iniPath):
        try:
            import configparser
        except Exception as e:
            print ("Cannot import ConfigParser to parse INI files. " + str(e))
            return

        if os.path.isfile(iniPath):
            self.config = configparser.ConfigParser()
            self.config.read(iniPath)
        else:
            self.config = None

    def getMap(self,section):
        if self.config is not None:
            dict1 = {}
            options = self.config.options(section)
            for option in options:
                try:
                    dict1[option] = self.config.get(section, option)
                    if dict1[option] == -1:
                        log("skip: %s" % option)
                except:
                    log("exception on %s!" % option)
                    dict1[option] = None
            return dict1
        else:
            return None