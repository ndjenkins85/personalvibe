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
