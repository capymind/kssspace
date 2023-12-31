"""empty message

Revision ID: 5a92b17adc15
Revises: 15685d598198
Create Date: 2023-12-01 13:41:46.299785

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5a92b17adc15'
down_revision: Union[str, None] = '15685d598198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schema_migration')
    with op.batch_alter_table('giant', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.create_unique_constraint('giant_uq_1', ['name'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('giant', schema=None) as batch_op:
        batch_op.drop_constraint('giant_uq_1', type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    op.create_table('schema_migration',
    sa.Column('onerow_id', sa.BOOLEAN(), server_default=sa.text('(TRUE)'), nullable=True),
    sa.Column('data_loaded', sa.BOOLEAN(), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('onerow_id', name='onerow_uni'),
    sa.PrimaryKeyConstraint('onerow_id')
    )
    # ### end Alembic commands ###
