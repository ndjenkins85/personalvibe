(personalvibe-py3.12) bash-3.2$ python prompts/storymaker/stages/10_bootstrap_p3a.py
• Wrote src/storymaker/api/spec_blueprint.py
• Wrote src/storymaker/api/app.py
• Wrote tests/test_api_spec.py
• Wrote .env.example

────────────────────────────────
Chunk A bootstrap completed 🎉
────────────────────────────────
• Run unit tests:      poetry run pytest -q
• Start API server:    python -m storymaker.api.app  (or `flask run`)
• Inspect spec:        http://localhost:8777/api/openapi.json

Front-end quick-start (if you’ve never used React/Vite):

1. Install Node ≥20 (recommended via https://github.com/nvm-sh/nvm).
2. cd storymaker_spa   # front-end folder
3. npm install        # pulls dependencies
4. npm run dev        # launches dev-server on http://localhost:5173

   The dev React app already uses the special header
   “Authorization: DEV” so it can call the Flask API without
   a login step.

When both servers are running you can open the SPA and browse:
• Home, My Books, Characters   (data coming from the backend)

Happy hacking! 🚀

(personalvibe-py3.12) bash-3.2$ poetry run pytest -q
FF...                                                                                                                                                                                              [100%]
================================================================================================ FAILURES ================================================================================================
___________________________________________________________________________________________ test_health_route ____________________________________________________________________________________________

    def test_health_route():
>       rv = _client().get("/api/health")

tests/test_api_spec.py:14:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests/test_api_spec.py:8: in _client
    app = create_app()
src/storymaker/api/app.py:40: in create_app
    from storymaker.api.spec_blueprint import spec_bp  # auto-added by Chunk A
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    """Light-weight OpenAPI-lite blueprint.

    Only captures *paths* and basic schema names.  Good enough for the SPA
    to auto-discover routes until a full swagger.json is generated later.
    """

    from __future__ import annotations

    from flask import Blueprint, jsonify, current_app

    spec_bp = Blueprint("spec_bp", __name__)

    _SPEC = {
        "openapi": "3.0.0",
        "info": {
            "title": "Storymaker API",
            "version": "0.1.0",
            "description": "Poor-man’s spec – will be replaced by real OpenAPI in a later chunk",
        },
        "paths": {
            "/api/health": {"get": {"summary": "Health check"}},
            "/api/login": {"post": {"summary": "Login (DEV shortcut)"}},
            "/api/me": {"get": {"summary": "Current user info"}},
            "/api/books": {
                "get": {"summary": "List books"},
                "post": {"summary": "Create book"},
            },
            "/api/books/{book_id}": {"get": {"summary": "Get book"}},
            "/api/characters": {
                "get": {"summary": "List characters"},
                "post": {"summary": "Create character"},
            },
            "/api/characters/{char_id}": {"get": {"summary": "Get character"}},
        },
    }

    @_SPEC.setdefault("__meta__", {})  # noqa: SLF001
E   TypeError: 'dict' object is not callable

src/storymaker/api/spec_blueprint.py:38: TypeError
___________________________________________________________________________________________ test_openapi_route ___________________________________________________________________________________________

    def test_openapi_route():
>       rv = _client().get("/api/openapi.json")

tests/test_api_spec.py:20:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests/test_api_spec.py:8: in _client
    app = create_app()
src/storymaker/api/app.py:40: in create_app
    from storymaker.api.spec_blueprint import spec_bp  # auto-added by Chunk A
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    """Light-weight OpenAPI-lite blueprint.

    Only captures *paths* and basic schema names.  Good enough for the SPA
    to auto-discover routes until a full swagger.json is generated later.
    """

    from __future__ import annotations

    from flask import Blueprint, jsonify, current_app

    spec_bp = Blueprint("spec_bp", __name__)

    _SPEC = {
        "openapi": "3.0.0",
        "info": {
            "title": "Storymaker API",
            "version": "0.1.0",
            "description": "Poor-man’s spec – will be replaced by real OpenAPI in a later chunk",
        },
        "paths": {
            "/api/health": {"get": {"summary": "Health check"}},
            "/api/login": {"post": {"summary": "Login (DEV shortcut)"}},
            "/api/me": {"get": {"summary": "Current user info"}},
            "/api/books": {
                "get": {"summary": "List books"},
                "post": {"summary": "Create book"},
            },
            "/api/books/{book_id}": {"get": {"summary": "Get book"}},
            "/api/characters": {
                "get": {"summary": "List characters"},
                "post": {"summary": "Create character"},
            },
            "/api/characters/{char_id}": {"get": {"summary": "Get character"}},
        },
    }

    @_SPEC.setdefault("__meta__", {})  # noqa: SLF001
E   TypeError: 'dict' object is not callable

src/storymaker/api/spec_blueprint.py:38: TypeError
============================================================================================ warnings summary ============================================================================================
src/storymaker/models/chapter.py:29
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/chapter.py:29: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("image_path", pre=True, always=True)

src/storymaker/models/character.py:34
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/character.py:34: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("avatar_path", pre=True, always=True)

src/storymaker/config.py:79
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/config.py:79: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("openai_api_key", pre=True, always=True)

.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:291
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:291: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

tests/test_auth.py::test_jwt_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/auth/auth.py:77: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "exp": _dt.datetime.utcnow() + expires,

tests/test_auth.py::test_jwt_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/auth/auth.py:78: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "iat": _dt.datetime.utcnow(),

tests/test_storage.py::test_save_load_book_roundtrip
tests/test_storage.py::test_save_load_book_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/main.py:212: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)

tests/test_storage.py::test_save_load_book_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/main.py:1114: PydanticDeprecatedSince20: The `dict` method is deprecated; use `model_dump` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================================================================== short test summary info =========================================================================================
FAILED tests/test_api_spec.py::test_health_route - TypeError: 'dict' object is not callable
FAILED tests/test_api_spec.py::test_openapi_route - TypeError: 'dict' object is not callable
2 failed, 3 passed, 9 warnings in 0.27s
(personalvibe-py3.12) bash-3.2$

------------

MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
2025-05-08 13:51:00 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-08 13:51:00 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/app.py", line 65, in <module>
    create_app().run(debug=settings.debug, port=8777)
    ^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/app.py", line 40, in create_app
    from storymaker.api.spec_blueprint import spec_bp  # auto-added by Chunk A
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/spec_blueprint.py", line 38, in <module>
    @_SPEC.setdefault("__meta__", {})  # noqa: SLF001
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'dict' object is not callable
MacBook-Air:personalvibe nicholasjenkins$
