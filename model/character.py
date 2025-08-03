from model.lexical_entry import LexicalEntry

class Character:

    def __init__(self,
                 character: str,
                 lex_entries: list[LexicalEntry]):
        self.character = character
        self.lex_entries = lex_entries