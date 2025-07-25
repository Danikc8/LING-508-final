from model.enumerations import *
from model.phonological_components import PhonologicalComponent

class LexicalEntry:

    def __init__(self,
                 pos: PartOfSpeech,
                 romanization: str,
                 phon_comp: PhonologicalComponent = None,
                 eng_tran: str = None,):
        self.pos = pos
        self.romanization = romanization
        self.phon_comp = phon_comp
        self.eng_tran = eng_tran