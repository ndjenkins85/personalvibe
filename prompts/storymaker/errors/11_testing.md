(personalvibe-py3.12) bash-3.2$ python prompts/storymaker/stages/06_bootstrap_chunk4.py
  • Wrote storymaker_spa/package.json
  • Wrote storymaker_spa/tsconfig.json
  • Wrote storymaker_spa/vite.config.ts
  • Wrote storymaker_spa/index.html
  • Wrote storymaker_spa/src/main.tsx
  • Wrote storymaker_spa/src/App.tsx
  • Wrote storymaker_spa/src/components/NavBar.tsx
  • Wrote storymaker_spa/src/api/client.ts
  • Wrote storymaker_spa/src/pages/IndexPage.tsx
  • Wrote storymaker_spa/src/pages/BooksPage.tsx
  • Wrote storymaker_spa/src/pages/CharactersPage.tsx
  • Wrote storymaker_spa/src/pages/StudioPage.tsx
  • Wrote storymaker_spa/src/pages/AccountPage.tsx
  • Wrote storymaker_spa/README.md

✅ Storymaker SPA skeleton generated.

What next?
──────────────────────────────────────────────────────────────
1.  Make sure **Node ≥ 20** is available – easiest via nvm:

        nvm install 20
        nvm use 20

2.  Install front-end dependencies:

        cd storymaker_spa
        npm install

3.  In **one** terminal start the Flask API:

        poetry run python -m storymaker.api.app

4.  In **another** terminal start the Vite dev server:

        npm run dev

    → open http://localhost:5173  (SPA)
    → API at http://localhost:8777

5.  Edit React/TS files under `storymaker_spa/src/` – hot-reload FTW.

Troubleshooting:
• If install fails, delete `node_modules` & `package-lock.json`, run `npm cache clean --force`, then `npm install`.
• The SPA talks to the API with the header `Authorization: DEV`, so no login flow is needed yet.

(personalvibe-py3.12) bash-3.2$



--------------

bash-3.2$ cd ~/Documents/personalvibe/storymaker_spa
bash-3.2$ pwd
/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa
bash-3.2$ npm install

added 69 packages, and audited 70 packages in 17s

7 packages are looking for funding
  run `npm fund` for details

2 moderate severity vulnerabilities

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
bash-3.2$ npm run dev

> storymaker-spa@0.0.1 dev
> vite


  VITE v5.4.19  ready in 1216 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help


---------------------

MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
2025-05-08 10:58:15 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-08 10:58:15 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-08 10:58:15 | INFO | __main__ | 🚀 Storymaker API up — debug=True
 * Serving Flask app 'app'
 * Debug mode: on
2025-05-08 10:58:15 | INFO | werkzeug | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8777
2025-05-08 10:58:15 | INFO | werkzeug | Press CTRL+C to quit
2025-05-08 10:58:15 | INFO | werkzeug |  * Restarting with stat
2025-05-08 10:58:15 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-08 10:58:15 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-08 10:58:15 | INFO | __main__ | 🚀 Storymaker API up — debug=True
2025-05-08 10:58:15 | WARNING | werkzeug |  * Debugger is active!
2025-05-08 10:58:15 | INFO | werkzeug |  * Debugger PIN: 394-183-848
2025-05-08 10:58:27 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:27] "OPTIONS /api/books HTTP/1.1" 200 -
2025-05-08 10:58:27 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:27] "OPTIONS /api/books HTTP/1.1" 200 -
2025-05-08 10:58:27 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:27] "GET /api/books HTTP/1.1" 200 -
2025-05-08 10:58:27 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:27] "GET /api/books HTTP/1.1" 200 -
2025-05-08 10:58:35 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:35] "OPTIONS /api/characters HTTP/1.1" 200 -
2025-05-08 10:58:35 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:35] "OPTIONS /api/characters HTTP/1.1" 200 -
2025-05-08 10:58:35 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:35] "GET /api/characters HTTP/1.1" 200 -
2025-05-08 10:58:35 | INFO | werkzeug | 127.0.0.1 - - [08/May/2025 10:58:35] "GET /api/characters HTTP/1.1" 200 -


----------------

(personalvibe-py3.12) bash-3.2$ pwd
/Users/nicholasjenkins/Documents/personalvibe
(personalvibe-py3.12) bash-3.2$ python -m pytest
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
(personalvibe-py3.12) bash-3.2$

-----------------------------

http://localhost:5173/characters
(crude copy paste, looks barebones but fine)

HomeMy BooksCharactersStudioAccount
Characters
Plushie Duck (toy)
🚧 Upload form & avatar tools coming in later chunks.

-------------------------------

http://localhost:8777/

{
  "code": 404,
  "error": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
  "status": "error"
}
