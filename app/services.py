from typing import Union, Any
import database.mysql_repo
from model.character import Character

class Services:

    def __init__(self, char: str):
        self.char = char
        self.repo = database.mysql_repo.MysqlRepository()

    def fetch(self) -> Union[Character, list[Any]]:
        return self.repo.load_lexical_entries(self.char)