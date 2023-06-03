from app.app.models import Game, GameResult, GameStatus, User, UserGames


def test_username_not_logged(app, db):
    response = app.get("/")
    print(response)
    assert response.status_code == 200
    assert b"Type your username" in response.data


def test_username_incorrect(app, db):
    response_create = app.post(
        "/",
        data={"username": "usernameusernameusernameusernameusername"},
    )
    assert b"Username must have between 1 and 30 characters" in response_create.data
    assert response_create.request.path == "/"


def test_username_correct(app, db):
    response_create = app.post(
        "/",
        data={"username": "username"},
        follow_redirects=True,
    )
    assert response_create.status_code == 200
    assert response_create.request.path == "/home"


def test_username_logged(app, db):
    response_create = app.post(
        "/", data={"username": "username"}, follow_redirects=True
    )
    assert response_create.status_code == 200
    assert response_create.request.path == "/home"

    response = app.get("/")
    assert response.status_code == 302
    assert response_create.request.path == "/home"


def test_homepage(app, db):
    response_create = app.post(
        "/",
        data={"username": "username"},
        follow_redirects=True,
    )
    response = app.get("/home")
    assert response.status_code == 200
    assert b"Tic-tac-toe game - Home" in response.data


def test_homepage_no_username(app, db):
    response = app.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert b"Type your username" in response.data


def test_health(app, db):
    response = app.get("/health", follow_redirects=True)
    assert response.status_code == 200
    assert response.data == b'{\n  "message": "It works!"\n}\n'


def test_game(app, db):
    response_create = app.post(
        "/",
        data={"username": "new_user"},
        follow_redirects=True,
    )
    response = app.get("/game", follow_redirects=True)
    assert response.status_code == 200
    assert b"Tic Tac Toe game" in response.data


def test_game_no_username(app, db):
    response = app.get("/game", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert b"Type your username" in response.data


def test_add_points(app, db):
    response_create = app.post(
        "/",
        data={"username": "new_user"},
        follow_redirects=True,
    )
    user = User.query.filter_by(username="new_user").first()
    response = app.get("/add_points", follow_redirects=True)
    assert response.status_code == 200
    assert response_create.request.path == "/home"
    assert user.points == 10


def test_add_points_no_username(app, db):
    response = app.get("/add_points", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert b"Type your username" in response.data


def test_stats(app, db):
    response_create = app.post(
        "/",
        data={"username": "new_user"},
        follow_redirects=True,
    )
    user = User.query.filter_by(username="new_user").first()
    opponent = User(username="opponent")
    db.session.add(opponent)
    db.session.commit()
    game = Game(
        player_1_id=user.id, player_2_id=opponent.id, status=GameStatus("ended")
    )
    db.session.add(game)
    db.session.commit()
    user_game = UserGames(user_id=user.id, game_id=game.id, status=GameResult("lose"))
    opponent_game = UserGames(
        user_id=opponent.id, game_id=game.id, status=GameResult("win")
    )

    db.session.add(user_game)
    db.session.add(opponent_game)
    db.session.commit()

    response = app.get("/stats")
    assert response.status_code == 200
    assert b"<a>Game status: </a>lose" in response.data
    assert b"<a>Opponent id: </a>\n    \n    2\n    \n" in response.data


def test_stats_no_username(app, db):
    response = app.get("/stats", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert b"Type your username" in response.data
