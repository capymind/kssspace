"""empty message

Revision ID: d15848920f3b
Revises: 5a92b17adc15
Create Date: 2023-12-01 15:53:58.401149

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd15848920f3b'
down_revision: Union[str, None] = '5a92b17adc15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schema_migration')
    with op.batch_alter_table('giant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('github', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('mastodon', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('giant', schema=None) as batch_op:
        batch_op.drop_column('mastodon')
        batch_op.drop_column('github')

    op.create_table('schema_migration',
    sa.Column('onerow_id', sa.BOOLEAN(), server_default=sa.text('(TRUE)'), nullable=True),
    sa.Column('data_loaded', sa.BOOLEAN(), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('onerow_id', name='onerow_uni'),
    sa.PrimaryKeyConstraint('onerow_id')
    )
    # ### end Alembic commands ###
