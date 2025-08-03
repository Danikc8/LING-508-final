from database.mysql_repo import MysqlRepository
from model.enumerations import PartOfSpeech
from model.lexical_entry import LexicalEntry
from model.phonological_components import PhonologicalComponent

repo = MysqlRepository()

def test_complete_phon_comp_data():
    entry_1 = {'id': 8,
                'character': '心',
                'pos': 'NOUN',
                'romanization': 'sam1',
                'eng_tran': 'heart',
                'onset': 's',
                'nucleus': 'a',
                'coda': 'm',
                'tone': '1'
                }
    lex_entry_1 = repo.mapper(entry_1)

    assert isinstance(lex_entry_1, LexicalEntry)
    assert lex_entry_1.pos == PartOfSpeech.NOUN
    assert lex_entry_1.romanization == "sam1"
    assert lex_entry_1.eng_tran == "heart"
    assert isinstance(lex_entry_1.phon_comp, PhonologicalComponent)
    assert lex_entry_1.phon_comp.onset == "s"
    assert lex_entry_1.phon_comp.nucleus == "a"
    assert lex_entry_1.phon_comp.coda == "m"
    assert lex_entry_1.phon_comp.tone == "1"

def test_incomplete_phonological_comp_data():
    entry_2 = {'id': 9,
               'character': '唔',
               'pos': 'PART',
               'romanization': 'm4',
               'eng_tran': 'not; no',
               'onset': '',
               'nucleus': 'm',
               'coda': '',
               'tone': '4'
               }

    lex_entry_2 = repo.mapper(entry_2)

    assert isinstance(lex_entry_2, LexicalEntry)
    assert lex_entry_2.pos == PartOfSpeech.PARTICLE
    assert lex_entry_2.romanization == "m4"
    assert lex_entry_2.eng_tran == "not; no"
    assert isinstance(lex_entry_2.phon_comp, PhonologicalComponent)
    assert lex_entry_2.phon_comp.onset == ""
    assert lex_entry_2.phon_comp.nucleus == "m"
    assert lex_entry_2.phon_comp.coda == ""
    assert lex_entry_2.phon_comp.tone == "4"