from typing import Optional
from database.repo import *
from model.enumerations import PartOfSpeech
from model.phonological_components import PhonologicalComponent
import mysql.connector
import pycantonese as pc

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

    def load_lexical_entries(self, char: str) -> list[LexicalEntry]:
        sql = 'SELECT * FROM lexicon WHERE `character` = %s'
        self.cursor.execute(sql, (char,))
        entries = []

        for (id, character, pos, romanization, onset, nucleus, coda, tone, eng_tran) in self.cursor:
            phon = PhonologicalComponent(onset, nucleus, coda, tone)
            entry = {
                'pos': pos,
                'romanization': romanization,
                'phon_comp': phon,
                'eng_tran': eng_tran
            }
            entries.append(self.mapper(entry))
        return entries

    def insert_lexicon(self):
        sql = """
              INSERT INTO lexicon
                  (`character`, pos, romanization, onset, nucleus, coda, tone, eng_tran)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
              """

        for char in self.all_chars:
            corpus = pc.parse_text(char)
            utterances = corpus.utterances()
            entries = []

            for utt in utterances:
                for token in utt.tokens:
                    if token.word != char:
                        continue

                    phon_comp = pc.parse_jyutping(token.jyutping)
                    phon = phon_comp[0] if phon_comp else None

                    entry_dict = {
                        'pos': token.pos,
                        'romanization': token.jyutping,
                        'phon_comp': {
                            'onset': phon.onset if phon else None,
                            'nucleus': phon.nucleus if phon else None,
                            'coda': phon.coda if phon else None,
                            'tone': phon.tone if phon else None,
                        } if phon else None,
                        'eng_tran': None  # No English translation in PyCantonese
                    }

                    mapped_entry = self.mapper(entry_dict)
                    entries.append(mapped_entry)

            # Insert all entries for this character into MySQL
            for entry in entries:
                phon = entry.phon_comp
                self.cursor.execute(sql, (
                    char,
                    entry.pos.value if hasattr(entry.pos, 'value') else entry.pos,
                    entry.romanization,
                    phon.onset if phon else None,
                    phon.nucleus if phon else None,
                    phon.coda if phon else None,
                    phon.tone if phon else None,
                    '; '.join(entry.eng_tran) if isinstance(entry.eng_tran, list) else entry.eng_tran
                ))

            self.connection.commit()
