Tic-tac-toe app build with Flask, Flask-socketio, Javscript and Docker.
-------------

Added eslint and prettier for JavaScript; pre-commit for Python.


Run app:

1. Run: ``` docker compose -f docker-compose.yml build ```

2. Run: ``` docker compose -f docker-compose.yml up ```
3. App should be available at http://127.0.0.1:5000/


Run tests:

1. Change Config to TestConfig in ```app/run.py```.

```python
from app.app.main import create_app
from app.config import TestConfig

app = create_app(config_class=TestConfig)
```

2.  Run: ``` docker compose -f test-docker-compose.yml build ```

3. Run: ``` docker compose -f test-docker-compose.yml up ```
4. Run tests eg. on test_routes.py: ``` pytest app/tests/test_routes.py ```



