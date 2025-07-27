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
    character = Character(surface_form="心", lex_entries=[entry])

    assert character.surface_form == "心"
    assert character.lex_entries[0].romanization == "sam1"
    assert character.lex_entries[0].eng_tran == "heart"

def test_character_with_multiple_lexical_entries():
    pc1 = PhonologicalComponent(onset="s", nucleus="a", coda="m", tone="1")
    entry1 = LexicalEntry(
        pos=PartOfSpeech.NOUN,
        romanization="sam1",
        phon_comp=pc1,
        eng_tran="heart"
    )

    pc2 = PhonologicalComponent(onset="s", nucleus="a", coda="m", tone="3")
    entry2 = LexicalEntry(
        pos=PartOfSpeech.VERB,
        romanization="sam3",
        phon_comp=pc2,
        eng_tran="to keep in mind"
    )

    character = Character(surface_form="心", lex_entries=[entry1, entry2])

    assert character.surface_form == "心"
    assert len(character.lex_entries) == 2
    assert character.lex_entries[0].romanization == "sam1"
    assert character.lex_entries[0].phon_comp.tone == "1"
    assert character.lex_entries[0].pos == PartOfSpeech.NOUN
    assert character.lex_entries[0].eng_tran == "heart"
    assert character.lex_entries[1].romanization == "sam3"
    assert character.lex_entries[1].phon_comp.tone == "3"
    assert character.lex_entries[1].pos == PartOfSpeech.VERB
    assert character.lex_entries[1].eng_tran == "to keep in mind"
