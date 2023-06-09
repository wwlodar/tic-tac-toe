"""remove user status

Revision ID: 843892171177
Revises: bc22ca9d006d
Create Date: 2023-06-02 18:59:25.460517

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "843892171177"
down_revision = "bc22ca9d006d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("games", schema=None) as batch_op:
        batch_op.alter_column(
            "date_ended",
            existing_type=postgresql.TIMESTAMP(),
            type_=sa.DateTime(timezone=True),
            existing_nullable=True,
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("status")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "status",
                postgresql.ENUM(
                    "idle", "waiting_for_game", "in_game", name="userstate"
                ),
                autoincrement=False,
                nullable=False,
            )
        )

    with op.batch_alter_table("games", schema=None) as batch_op:
        batch_op.alter_column(
            "date_ended",
            existing_type=sa.DateTime(timezone=True),
            type_=postgresql.TIMESTAMP(),
            existing_nullable=True,
        )

    # ### end Alembic commands ###
