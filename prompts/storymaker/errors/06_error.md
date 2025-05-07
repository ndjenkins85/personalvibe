running test commands

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
>         -d '{"email":"dev@local","password":""}'
{
  "code": 422,
  "error": "1 validation error for LoginRequest\nemail\n  value is not a valid email address: The part after the @-sign is not valid. It should have a period. [type=value_error, input_value='dev@local', input_type=str]",
  "status": "error"
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
  "code": 500,
  "error": "Internal Server Error",
  "status": "error"
}
(personalvibe-py3.12) bash-3.2$ curl http://127.0.0.1:8777/api/characters -H "Authorization: DEV"
{
  "data": [],
  "meta": {
    "page": 1,
    "pages": 0,
    "per_page": 50,
    "total": 0
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
  "code": 500,
  "error": "Internal Server Error",
  "status": "error"
}
(personalvibe-py3.12) bash-3.2$    curl "http://127.0.0.1:8777/api/books?page=1&per_page=10" -H "Authorization: DEV"
{
  "data": [],
  "meta": {
    "page": 1,
    "pages": 0,
    "per_page": 10,
    "total": 0
  },
  "status": "ok"
}
(personalvibe-py3.12) bash-3.2$ poetry run pytest
========================================================================================== test session starts ===========================================================================================
platform darwin -- Python 3.12.3, pytest-7.4.4, pluggy-1.5.0
rootdir: /Users/nicholasjenkins/Documents/personalvibe
plugins: anyio-4.9.0, xdoctest-1.2.0
collected 3 items

tests/test_auth.py .                                                                                                                                                                               [ 33%]
tests/test_storage.py F                                                                                                                                                                            [ 66%]
tests/test_utils.py .                                                                                                                                                                              [100%]

================================================================================================ FAILURES ================================================================================================
_____________________________________________________________________________________ test_save_load_book_roundtrip ______________________________________________________________________________________

    def test_save_load_book_roundtrip():
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalStorage(base_dir=Path(tmp))
            b = _dummy_book()
>           store.save_book(b)

tests/test_storage.py:26:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src/storymaker/data/storage.py:89: in save_book
    return self.save_json(book.dict(), self.base_dir / f"book_{book.id}")
src/storymaker/data/storage.py:78: in save_json
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False))
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py:238: in dumps
    **kw).encode(obj)
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py:202: in encode
    chunks = list(chunks)
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py:432: in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py:406: in _iterencode_dict
    yield from chunks
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py:439: in _iterencode
    o = _default(o)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <json.encoder.JSONEncoder object at 0x10db10620>, o = datetime.datetime(2025, 5, 7, 21, 27, 16, 617588)

    def default(self, o):
        """Implement this method in a subclass such that it returns
        a serializable object for ``o``, or calls the base implementation
        (to raise a ``TypeError``).

        For example, to support arbitrary iterators, you could
        implement default like this::

            def default(self, o):
                try:
                    iterable = iter(o)
                except TypeError:
                    pass
                else:
                    return list(iterable)
                # Let the base class default method raise the TypeError
                return super().default(o)

        """
>       raise TypeError(f'Object of type {o.__class__.__name__} '
                        f'is not JSON serializable')
E       TypeError: Object of type datetime is not JSON serializable

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py:180: TypeError
------------------------------------------------------------------------------------------ Captured stderr call ------------------------------------------------------------------------------------------
2025-05-07 17:27:16 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /private/var/folders/tp/5smflv0964j4q9b8fdxnf_3h0000gn/T/tmp_dahq8f6
------------------------------------------------------------------------------------------- Captured log call --------------------------------------------------------------------------------------------
INFO     storymaker.data.storage:storage.py:72 📂 LocalStorage ready at /private/var/folders/tp/5smflv0964j4q9b8fdxnf_3h0000gn/T/tmp_dahq8f6
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
======================================================================================== short test summary info =========================================================================================
FAILED tests/test_storage.py::test_save_load_book_roundtrip - TypeError: Object of type datetime is not JSON serializable
================================================================================ 1 failed, 2 passed, 9 warnings in 0.28s =================================================================================
(personalvibe-py3.12) bash-3.2$

----

server logs


MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
2025-05-07 17:25:42 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-07 17:25:42 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-07 17:25:42 | INFO | __main__ | 🚀 Storymaker API up — debug=True
 * Serving Flask app 'app'
 * Debug mode: on
2025-05-07 17:25:42 | INFO | werkzeug | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8777
2025-05-07 17:25:42 | INFO | werkzeug | Press CTRL+C to quit
2025-05-07 17:25:42 | INFO | werkzeug |  * Restarting with stat
2025-05-07 17:25:42 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-07 17:25:42 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-07 17:25:42 | INFO | __main__ | 🚀 Storymaker API up — debug=True
2025-05-07 17:25:42 | WARNING | werkzeug |  * Debugger is active!
2025-05-07 17:25:42 | INFO | werkzeug |  * Debugger PIN: 394-183-848
2025-05-07 17:25:45 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:25:45] "GET /api/health HTTP/1.1" 200 -
2025-05-07 17:25:49 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:25:49] "GET /api/spec HTTP/1.1" 200 -
2025-05-07 17:25:53 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:25:53] "POST /api/login HTTP/1.1" 422 -
2025-05-07 17:26:26 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:26:26] "POST /api/login HTTP/1.1" 401 -
2025-05-07 17:26:44 | ERROR | storymaker.api.errors | Unhandled exception: Object of type datetime is not JSON serializable
Traceback (most recent call last):
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/auth/auth.py", line 113, in wrapper
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/routes.py", line 114, in create_character
    storage.save_json(char.dict(), storage.base_dir / f"character_{char.id}")
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/data/storage.py", line 78, in save_json
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type datetime is not JSON serializable
2025-05-07 17:26:44 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:26:44] "POST /api/characters HTTP/1.1" 500 -
2025-05-07 17:26:49 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:26:49] "GET /api/characters HTTP/1.1" 200 -
2025-05-07 17:26:57 | ERROR | storymaker.api.errors | Unhandled exception: Object of type datetime is not JSON serializable
Traceback (most recent call last):
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/auth/auth.py", line 113, in wrapper
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/routes.py", line 83, in create_book
    storage.save_book(book)
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/data/storage.py", line 89, in save_book
    return self.save_json(book.dict(), self.base_dir / f"book_{book.id}")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/data/storage.py", line 78, in save_json
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type datetime is not JSON serializable
2025-05-07 17:26:57 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:26:57] "POST /api/books HTTP/1.1" 500 -
2025-05-07 17:27:03 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:27:03] "GET /api/books?page=1&per_page=10 HTTP/1.1" 200 -
