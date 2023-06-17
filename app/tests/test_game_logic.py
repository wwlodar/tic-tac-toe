from app.app import game_logic
from app.app.game_logic import (
    add_new_move,
    add_new_player,
    check_if_winning_move,
    clean_board,
    clean_player_list,
    create_new_game,
    get_opponent,
    get_user_name,
)
from app.app.models import Game, GameResult, GameStatus, User, UserGames


def test_clean_player_list():
    add_new_player(current_user_id=1)
    assert len(game_logic.player_list) == 1

    clean_player_list()
    assert len(game_logic.player_list) == 0


def test_add_new_player(app, db):
    result = add_new_player(current_user_id=1)
    assert result == {"data": "Wait for another player"}

    result = add_new_player(current_user_id=2)
    assert result == {1: "X", 2: "O"}


def test_get_opponent(app, db):
    user_1 = User(username="user1")
    user_2 = User(username="user2")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    result_of_selection = {1: "X", 2: "O"}
    current_user_id = 2
    [opponent_id, opponent_username] = get_opponent(
        result_of_selection, current_user_id
    )
    assert opponent_id == 1
    assert opponent_username == "user1"


def test_get_username(app, db):
    user_1 = User(username="user1")
    db.session.add(user_1)
    db.session.commit()
    username = get_user_name(user_1.id)
    assert username == "user1"


def test_clean_board(app, db):
    game_logic.board = [1, "x", "x", "x", 5, 6, 7, 8, 9]
    clean_board()
    assert game_logic.board == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_create_game(app, db):
    user_1 = User(username="user1")
    user_2 = User(username="user2")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    player_and_symbol = {1: "X", 2: "O"}
    game_id = create_new_game(player_and_symbol)
    assert game_id == 1

    game = Game.query.filter_by(id=game_id).first()
    assert game.player_1_id == user_1.id
    assert game.player_2_id == user_2.id


def test_add_new_move(app, db):
    updated_board = add_new_move(1, "x")
    assert updated_board == ["x", 2, 3, 4, 5, 6, 7, 8, 9]


def test_check_if_winning_move(app, db):
    user_1 = User(username="user1")
    user_2 = User(username="user2")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    game = Game(
        player_1_id=user_1.id, player_2_id=user_2.id, status=GameStatus("in_progress")
    )
    db.session.add(game)
    db.session.commit()

    # user 1 - "o" is current_user
    game_logic.board = ["o", "o", "o", 4, 5, "x", 6, "x", 8, 9]

    result = check_if_winning_move(user_1.id, game_logic.board, game.id)
    assert result == "user1"
    # user1 is winner

    game = Game.query.filter_by(id=game.id).first()
    assert game.status == GameStatus("ended")

    user_game = UserGames.query.filter_by(game_id=game.id).all()
    assert len(user_game) == 2
    assert user_game[0].user_id == user_1.id
    assert user_game[0].status == GameResult("win")
    assert user_game[1].user_id == user_2.id
    assert user_game[1].status == GameResult("lose")


def test_check_for_tie(app, db):
    user_1 = User(username="user1")
    user_2 = User(username="user2")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    game = Game(
        player_1_id=user_1.id, player_2_id=user_2.id, status=GameStatus("in_progress")
    )
    db.session.add(game)
    db.session.commit()

    # user 1 - "o" is current_user
    game_logic.board = ["o", "o", "x", "o", "x", "o", "x", "x", "o"]

    result = check_if_winning_move(user_1.id, game_logic.board, game.id)
    assert result == "Tie"
    # no winner - tie

    game = Game.query.filter_by(id=game.id).first()
    assert game.status == GameStatus("ended")

    user_game = UserGames.query.filter_by(game_id=game.id).all()
    assert len(user_game) == 2
    assert user_game[0].user_id == user_1.id
    assert user_game[0].status == GameResult("tie")
    assert user_game[1].user_id == user_2.id
    assert user_game[1].status == GameResult("tie")
