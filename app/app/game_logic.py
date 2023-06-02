from typing import List

from app.app.models import Game, GameResult, GameStatus, User, UserGames
from app.extensions import db

player_list: List[str] = []
board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
winning_combinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def add_new_player(current_user_id):
    if len(player_list) == 0:
        player_list.append(current_user_id)
        return {"data": "Wait for another player"}
    else:
        player_list.append(current_user_id)
        return select_symbols(player_list)


def select_symbols(player_list):
    return {player_list[0]: "X", player_list[1]: "O"}


def get_opponent(result_of_selection, current_user_id):
    opponent_id = [i for i in list(result_of_selection.keys()) if i != current_user_id][
        0
    ]
    opponent = User.query.get(int(opponent_id))
    return [opponent_id, opponent.username]


def get_user_name(user_id):
    user = User.query.get(int(user_id))
    return user.username


def clean_board():
    global board
    board = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def create_new_game(player_and_symbol: dict):
    board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    player_1 = list(player_and_symbol.keys())[0]
    player_2 = list(player_and_symbol.keys())[1]
    p1 = User.query.get(int(player_1))
    p2 = User.query.get(int(player_2))
    p1.points -= 3
    p2.points -= 3
    new_game = Game(
        player_1_id=player_1, player_2_id=player_2, status=GameStatus("in_progress")
    )
    db.session.add(new_game)
    db.session.commit()
    return new_game.id


def add_new_move(move, symbol):
    if board[move - 1] == move:
        board[move - 1] = symbol
    return board


def check_if_winning_move(current_user_id, symbol, board, game_id):
    print("check if winning")
    print("game_id", game_id)
    if check_for_tie():
        game = Game.query.filter_by(id=game_id).first()
        game.status = GameStatus("ended")

        player_1 = game.player_1_id
        player_2 = game.player_2_id
        user_game_1 = UserGames(user_id=player_1, status="tie", game_id=game.id)
        user_game_2 = UserGames(user_id=player_2, status="tie", game_id=game.id)
        db.session.add(user_game_1)
        db.session.add(user_game_2)

        db.session.commit()
        return "Tie"
    # if winner, add 4 point to user.points
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]]:
            print("Someone won")
            game = Game.query.filter_by(id=game_id).first()
            game.status = GameStatus("ended")
            player_1 = game.player_1_id
            player_2 = game.player_2_id
            print("current_user", current_user_id)
            print("player1", player_1)
            print("player2", player_2)
            print("symbol", symbol)
            print("board_combo", board[combination[0]])
            db.session.commit()

            if symbol == board[combination[0]]:
                if int(current_user_id) == int(player_1):
                    print("player 1 won")
                    user_game_1 = UserGames(
                        user_id=player_1, status=GameResult("win"), game_id=game_id
                    )
                    user_game_2 = UserGames(
                        user_id=player_2, status=GameResult("lose"), game_id=game_id
                    )
                    db.session.add(user_game_1)
                    db.session.add(user_game_2)
                    winner = User.query.get(int(player_1))
                else:
                    print("player 2 won")
                    user_game_1 = UserGames(
                        user_id=player_1, status=GameResult("lose"), game_id=game_id
                    )
                    user_game_2 = UserGames(
                        user_id=player_2, status=GameResult("win"), game_id=game_id
                    )
                    db.session.add(user_game_1)
                    db.session.add(user_game_2)
                    winner = User.query.get(int(player_2))
                winner.points += 4
                db.session.commit()

            return winner.username
    return None


def check_for_tie():
    check_for_num = [i for i in board if i in range(0, 10)]
    if len(check_for_num) == 0:
        return True
    else:
        return False
