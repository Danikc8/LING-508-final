import database.mysql_repo
from model.enumerations import PartOfSpeech
from model.lexical_entry import LexicalEntry
from model.phonological_components import PhonologicalComponent

class Services:

    def __init__(self):
        self.repo = database.mysql_repo.MysqlRepository()

    # Get all lexical entries for a given Chinese character
    def get_lexical_entries(self, char: str) -> list[LexicalEntry]:
        return self.repo.load_lexical_entries(char)

    # Return English translations for that character
    def get_translations(self, char: str) -> list[str]:
        entries = self.get_lexical_entries(char)
        return [entry.eng_tran for entry in entries if entry.eng_tran]

    # Return phonological breakdown(s) for that character
    def get_phonological_components(self, char: str) -> list[PhonologicalComponent]:
        entries = self.get_lexical_entries(char)
        return [entry.phon_comp for entry in entries if entry.phon_comp]

    # Return part-of-speech categories for that character
    def get_parts_of_speech(self, char: str) -> list[PartOfSpeech]:
        entries = self.get_lexical_entries(char)
        return [entry.pos for entry in entries if entry.pos]