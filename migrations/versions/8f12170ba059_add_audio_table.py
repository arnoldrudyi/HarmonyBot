"""add audio table

Revision ID: 8f12170ba059
Revises: 3157410d2bc3
Create Date: 2023-07-30 01:36:28.256845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f12170ba059'
down_revision = '3157410d2bc3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=512), nullable=False),
    sa.Column('unique_id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('unique_id'),
    sa.UniqueConstraint('url')
    )
    op.create_unique_constraint(None, 'accounts', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'accounts', type_='unique')
    op.drop_table('audios')
    # ### end Alembic commands ###
