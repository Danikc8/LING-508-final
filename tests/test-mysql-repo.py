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


def test_insert_lexicon():
    test_char = '白'

    # Clear any existing entries for this character
    repo.cursor.execute("DELETE FROM lexicon WHERE `character` = %s", (test_char,))
    repo.connection.commit()

    # Insert the character using the new method
    repo.all_chars = {test_char}
    repo.insert_lexicon()  # assumes insert_lexicon now uses self.all_chars internally

    # Fetch back from DB
    repo.cursor.execute(
        "SELECT `character`, pos, romanization, onset, nucleus, coda, tone FROM lexicon WHERE `character` = %s",
        (test_char,)
    )
    rows = repo.cursor.fetchall()

    # Assert that at least one entry was inserted
    assert len(rows) > 0

    # Assert that the character in the row matches what we inserted
    for row in rows:
        char, pos, romanization, onset, nucleus, coda, tone = row
        assert char == test_char
        assert pos is not None
        assert romanization is not None
        assert onset is not None
        assert nucleus is not None
        assert coda is not None
        assert tone is not None

    print(f"Inserted {len(rows)} entries for character '{test_char}' successfully.")