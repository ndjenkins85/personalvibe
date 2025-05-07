MacBook-Air:personalvibe nicholasjenkins$ poetry run python -m storymaker.api.app
2025-05-07 17:21:49 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-07 17:21:49 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-07 17:21:49 | INFO | __main__ | 🚀 Storymaker API up — debug=True
 * Serving Flask app 'app'
 * Debug mode: on
2025-05-07 17:21:49 | INFO | werkzeug | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8777
2025-05-07 17:21:49 | INFO | werkzeug | Press CTRL+C to quit
2025-05-07 17:21:49 | INFO | werkzeug |  * Restarting with stat
2025-05-07 17:21:49 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
2025-05-07 17:21:49 | INFO | storymaker.data.storage | 📂 LocalStorage ready at /Users/nicholasjenkins/Documents/personalvibe/data/storymaker
<frozen runpy>:128: RuntimeWarning: 'storymaker.api.app' found in sys.modules after import of package 'storymaker.api', but prior to execution of 'storymaker.api.app'; this may result in unpredictable behaviour
2025-05-07 17:21:49 | INFO | __main__ | 🚀 Storymaker API up — debug=True
2025-05-07 17:21:49 | WARNING | werkzeug |  * Debugger is active!
2025-05-07 17:21:49 | INFO | werkzeug |  * Debugger PIN: 394-183-848
2025-05-07 17:21:53 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:21:53] "GET / HTTP/1.1" 404 -
2025-05-07 17:21:53 | INFO | werkzeug | 127.0.0.1 - - [07/May/2025 17:21:53] "GET /favicon.ico HTTP/1.1" 404 -

Does this look as expected (visiting http://127.0.0.1:8777/) what is the logical next steps for testing?
