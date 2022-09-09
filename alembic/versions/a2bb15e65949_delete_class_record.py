"""delete class Record

Revision ID: a2bb15e65949
Revises: 89542b8abc71
Create Date: 2022-09-06 11:32:15.409638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2bb15e65949'
down_revision = '89542b8abc71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('records')
    op.add_column('notes', sa.Column('description', sa.String(length=200), nullable=False))
    op.add_column('notes', sa.Column('done', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'done')
    op.drop_column('notes', 'description')
    op.create_table('records',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('done', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('note_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['note_id'], ['notes.id'], name='records_note_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='records_pkey')
    )
    # ### end Alembic commands ###
