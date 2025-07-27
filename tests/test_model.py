from model.character import Character
from model.lexical_entry import LexicalEntry
from model.phonological_components import PhonologicalComponent
from model.enumerations import PartOfSpeech

def test_phonological_component():
    pc = PhonologicalComponent(onset="s", nucleus="a", coda="m", tone="1")

    assert pc.onset == "s"
    assert pc.nucleus == "a"
    assert pc.coda == "m"
    assert pc.tone == "1"

def test_lexical_entry():
    pc = PhonologicalComponent(onset="s", nucleus="a", coda="m", tone="1")
    entry = LexicalEntry(
        pos=PartOfSpeech.NOUN,
        romanization="sam1",
        phon_comp=pc,
        eng_tran="heart"
    )

    assert entry.pos == PartOfSpeech.NOUN
    assert entry.romanization == "sam1"
    assert entry.phon_comp == pc
    assert entry.eng_tran == "heart"

def test_character():
    pc = PhonologicalComponent(onset="s", nucleus="a", coda="m", tone="1")
    entry = LexicalEntry(
        pos=PartOfSpeech.NOUN,
        romanization="sam1",
        phon_comp=pc,
        eng_tran="heart"
    )
    character = Character(surface_form="心", lex_entry=entry)

    assert character.surface_form == "心"
    assert character.lex_entry.romanization == "sam1"
    assert character.lex_entry.phon_comp.onset == "s"
    assert character.lex_entry.eng_tran == "heart"
