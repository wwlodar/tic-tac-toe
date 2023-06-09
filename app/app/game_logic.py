from typing import Any, Dict, List, Union

from app.app.models import Game, GameResult, GameStatus, User, UserGames
from app.extensions import db

player_list: List[int] = []
board: List[Union[str, int]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
winning_combinations: List[List[int]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def add_new_player(current_user_id: int) -> Dict[Any, str]:
    if len(player_list) == 0:
        player_list.append(current_user_id)
        return {"data": "Wait for another player"}
    elif current_user_id in player_list:
        return {"data": "Wait for another player"}
    else:
        player_list.append(current_user_id)
        return select_symbols(player_list)


def select_symbols(player_list: List[int]) -> Dict[int, str]:
    return {player_list[0]: "X", player_list[1]: "O"}


def get_opponent(
    result_of_selection: Dict[int, str], current_user_id: int
) -> List[Union[str, int]]:
    opponent_id = [i for i in list(result_of_selection.keys()) if i != current_user_id][
        0
    ]
    opponent = User.query.get(int(opponent_id))
    return [opponent_id, opponent.username]


def get_user_name(user_id: int) -> str:
    user = User.query.get(int(user_id))
    return user.username


def clean_board() -> None:
    global board
    board = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def clean_player_list() -> None:
    global player_list
    player_list = []


def create_new_game(player_and_symbol: Dict[int, str]) -> int:
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


def add_new_move(move: int, symbol: str) -> List[Union[str, int]]:
    if board[move - 1] == move:
        board[move - 1] = symbol
    return board


def check_if_winning_move(
    current_user_id: int, board: List[Union[str, int]], game_id: int
) -> str:
    if check_for_tie():
        game = Game.query.filter_by(id=game_id).first()
        game.status = GameStatus("ended")

        player_1 = game.player_1_id
        player_2 = game.player_2_id
        user_game_1 = UserGames(
            user_id=player_1, status=GameResult("tie"), game_id=game.id
        )
        user_game_2 = UserGames(
            user_id=player_2, status=GameResult("tie"), game_id=game.id
        )
        db.session.add(user_game_1)
        db.session.add(user_game_2)

        db.session.commit()
        return "Tie"

    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]]:
            game = Game.query.filter_by(id=game_id).first()
            game.status = GameStatus("ended")
            player_1 = game.player_1_id
            player_2 = game.player_2_id
            db.session.commit()

            if int(current_user_id) == int(player_1):
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
    return "No winner"


def check_for_tie() -> bool:
    check_for_num = [i for i in board if i in range(0, 10)]
    if len(check_for_num) == 0:
        print("True")
        return True
    else:
        return False
