from dotenv import load_dotenv
from os import getenv

class Service:

    def __init__(self, api_app_keyname: str = None, api_key_keyname: str = None) -> None:
        self.app_id = self.load_env(api_app_keyname) 
        self.app_key = self.load_env(api_key_keyname)

    def load_env(self, key: str) -> str:
        load_dotenv(verbose=True)
        return getenv(key)