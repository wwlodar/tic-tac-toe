import json

from flask import request
from flask_socketio import SocketIO, emit

from app.app.game_logic import (
    add_new_move,
    add_new_player,
    check_if_winning_move,
    clean_board,
    clean_player_list,
    create_new_game,
    get_user_name,
)
from app.run import app

socketio = SocketIO(app)

socket_list = {}


@socketio.on("event connect")
def connect(data, current_user_id):
    socket_list[current_user_id["current_user_id"]] = request.sid
    print("You are connected")


@socketio.on_error()
def error_handler(e):
    print(e)


@socketio.on("start game")
def start_game(current_user_id):
    print("START GAME")
    result_of_selection = add_new_player(current_user_id)
    print(result_of_selection)
    if "X" in result_of_selection.values():
        clean_board()
        opponent_id = [
            i for i in list(result_of_selection.keys()) if i != current_user_id
        ][0]

        current_user_name = get_user_name(current_user_id)
        opponent_name = get_user_name(opponent_id)

        emit(
            "message from server",
            json.dumps({"data": f"Game starts! Your opponent is: {opponent_name}"}),
        )
        emit("symbol", json.dumps({"data": result_of_selection[current_user_id]}))
        emit("opponent name", json.dumps({"data": opponent_name}))

        emit(
            "message from server",
            json.dumps({"data": f"Game starts! Your opponent is: {current_user_name}"}),
            to=socket_list[opponent_id],
        )
        emit(
            "symbol",
            json.dumps({"data": result_of_selection[opponent_id]}),
            to=socket_list[opponent_id],
        )
        emit(
            "opponent name",
            json.dumps({"data": current_user_name}),
            to=socket_list[opponent_id],
        )

        game_id = create_new_game(player_and_symbol=result_of_selection)
        emit("new game id", json.dumps({"data": game_id}), broadcast=True)
    else:
        emit("message from server", json.dumps({result_of_selection}))


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


@socketio.on("move")
def handle_move(current_user_id, move, symbol, game_id):
    updated_board = add_new_move(int(move["move"]), symbol["symbol"])
    emit(
        "update board",
        {"move": move["move"], "symbol": symbol["symbol"]},
        broadcast=True,
    )
    result = check_if_winning_move(
        current_user_id["current_user_id"],
        symbol["symbol"],
        updated_board,
        game_id["game_id"],
    )
    if result == "Tie":
        emit("message from server", {"data": f"Game has ended, it was a tie"})
    elif not result:
        pass
    else:
        emit("finished game", broadcast=True)
        emit(
            "message from server",
            json.dumps(
                {"data": f"{result} won! Get back to homepage to start new game"}
            ),
            broadcast=True,
        )
        clean_player_list()
