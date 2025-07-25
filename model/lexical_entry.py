from model.enumerations import *

class LexicalEntry:

    def __init__(self,
                 form: str,
                 pos: PartOfSpeech,
                 romanization: str,
                 phon_comp: PhonologicalComponents = None,
                 eng_tran: str):
        self.form = form
        self.pos = pos
        self.romanization = romanization
        self.phon_comp = phon_comp
        self.eng_tran = eng_tran