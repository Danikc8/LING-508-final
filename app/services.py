from typing import Union, Any
import database.mysql_repo
from model.character import Character
from gtts import gTTS

class Services:

    def __init__(self, char: str):
        self.char = char
        self.repo = database.mysql_repo.MysqlRepository()

    def pronounce(self, filename: str = None) -> str:
        if not filename:
            filename = f"{self.char}.mp3"
        tts = gTTS(text=self.char, lang='zh-CN')
        tts.save(filename)
        return filename

    def fetch(self) -> Union[Character, list[Any]]:
        return self.repo.load_lexical_entries(self.char)