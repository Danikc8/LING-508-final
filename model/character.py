from model.lexical_entry import LexicalEntry

class Character:

    def __init__(self,
                 surface_form: str,
                 lex_entry: LexicalEntry):
        self.surface_form = surface_form
        self.lex_entry = lex_entry