MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_config.py:341: UserWarning: Valid config keys have changed in V2:
* 'allow_population_by_field_name' has been renamed to 'populate_by_name'
* 'orm_mode' has been renamed to 'from_attributes'
  warnings.warn(message, UserWarning)
Traceback (most recent call last):
  File "<frozen runpy>", line 189, in _run_module_as_main
  File "<frozen runpy>", line 112, in _get_module_details
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/__init__.py", line 9, in <module>
    from storymaker.api.app import create_app  # noqa: F401
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/app.py", line 18, in <module>
    from storymaker.api.routes import register_routes
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/routes.py", line 24, in <module>
    from storymaker.auth.auth import DEV_USER, create_access_token, login_required
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/auth/auth.py", line 27, in <module>
    from storymaker.config import settings
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/config.py", line 19, in <module>
    from pydantic import BaseSettings, Field, HttpUrl, validator
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/__init__.py", line 402, in __getattr__
    return _getattr_migration(attr_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_migration.py", line 296, in wrapper
    raise PydanticImportError(
pydantic.errors.PydanticImportError: `BaseSettings` has been moved to the `pydantic-settings` package. See https://docs.pydantic.dev/2.9/migration/#basesettings-has-moved-to-pydantic-settings for more details.

For further information visit https://errors.pydantic.dev/2.9/u/import-error
MacBook-Air:personalvibe nicholasjenkins$
