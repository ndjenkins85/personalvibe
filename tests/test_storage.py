# Copyright © 2025 by Nick Jenkins. All rights reserved

import tempfile
from pathlib import Path

from storymaker.data.storage import LocalStorage
from storymaker.models.book import Book
from storymaker.models.chapter import Chapter
from storymaker.models.character import Character


def _dummy_book() -> Book:
    return Book(
        id="b1",
        name="Test Book",
        description="desc",
        main_character=Character(name="Plushie"),
        chapters=[Chapter(chapter=1, title="T", scene="S", key_visual="K")],
    )


def test_save_load_book_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        store = LocalStorage(base_dir=Path(tmp))
        b = _dummy_book()
        store.save_book(b)
        loaded = store.load_book(b.id)
        assert loaded.id == b.id
        assert loaded.main_character.name == "Plushie"
