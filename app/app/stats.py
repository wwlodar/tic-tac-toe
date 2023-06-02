# for user stats: date = today
# user = id
# based on id -> usergames
# based on usergames -> game for time and opponent id
from app.app.models import Game, UserGames


def get_user_stats(current_user):
    user_games = UserGames.query.filter_by(user_id=current_user.id).join(Game).all()
    breakpoint()
    return user_games
