(personalvibe-py3.12) bash-3.2$ python prompts/storymaker/stages/14_bootstrap_p3e.py
🛠  Detected repo root at /Users/nicholasjenkins/Documents/personalvibe
✅ Patched src/storymaker/api/app.py
✅ Created tests/test_api_endpoints.py

───────────────────────────────────────────────────────────────
SUCCESS – Chunk E assets written/updated.

Next steps
──────────
1.  Install dev deps (once per machine):
      $ poetry install --with tests

2.  Run the test suite:
      $ poetry run pytest

    All  🟢  tests (auth, storage, NEW api endpoints) should pass.

3.  (Optional) start the Flask API locally to verify the new
    '/' redirect:
      $ python -m storymaker.api.app
      Visit http://127.0.0.1:8777/  → should bounce to /api/spec

4.  Front-end developers can now rely on these tested endpoints.

Happy hacking! 🚀
───────────────────────────────────────────────────────────────

(personalvibe-py3.12) bash-3.2$ poetry install --with tests
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: personalvibe (0.1.0)
(personalvibe-py3.12) bash-3.2$ poetry run pytest
========================================================================================== test session starts ===========================================================================================
platform darwin -- Python 3.12.3, pytest-7.4.4, pluggy-1.5.0
rootdir: /Users/nicholasjenkins/Documents/personalvibe
plugins: anyio-4.9.0, xdoctest-1.2.0
collected 11 items

tests/test_api_endpoints.py .F...                                                                                                                                                                  [ 45%]
tests/test_api_spec.py ..                                                                                                                                                                          [ 63%]
tests/test_auth.py .                                                                                                                                                                               [ 72%]
tests/test_jobs.py F                                                                                                                                                                               [ 81%]
tests/test_storage.py .                                                                                                                                                                            [ 90%]
tests/test_utils.py .                                                                                                                                                                              [100%]

================================================================================================ FAILURES ================================================================================================
__________________________________________________________________________________________ test_root_redirects ___________________________________________________________________________________________

client = <FlaskClient <Flask 'storymaker.api.app'>>

    def test_root_redirects(client):
        r = client.get("/", follow_redirects=False)
>       assert r.status_code in (301, 302, 308)
E       assert 404 in (301, 302, 308)
E        +  where 404 = <WrapperTestResponse streamed [404 NOT FOUND]>.status_code

tests/test_api_endpoints.py:44: AssertionError
----------------------------------------------------------------------------------------- Captured stderr setup ------------------------------------------------------------------------------------------
2025-05-09 12:15:19 | WARNING | storymaker.data.storage | 🧹 LocalStorage wiped data/storymaker
------------------------------------------------------------------------------------------- Captured log setup -------------------------------------------------------------------------------------------
WARNING  storymaker.data.storage:storage.py:117 🧹 LocalStorage wiped data/storymaker
---------------------------------------------------------------------------------------- Captured stderr teardown ----------------------------------------------------------------------------------------
2025-05-09 12:15:19 | WARNING | storymaker.data.storage | 🧹 LocalStorage wiped data/storymaker
----------------------------------------------------------------------------------------- Captured log teardown ------------------------------------------------------------------------------------------
WARNING  storymaker.data.storage:storage.py:117 🧹 LocalStorage wiped data/storymaker
__________________________________________________________________________________________ test_job_queue_basic __________________________________________________________________________________________

    def test_job_queue_basic():
>       job_id = job_queue.submit(_echo, 21)

tests/test_jobs.py:13:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src/storymaker/jobs/__init__.py:88: in submit
    self._persist(job)
src/storymaker/jobs/__init__.py:138: in _persist
    path.write_text(job.model_dump_json(indent=2, exclude_none=True), encoding="utf-8")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1047: in write_text
    with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = PosixPath('data/storymaker/jobs/job_a34fa3ca-a4f3-4d3b-9e43-2b87241fef5b.json'), mode = 'w', buffering = -1, encoding = 'utf-8', errors = None, newline = None

    def open(self, mode='r', buffering=-1, encoding=None,
             errors=None, newline=None):
        """
        Open the file pointed by this path and return a file object, as
        the built-in open() function does.
        """
        if "b" not in mode:
            encoding = io.text_encoding(encoding)
>       return io.open(self, mode, buffering, encoding, errors, newline)
E       FileNotFoundError: [Errno 2] No such file or directory: 'data/storymaker/jobs/job_a34fa3ca-a4f3-4d3b-9e43-2b87241fef5b.json'

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1013: FileNotFoundError
============================================================================================ warnings summary ============================================================================================
src/storymaker/models/chapter.py:29
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/chapter.py:29: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("image_path", pre=True, always=True)

src/storymaker/models/character.py:42
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/character.py:42: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("avatar_path", pre=True, always=True)

src/storymaker/config.py:79
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/config.py:79: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    @validator("openai_api_key", pre=True, always=True)

.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:291
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:291: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

tests/test_api_endpoints.py::test_characters_roundtrip
tests/test_api_endpoints.py::test_books_roundtrip
tests/test_api_endpoints.py::test_books_roundtrip
tests/test_api_endpoints.py::test_login_must_be_dev_local
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/main.py:1159: PydanticDeprecatedSince20: The `parse_obj` method is deprecated; use `model_validate` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    warnings.warn(

tests/test_api_endpoints.py::test_characters_roundtrip
tests/test_api_endpoints.py::test_books_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/main.py:596: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return cls.__pydantic_validator__.validate_python(

tests/test_api_endpoints.py: 11 warnings
tests/test_storage.py: 1 warning
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/main.py:1114: PydanticDeprecatedSince20: The `dict` method is deprecated; use `model_dump` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

tests/test_api_endpoints.py::test_books_roundtrip
tests/test_jobs.py::test_job_queue_basic
tests/test_jobs.py::test_job_queue_basic
tests/test_storage.py::test_save_load_book_roundtrip
tests/test_storage.py::test_save_load_book_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/main.py:212: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)

tests/test_auth.py::test_jwt_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/auth/auth.py:77: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "exp": _dt.datetime.utcnow() + expires,

tests/test_auth.py::test_jwt_roundtrip
  /Users/nicholasjenkins/Documents/personalvibe/src/storymaker/auth/auth.py:78: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "iat": _dt.datetime.utcnow(),

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================================================================== short test summary info =========================================================================================
FAILED tests/test_api_endpoints.py::test_root_redirects - assert 404 in (301, 302, 308)
FAILED tests/test_jobs.py::test_job_queue_basic - FileNotFoundError: [Errno 2] No such file or directory: 'data/storymaker/jobs/job_a34fa3ca-a4f3-4d3b-9e43-2b87241fef5b.json'
================================================================================ 2 failed, 9 passed, 29 warnings in 0.32s ================================================================================
(personalvibe-py3.12) bash-3.2$

--------------

MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
2025-05-09 12:16:04 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-09 12:16:04 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-09 12:16:04 | INFO | storymaker.jobs | 🪄 LocalJobQueue ready (workers=4)
2025-05-09 12:16:04 | INFO | __main__ | 🚀 Storymaker API up — debug=True
 * Serving Flask app 'app'
 * Debug mode: on
2025-05-09 12:16:04 | INFO | werkzeug | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8777
2025-05-09 12:16:04 | INFO | werkzeug | Press CTRL+C to quit
2025-05-09 12:16:04 | INFO | werkzeug |  * Restarting with stat
2025-05-09 12:16:04 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-09 12:16:04 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-09 12:16:04 | INFO | storymaker.jobs | 🪄 LocalJobQueue ready (workers=4)
2025-05-09 12:16:04 | INFO | __main__ | 🚀 Storymaker API up — debug=True
2025-05-09 12:16:04 | WARNING | werkzeug |  * Debugger is active!
2025-05-09 12:16:04 | INFO | werkzeug |  * Debugger PIN: 394-183-848
2025-05-09 12:16:05 | INFO | werkzeug | 127.0.0.1 - - [09/May/2025 12:16:05] "GET / HTTP/1.1" 404 -





-----------

http://127.0.0.1:8777/

{
  "code": 404,
  "error": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
  "status": "error"
}
