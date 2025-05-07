(personalvibe-py3.12) bash-3.2$ poetry run python -m storymaker.api.app
Traceback (most recent call last):
  File "<frozen runpy>", line 189, in _run_module_as_main
  File "<frozen runpy>", line 112, in _get_module_details
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/__init__.py", line 9, in <module>
    from storymaker.api.app import create_app  # noqa: F401
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/app.py", line 18, in <module>
    from storymaker.api.routes import register_routes
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/routes.py", line 15, in <module>
    from storymaker.api.schemas import (
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/api/schemas.py", line 9, in <module>
    from storymaker.models.book import Book
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/__init__.py", line 3, in <module>
    from storymaker.models.book import Book
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/book.py", line 20, in <module>
    class Book(BaseModel):
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/book.py", line 36, in Book
    @root_validator
     ^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/deprecated/class_validators.py", line 234, in root_validator
    return root_validator()(*__args)  # type: ignore
           ^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/deprecated/class_validators.py", line 240, in root_validator
    raise PydanticUserError(
pydantic.errors.PydanticUserError: If you use `@root_validator` with pre=False (the default) you MUST specify `skip_on_failure=True`. Note that `@root_validator` is deprecated and should be replaced with `@model_validator`.

For further information visit https://errors.pydantic.dev/2.9/u/root-validator-pre-skip
(personalvibe-py3.12) bash-3.2$
