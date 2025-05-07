MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
Traceback (most recent call last):
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/networks.py", line 419, in import_email_validator
    import email_validator
ModuleNotFoundError: No module named 'email_validator'

The above exception was the direct cause of the following exception:

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
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/__init__.py", line 6, in <module>
    from storymaker.models.user import User
  File "/Users/nicholasjenkins/Documents/personalvibe/src/storymaker/models/user.py", line 12, in <module>
    class User(BaseModel):
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_model_construction.py", line 224, in __new__
    complete_model_class(
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_model_construction.py", line 577, in complete_model_class
    schema = cls.__get_pydantic_core_schema__(cls, handler)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/main.py", line 671, in __get_pydantic_core_schema__
    return handler(source)
           ^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_schema_generation_shared.py", line 83, in __call__
    schema = self._handler(source_type)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 655, in generate_schema
    schema = self._generate_schema_inner(obj)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 924, in _generate_schema_inner
    return self._model_schema(obj)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 739, in _model_schema
    {k: self._generate_md_field_schema(k, v, decorators) for k, v in fields.items()},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 1115, in _generate_md_field_schema
    common_field = self._common_field_schema(name, field_info, decorators)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 1308, in _common_field_schema
    schema = self._apply_annotations(
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 2107, in _apply_annotations
    schema = get_inner_schema(source_type)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_schema_generation_shared.py", line 83, in __call__
    schema = self._handler(source_type)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 2086, in inner_handler
    from_property = self._generate_schema_from_property(obj, source_type)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py", line 821, in _generate_schema_from_property
    schema = get_schema(
             ^^^^^^^^^^^
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/networks.py", line 459, in __get_pydantic_core_schema__
    import_email_validator()
  File "/Users/nicholasjenkins/Documents/personalvibe/.venv/lib/python3.12/site-packages/pydantic/networks.py", line 421, in import_email_validator
    raise ImportError('email-validator is not installed, run `pip install pydantic[email]`') from e
ImportError: email-validator is not installed, run `pip install pydantic[email]`
MacBook-Air:personalvibe nicholasjenkins$
