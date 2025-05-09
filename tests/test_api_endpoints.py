# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Happy-path integration tests for Flask API.

These tests spin up a real Flask test_client, exercise the
JSON routes, and verify that the LocalStorage layer performs
the expected round-trips.  They *wipe* the LocalStorage
folder before/after to stay hermetic.
"""

import json
from http import HTTPStatus
from pathlib import Path

import pytest

from storymaker.api import create_app
from storymaker.api.routes import storage  # re-exported LocalStorage


# ───────────────────────── Fixtures ──────────────────────────
@pytest.fixture(scope="module")
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def _isolated_storage():
    """Clean LocalStorage before & after each test."""
    storage.wipe_all()
    yield
    storage.wipe_all()


DEV = {"Authorization": "DEV"}


# ───────────────────────── Tests – health & misc ─────────────
def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == HTTPStatus.OK
    assert r.get_json()["status"] == "ok"


def test_root_redirects(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (301, 302, 308)
    assert r.headers["Location"].endswith("/api/spec")


# ───────────────────────── Characters CRUD ───────────────────
def _create_character(client, name="Plushie Duck"):
    payload = {"name": name, "type": "toy", "description": "Soft yellow"}
    res = client.post("/api/characters", json=payload, headers=DEV)
    assert res.status_code == HTTPStatus.CREATED
    cid = res.get_json()["data"]["character_id"]
    # Fetch full object
    full = client.get(f"/api/characters/{cid}", headers=DEV).get_json()["data"]
    return full  # dict


def test_characters_roundtrip(client):
    char = _create_character(client)
    # List returns our character
    listed = client.get("/api/characters", headers=DEV).get_json()["data"]
    assert any(c["id"] == char["id"] for c in listed)


# ───────────────────────── Books CRUD ────────────────────────
def _create_book(client, main_character):
    payload = {
        "name": "My Test Book",
        "description": "A lovely description",
        "main_character": main_character,
        "side_characters": [],
        "chapters": [],
    }
    r = client.post("/api/books", json=payload, headers=DEV)
    assert r.status_code == HTTPStatus.CREATED
    return r.get_json()["data"]["book_id"]


def test_books_roundtrip(client):
    char = _create_character(client)
    book_id = _create_book(client, char)
    # GET
    g = client.get(f"/api/books/{book_id}", headers=DEV)
    assert g.status_code == HTTPStatus.OK
    assert g.get_json()["data"]["name"] == "My Test Book"
    # LIST
    books = client.get("/api/books", headers=DEV).get_json()["data"]
    assert any(b["id"] == book_id for b in books)


# ───────────────────────── Auth edge cases ───────────────────
def test_login_must_be_dev_local(client):
    bad = {"email": "foo@example.com", "password": "x"}
    r = client.post("/api/login", json=bad)
    assert r.status_code == HTTPStatus.UNAUTHORIZED
