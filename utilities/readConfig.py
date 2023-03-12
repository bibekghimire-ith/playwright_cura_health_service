from configparser import RawConfigParser, ConfigParser

config = ConfigParser()
config.read("./Configurations/config.conf")

class ReadConfig:
    @staticmethod
    def getApplicationURL() -> str:
        url = config.get("common fields", "baseURL")
        return url
    
    @staticmethod
    def getUsername() -> str:
        username = config.get("common fields", "username")
        return username
    
    @staticmethod
    def getPassword() -> str:
        password = config.get("common fields", "password")
        return password