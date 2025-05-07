# Copyright © 2025 by Nick Jenkins. All rights reserved

from storymaker.auth.auth import create_access_token, decode_access_token


def test_jwt_roundtrip():
    token = create_access_token("user123")
    payload = decode_access_token(token)
    assert payload["sub"] == "user123"
