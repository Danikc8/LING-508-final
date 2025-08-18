import pytest
from model.enumerations import PartOfSpeech
from model.lexical_entry import LexicalEntry
from model.phonological_components import PhonologicalComponent
from app.services import Services

@pytest.fixture
def services():
    return Services()

def test_get_lexical_entries_single_character(services):
    char = "心"  # test character
    entries = services.get_lexical_entries(char)

    # Assert we got a list
    assert isinstance(entries, list)
    assert len(entries) > 0  # should have at least one entry

    # Check properties of first entry
    first_entry = entries[0]
    assert isinstance(first_entry, LexicalEntry)
    assert first_entry.pos in PartOfSpeech  # pos should be valid enum
    assert isinstance(first_entry.romanization, str)
    # phonological component may or may not exist
    if first_entry.phon_comp:
        assert isinstance(first_entry.phon_comp, PhonologicalComponent)
        assert hasattr(first_entry.phon_comp, 'onset')
        assert hasattr(first_entry.phon_comp, 'nucleus')
        assert hasattr(first_entry.phon_comp, 'coda')
        assert hasattr(first_entry.phon_comp, 'tone')
    # English translation may be None
    if first_entry.eng_tran:
        assert isinstance(first_entry.eng_tran, str)