import os
from app.services import Services
from model.lexical_entry import LexicalEntry
from model.phonological_components import PhonologicalComponent
from model.enumerations import PartOfSpeech


def test_fetch_inserts_and_retrieves():
    # First fetch should pull from PyCantonese and insert into DB
    service = Services("白")
    entries = service.fetch()
    assert isinstance(entries, list)
    assert all(isinstance(e, LexicalEntry) for e in entries)

    # Second fetch should come from DB (no PyCantonese call)
    entries2 = service.fetch()
    assert isinstance(entries2, list)
    assert len(entries2) == len(entries)


def test_fetch_has_pos_and_jyutping():
    service = Services("白")
    entries = service.fetch()
    assert any(isinstance(e.pos, PartOfSpeech) for e in entries)
    assert any(isinstance(e.phon_comp, PhonologicalComponent) for e in entries if e.phon_comp)


def test_pronounce_creates_file(tmp_path):
    char = "白"
    service = Services(char)

    mp3_file = tmp_path / f"{char}.mp3"
    filename = service.pronounce(str(mp3_file))

    assert os.path.exists(filename)
    assert filename.endswith(".mp3")
