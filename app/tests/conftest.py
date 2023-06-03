import pytest

from app.app.main import create_app
from app.config import TestConfig
from app.extensions import db as _db


@pytest.fixture(scope="function")
def app(request):
    flask_app = create_app(config_class=TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.

    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()

    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return testing_client


@pytest.fixture(scope="function")
def db(app, request):
    def teardown():
        _db.session.close()
        _db.drop_all()

    _db.app = app
    _db.drop_all()
    _db.create_all()

    request.addfinalizer(teardown)
    return _db
