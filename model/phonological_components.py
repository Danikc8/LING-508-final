from model.enumerations import *
from model.character import *
from model.lexical_entry import *

class PhonologicalComponent(Character):

    def __init__(self,
                 lex_entry: LexicalEntry,
                 surface_form: str,
                 onset: Onset,
                 nucleus: Nucleus,
                 coda: Coda,
                 tone: Tone):
        super().__init__(lex_entry, surface_form)
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
        self.tone = tone