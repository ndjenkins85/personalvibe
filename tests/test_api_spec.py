# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Smoke-tests for the API foundations (health + openapi)."""

from storymaker.api.app import create_app


def _client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_health_route():
    rv = _client().get("/api/health")
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "ok"}


def test_openapi_route():
    rv = _client().get("/api/openapi.json")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["openapi"].startswith("3.")
    assert "/api/health" in data["paths"]
