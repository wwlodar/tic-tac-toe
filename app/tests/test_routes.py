import unittest

from app.run import app


class TestIntegrations(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

    def test_username_not_logged(self):
        response = self.app.get("/")
        print(response)
        assert response.status_code == 200
        assert b"Type your username" in response.data

    def test_username_logged(self):
        response_create = self.app.post(
            "/", data={"username": "username"}, follow_redirects=True
        )
        assert response_create.status_code == 200
        assert response_create.request.path == "/home"

        response = self.app.get("/")
        assert response.status_code == 302
        assert response_create.request.path == "/home"

    def test_username_incorrect(self):
        response_create = self.app.post(
            "/",
            data={"username": "usernameusernameusernameusernameusername"},
            follow_redirects=True,
        )
        assert response_create.request.path == "/"
        assert b"Incorrect username!" in response_create.data

    def test_redirect(self):
        pass
