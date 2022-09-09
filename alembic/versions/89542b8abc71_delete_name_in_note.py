"""delete name in Note

Revision ID: 89542b8abc71
Revises: 52eb45fd326d
Create Date: 2022-09-06 11:27:38.890992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89542b8abc71'
down_revision = '52eb45fd326d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('name', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    # ### end Alembic commands ###