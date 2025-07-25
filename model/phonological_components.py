from model.character import *
from model.lexical_entry import *

class PhonologicalComponent(Character):

    def __init__(self,
                 lex_entry: LexicalEntry,
                 surface_form: str,
                 onset: str,
                 nucleus: str,
                 coda: str,
                 tone: str):
        super().__init__(lex_entry, surface_form)
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
        self.tone = tone