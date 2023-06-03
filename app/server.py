from app.app.connect_players import socketio
from app.run import app

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
