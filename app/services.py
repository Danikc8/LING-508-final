from typing import Union, Any

import database.mysql_repo
from model.character import Character
from model.enumerations import PartOfSpeech
from model.lexical_entry import LexicalEntry
from model.phonological_components import PhonologicalComponent
from gtts import gTTS
import pycantonese
from bs4 import BeautifulSoup
import re

hkcancor = pycantonese.hkcancor()
all_words = hkcancor.words()
ALL_CHARS = set(char for word in all_words for char in word)

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
        entries = self.repo.load_lexical_entries(self.char)
        if entries:
            print("Retrieved from DB")
            return entries

        print("Fetching from PyCantonese...")
        corpus = pycantonese.parse_text(self.char)
        lex_entries = []

        for utterance in corpus.utterances():
            for token in utterance.tokens:
                pos = next(
                    (p for p in PartOfSpeech if p.value == token.pos),
                    PartOfSpeech.OTHER
                )
                entry = LexicalEntry(
                    pos=pos,
                    romanization=token.word,
                    phon_comp=PhonologicalComponent(
                        onset=None, nucleus=None, coda=None, tone=None
                    ),
                    eng_tran=""  # fill from scraper later
                )
                lex_entries.append(entry)

        self.repo.insert_lexicon(self.char, lex_entries)
        return lex_entries