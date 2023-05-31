"""Initial migration

Revision ID: d66390af6709
Revises:
Create Date: 2023-05-30 15:08:45.857816

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d66390af6709"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=30), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "idle",
                "waiting_for_game",
                "in_game",
                name="userstate",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_1_id", sa.Integer(), nullable=False),
        sa.Column("player_2_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "in_progess", "ended", name="gamestatus", create_type=False
            ),
            nullable=True,
        ),
        sa.Column("time_in_seconds", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_1_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["player_2_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "usergames",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM("win", "lose", "tie", name="gameresult", create_type=False),
            nullable=True,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("usergames")
    op.drop_table("games")
    op.drop_table("users")
    # ### end Alembic commands ###