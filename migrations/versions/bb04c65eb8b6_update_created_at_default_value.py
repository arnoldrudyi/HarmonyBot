"""update created_at default value

Revision ID: bb04c65eb8b6
Revises: 8f12170ba059
Create Date: 2023-08-09 15:35:42.884559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb04c65eb8b6'
down_revision = '8f12170ba059'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE audios ALTER COLUMN created_at SET DEFAULT NOW()")

    op.execute("ALTER TABLE accounts ALTER COLUMN created_at SET DEFAULT NOW()")

    op.create_unique_constraint('uq_audios_created_at', 'audios', ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_constraint('uq_audios_created_at', 'audios', type_='unique')

    op.execute("ALTER TABLE accounts ALTER COLUMN created_at SET DEFAULT NULL")

    op.execute("ALTER TABLE audios ALTER COLUMN created_at SET DEFAULT NULL")
    # ### end Alembic commands ###
