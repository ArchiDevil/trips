"""Switch user types

Revision ID: 9f8cd26e465e
Revises: 925e172cea3a
Create Date: 2022-06-02 00:10:52.423810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f8cd26e465e'
down_revision = '925e172cea3a'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("ALTER TYPE accessgroup RENAME TO accessgroup_old")
    op.execute("ALTER TYPE accessgroup_old RENAME VALUE 'TripManager' TO 'User'")

    op.execute("UPDATE users SET access_group = 'User' WHERE access_group = 'Guest'::accessgroup_old")

    op.execute("CREATE TYPE accessgroup AS ENUM ('User', 'Administrator')")
    op.execute("ALTER TABLE users ALTER COLUMN access_group TYPE accessgroup USING access_group::text::accessgroup")
    op.execute("DROP TYPE accessgroup_old")


def downgrade() -> None:
    op.execute("ALTER TYPE accessgroup RENAME TO accessgroup_old")
    op.execute("ALTER TYPE accessgroup_old RENAME VALUE 'User' TO 'TripManager'")
    op.execute("CREATE TYPE accessgroup AS ENUM ('Guest', 'TripManager', 'Administrator')")
    op.execute("ALTER TABLE users ALTER COLUMN access_group TYPE accessgroup USING access_group::text::accessgroup")
    op.execute("DROP TYPE accessgroup_old")
