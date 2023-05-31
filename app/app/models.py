import enum
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.app.main import db
from app.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserState(enum.Enum):
    idle = "idle"
    waiting_for_game = "waiting_for_game"
    in_game = "in_game"


class GameResult(enum.Enum):
    win = "win"
    lose = "lose"
    tie = "tie"


class GameStatus(enum.Enum):
    in_progess = "in_progress"
    ended = "ended"


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    status: Mapped[UserState] = mapped_column(default="idle")
    points: Mapped[int] = mapped_column(default=0)
    added_points: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    games: Mapped[List["UserGames"]] = relationship(back_populates="user")

    def get_id(self):
        return self.id


class Game(db.Model):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)

    player_1_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    player_2_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    status: Mapped[GameStatus]

    time_in_seconds: Mapped[int]
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UserGames(db.Model):
    __tablename__ = "usergames"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[GameResult]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship()

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    game: Mapped["Game"] = relationship()
