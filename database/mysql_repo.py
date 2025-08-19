from typing import Optional
from database.repo import *
from model.enumerations import PartOfSpeech
from model.phonological_components import PhonologicalComponent
import mysql.connector
import pycantonese as pc
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote

class MysqlRepository(Repository):

    def __init__(self):
        super().__init__()
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'localhost', # to run LOCALLY, this should be localhost
            'port': '32000', # to run LOCALLY, this should be 32000
            'database': 'cantonese'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

        self.hkcancor = pc.hkcancor()
        words = self.hkcancor.words()
        self.all_chars = set(ch for w in words for ch in w)

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def map_pos(self, entry: dict) -> Optional[PartOfSpeech]:
        pos_switcher = {'ADJ': PartOfSpeech.ADJECTIVE,
                        'ADP': PartOfSpeech.ADPOSITION,
                        'ADV': PartOfSpeech.ADVERB,
                        'AUX': PartOfSpeech.AUXILIARY,
                        'CCONJ': PartOfSpeech.COORDINATING_CONJUNCTION,
                        'DET': PartOfSpeech.DETERMINER,
                        'INTJ': PartOfSpeech.INTERJECTION,
                        'NOUN': PartOfSpeech.NOUN,
                        'NUM': PartOfSpeech.NUMERAL,
                        'PART': PartOfSpeech.PARTICLE,
                        'PRON': PartOfSpeech.PRONOUN,
                        'PROPN': PartOfSpeech.PROPER_NOUN,
                        'PUNCT': PartOfSpeech.PUNCTUATION,
                        'SCONJ': PartOfSpeech.SUBORDINATING_CONJUNCTION,
                        'SYM': PartOfSpeech.SYMBOL,
                        'VERB': PartOfSpeech.VERB,
                        'X': PartOfSpeech.OTHER}
        pos = pos_switcher.get(entry.get('pos'), None)
        return pos

    def map_phonological_component(self, jyutping: str) -> Optional[PhonologicalComponent]:
        if not jyutping:
            return None
        parsed = pc.parse_jyutping(jyutping)
        if not parsed:
            return None
        phon_comp = parsed[0]
        return PhonologicalComponent(
            onset=phon_comp.onset,
            nucleus=phon_comp.nucleus,
            coda=phon_comp.coda,
            tone=phon_comp.tone
        )

    def mapper(self, entry: dict) -> LexicalEntry:
        lexical_entry = LexicalEntry(pos=self.map_pos(entry),
                                     romanization=entry.get('romanization'),
                                     phon_comp=self.map_phonological_component(entry.get('romanization')),
                                     eng_tran=entry.get('eng_tran'))
        return lexical_entry

    def get_eng_translation(self, char: str) -> Optional[str]:
        char_url = "https://cantonese.org/search.php?q=" + quote(char)
        try:
            html = urlopen(char_url)
        except Exception as e:
            print("\Error:", e)
            return None

        soup = BeautifulSoup(html, 'html.parser')

        eng_tran_list = []

        for translation in soup.find('ol', attrs={'class': 'defnlist'}).children:
            eng_tran_list.append(translation.text)

        # Join the definitions with semicolons
        return "; ".join(m.strip() for m in eng_tran_list[:3])

    def insert_lexicon(self, char: str) -> None:
        # Only using small sample size from PyCantonese
        if char not in self.all_chars:
            return

        # Check if already in database
        self.cursor.execute('SELECT 1 FROM lexicon WHERE `character` = %s LIMIT 1', (char,))
        if self.cursor.fetchone():
            return

        sql = """
              INSERT INTO lexicon
                  (`character`, pos, romanization, onset, nucleus, coda, tone, eng_tran)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
              """

        corpus = pc.parse_text(char)
        entries_to_insert = []

        eng_tran = self.get_eng_translation(char)

        for utt in corpus.utterances():
            for token in utt.tokens:
                phon = self.map_phonological_component(token.jyutping)

                entry_dict = {
                    'pos': token.pos,
                    'romanization': token.jyutping,
                    'phon_comp': phon,
                    'eng_tran': eng_tran
                }

                lexical_entry = self.mapper(entry_dict)
                entries_to_insert.append(lexical_entry)

        # Insert into database
        for entry in entries_to_insert:
            phon = entry.phon_comp
            self.cursor.execute(sql, (
                char,
                entry.pos.value if entry.pos else None,
                entry.romanization if entry.romanization else None,
                phon.onset if phon else None,
                phon.nucleus if phon else None,
                phon.coda if phon else None,
                phon.tone if phon else None,
                entry.eng_tran if entry.eng_tran else None,
            ))

        self.connection.commit()

    def load_lexical_entries(self, char: str) -> list[LexicalEntry]:
        """
        Load lexical entries for a character. If it doesn't exist in the database,
        insert it first using insert_lexicon.
        """
        # Check if character exists
        self.cursor.execute('SELECT * FROM lexicon WHERE `character` = %s', (char,))
        rows = self.cursor.fetchall()

        if not rows:
            # Insert character on demand
            self.insert_lexicon(char)
            self.cursor.execute('SELECT * FROM lexicon WHERE `character` = %s', (char,))
            rows = self.cursor.fetchall()

        entries = []
        for (id, character, pos, romanization, onset, nucleus, coda, tone, eng_tran) in rows:
            phon = PhonologicalComponent(onset, nucleus, coda, tone)
            entry_dict = {
                'pos': pos,
                'romanization': romanization,
                'phon_comp': phon,
                'eng_tran': eng_tran
            }
            entries.append(self.mapper(entry_dict))

        return entries
