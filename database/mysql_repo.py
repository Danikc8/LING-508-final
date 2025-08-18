from database.repo import *
from model.enumerations import PartOfSpeech
from model.phonological_components import PhonologicalComponent
import mysql.connector

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

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def map_pos(self, entry: dict) -> PartOfSpeech:
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

    def map_phonological_component(self, entry: dict) -> PhonologicalComponent:
        return PhonologicalComponent(
            onset=entry.get("onset"),
            nucleus=entry.get("nucleus"),
            coda=entry.get("coda"),
            tone=entry.get("tone")
        )

    def mapper(self, entry: dict) -> LexicalEntry:
        lexical_entry = LexicalEntry(pos=self.map_pos(entry),
                                     romanization=entry.get('romanization'),
                                     phon_comp=self.map_phonological_component(entry),
                                     eng_tran=entry.get('eng_tran'))
        return lexical_entry

    def load_lexical_entries(self, char: str) -> list[LexicalEntry]:
        sql = 'SELECT * FROM lexicon WHERE `character` = %s'
        self.cursor.execute(sql, (char,))
        entries = []
        for (id, character, pos, romanization, onset, nucleus, coda, tone, eng_tran) in self.cursor:
            entry = {'id': id,
                    'character': character,
                    'pos': pos,
                    'romanization': romanization,
                    'phon_comp': self.map_phonological_component({
                        'onset': onset,
                        'nucleus': nucleus,
                        'coda': coda,
                        'tone': tone,
                    }),
                    'eng_tran': eng_tran
                     }
        entries.append(self.mapper(entry))
        return entries
