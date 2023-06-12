"""Add UID for trips

Revision ID: 1daa250ee6c3
Revises: f3b468706c42
Create Date: 2023-04-30 17:21:32.038560

"""
import secrets

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1daa250ee6c3'
down_revision = 'f3b468706c42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    def generate_uid():
        return secrets.token_urlsafe(8)

    op.add_column('trips', sa.Column('uid', sa.String(), unique=True))

    # generate new UIDs
    conn = op.get_bind()
    result = conn.execute('SELECT id FROM trips')
    for row in result:
        conn.execute('UPDATE trips SET uid = %(uid)s WHERE id = %(id)s', {
            'uid': generate_uid(),
            'id': row['id']
        })

    op.alter_column('trips', 'uid', nullable=False)


def downgrade() -> None:
    op.drop_column('trips', 'uid')
