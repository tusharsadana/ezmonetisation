
"""initial_migration

Revision ID: fad5080477ee
Revises: 
Create Date: 2023-11-08 20:33:07.382355

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'fad5080477ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(), nullable=False, comment='Email of user'),
    sa.Column('first_name', sa.String(), nullable=True, comment='First Name of user'),
    sa.Column('last_name', sa.String(), nullable=True, comment='Last Name of user'),
    sa.Column('user_type', sa.Integer(), nullable=False, comment='User Type'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='Is this user active or not'),
    sa.Column('password', sqlalchemy_utils.types.password.PasswordType(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Creation date'),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Modified date'),
    sa.PrimaryKeyConstraint('email'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
