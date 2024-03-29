"""Initial state of the database

Revision ID: dbfec4efa1d5
Revises:
Create Date: 2023-04-29 22:15:03.002662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbfec4efa1d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('calories', sa.Float(), nullable=False),
                    sa.Column('proteins', sa.Float(), nullable=False),
                    sa.Column('fats', sa.Float(), nullable=False),
                    sa.Column('carbs', sa.Float(), nullable=False),
                    sa.Column('grams', sa.Float(), nullable=True),
                    sa.Column('archived', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('login', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.Column('displayed_name', sa.String(), nullable=True),
                    sa.Column('access_group', sa.Enum('User', 'Administrator',
                                                      name='accessgroup'), nullable=False),
                    sa.Column('user_type', sa.Enum('Native', 'Vk',
                                                   name='usertype'), nullable=False),
                    sa.Column('last_logged_in', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('passwordlinks',
                    sa.Column('uuid', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('expiration_date',
                              sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('trips',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('from_date', sa.Date(), nullable=False),
                    sa.Column('till_date', sa.Date(), nullable=False),
                    sa.Column('created_by', sa.Integer(), nullable=False),
                    sa.Column('last_update', sa.DateTime(), nullable=False),
                    sa.Column('archived', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('vkusers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('user_token', sa.String(), nullable=False),
                    sa.Column('token_exp_time', sa.DateTime(), nullable=False),
                    sa.Column('photo_url', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id', 'user_id')
                    )
    op.create_table('groups',
                    sa.Column('trip_id', sa.Integer(), nullable=False),
                    sa.Column('group_number', sa.Integer(), nullable=False),
                    sa.Column('persons', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ),
                    sa.PrimaryKeyConstraint('trip_id', 'group_number')
                    )
    op.create_table('meal_records',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('trip_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('day_number', sa.Integer(), nullable=False),
                    sa.Column('meal_number', sa.Integer(), nullable=False),
                    sa.Column('mass', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('sharinglinks',
                    sa.Column('uuid', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('trip_id', sa.Integer(), nullable=True),
                    sa.Column('expiration_date',
                              sa.DateTime(), nullable=False),
                    sa.Column('access_type', sa.Enum('Read', 'Write',
                                                     name='tripaccesstype'), nullable=False),
                    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('tripaccess',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('trip_id', sa.Integer(), nullable=False),
                    sa.Column('access_type', sa.Enum('Read', 'Write',
                                                     name='tripaccesstype'), nullable=False),
                    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'trip_id')
                    )


def downgrade() -> None:
    op.drop_table('tripaccess')
    op.drop_table('sharinglinks')
    op.drop_table('meal_records')
    op.drop_table('groups')
    op.drop_table('vkusers')
    op.drop_table('trips')
    op.drop_table('passwordlinks')
    op.drop_table('users')
    op.drop_table('products')
