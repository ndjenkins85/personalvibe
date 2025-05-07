(personalvibe-py3.12) bash-3.2$ poetry run pytest
========================================================================================== test session starts ===========================================================================================
platform darwin -- Python 3.12.3, pytest-7.4.4, pluggy-1.5.0
rootdir: /Users/nicholasjenkins/Documents/personalvibe
plugins: anyio-4.9.0, xdoctest-1.2.0
collected 3 items

tests/test_auth.py .                                                                                                                                                                               [ 33%]
tests/test_storage.py .                                                                                                                                                                            [ 66%]
tests/test_utils.py .                                                                                                                                                                              [100%]

============================================================================================ warnings summary ============================================================================================
src/storymaker/config.py:79
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/config.py:79: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("openai_api_key", pre=True, always=True)

.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:291
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:291: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

src/storymaker/models/chapter.py:29
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/chapter.py:29: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("image_path", pre=True, always=True)

src/storymaker/models/character.py:34
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/character.py:34: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("avatar_path", pre=True, always=True)

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
===================================================================================== 3 passed, 9 warnings in 0.20s ======================================================================================
(personalvibe-py3.12) bash-3.2$ curl http://127.0.0.1:8777/api/health
{
  "status": "ok"
}
(personalvibe-py3.12) bash-3.2$ curl http://127.0.0.1:8777/api/spec
{
  "endpoints": [
    "/api/health",
    "/api/books",
    "/api/books/<id>",
    "/api/characters",
    "/api/characters/<id>",
    "/api/login",
    "/api/me"
  ]
}
(personalvibe-py3.12) bash-3.2$    curl -X POST http://127.0.0.1:8777/api/login \
>         -H "Content-Type: application/json" \
>         -d '{"email":"dev@local.com","password":""}'
{
  "code": 401,
  "error": "Only dev@local supported in MVP",
  "status": "error"
}
(personalvibe-py3.12) bash-3.2$    curl -X POST http://127.0.0.1:8777/api/characters \
>         -H "Content-Type: application/json" \
>         -H "Authorization: DEV" \
>         -d '{"name":"Plushie Duck","type":"toy","description":"Soft yellow plush"}'
{
  "data": {
    "character_id": "ee0033d6-7ebc-423a-a2ec-242e310b94f4"
  },
  "status": "ok"
}
(personalvibe-py3.12) bash-3.2$    curl http://127.0.0.1:8777/api/characters -H "Authorization: DEV"
{
  "data": [
    {
      "avatar_path": null,
      "created_at": "Wed, 07 May 2025 21:33:32 GMT",
      "description": "Soft yellow plush",
      "id": "ee0033d6-7ebc-423a-a2ec-242e310b94f4",
      "name": "Plushie Duck",
      "type": "toy"
    }
  ],
  "meta": {
    "page": 1,
    "pages": 1,
    "per_page": 50,
    "total": 1
  },
  "status": "ok"
}
(personalvibe-py3.12) bash-3.2$    curl -X POST http://127.0.0.1:8777/api/books \
>         -H "Content-Type: application/json" \
>         -H "Authorization: DEV" \
>         -d '{
>              "name":"My First Book",
>              "description":"A test book",
>              "main_character":{"name":"Plushie Duck","type":"toy","description":""},
>              "side_characters":[],
>              "chapters":[]
>         }'
{
  "data": {
    "book_id": "3c21b2b5-f9e4-44aa-87ce-b77fb5ae8fdb"
  },
  "status": "ok"
}
(personalvibe-py3.12) bash-3.2$    curl "http://127.0.0.1:8777/api/books?page=1&per_page=10" -H "Authorization: DEV"
{
  "data": [
    {
      "cover_image": null,
      "created_at": "Wed, 07 May 2025 21:33:47 GMT",
      "description": "A test book",
      "id": "3c21b2b5-f9e4-44aa-87ce-b77fb5ae8fdb",
      "name": "My First Book",
      "page_count": 0
    }
  ],
  "meta": {
    "page": 1,
    "pages": 1,
    "per_page": 10,
    "total": 1
  },
  "status": "ok"
}
(personalvibe-py3.12) bash-3.2$    curl -X POST http://127.0.0.1:8777/api/login \
>         -H "Content-Type: application/json" \
>         -d '{"email":"dev@local","password":""}'
{
  "code": 422,
  "error": "1 validation error for LoginRequest\nemail\n  value is not a valid email address: The part after the @-sign is not valid. It should have a period. [type=value_error, input_value='dev@local', input_type=str]",
  "status": "error"
}
(personalvibe-py3.12) bash-3.2$


--- webserver logs


MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
2025-05-07 17:33:10 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-07 17:33:10 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-07 17:33:11 | INFO | __main__ | 🚀 Storymaker API up — debug=True
 * Serving Flask app 'app'
 * Debug mode: on
2025-05-07 17:33:11 | INFO | werkzeug | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8777
2025-05-07 17:33:11 | INFO | werkzeug | Press CTRL+C to quit
2025-05-07 17:33:11 | INFO | werkzeug |  * Restarting with stat
2025-05-07 17:33:11 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-07 17:33:11 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-07 17:33:11 | INFO | __main__ | 🚀 Storymaker API up — debug=True
2025-05-07 17:33:11 | WARNING | werkzeug |  * Debugger is active!
2025-05-07 17:33:11 | INFO | werkzeug |  * Debugger PIN: 394-183-848
2025-05-07 17:33:17 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:33:17] "GET /api/health HTTP/1.1" 200 -
2025-05-07 17:33:20 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:33:20] "GET /api/spec HTTP/1.1" 200 -
2025-05-07 17:33:25 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:33:25] "POST /api/login HTTP/1.1" 401 -
2025-05-07 17:33:32 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:33:32] "POST /api/characters HTTP/1.1" 201 -
2025-05-07 17:33:39 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:33:39] "GET /api/characters HTTP/1.1" 200 -
2025-05-07 17:33:47 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:33:47] "POST /api/books HTTP/1.1" 201 -
2025-05-07 17:33:54 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:33:54] "GET /api/books?page=1&per_page=10 HTTP/1.1" 200 -
2025-05-07 17:34:41 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:34:41] "POST /api/login HTTP/1.1" 422 -
