"""Added points

Revision ID: 6cf7671a83da
Revises: 2382738a92d6
Create Date: 2023-05-30 18:14:28.696239

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6cf7671a83da"
down_revision = "2382738a92d6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("added_points", sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("added_points")

    # ### end Alembic commands ###
