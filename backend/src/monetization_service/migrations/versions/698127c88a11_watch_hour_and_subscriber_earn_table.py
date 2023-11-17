"""watch_hour and subscriber_earn table

Revision ID: 698127c88a11
Revises: 0435f6526985
Create Date: 2023-11-13 18:05:25.101264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '698127c88a11'
down_revision = '0435f6526985'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriber_earn',
    sa.Column('user_email', sa.String(), nullable=False, comment='User email of the linked channel'),
    sa.Column('subscriber_earn', sa.Float(), nullable=False, comment='Subscriber earn'),
    sa.Column('id', sa.UUID(), nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Creation date'),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Modified date'),
    sa.ForeignKeyConstraint(['user_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('watch_hour_earn',
    sa.Column('user_email', sa.String(), nullable=False, comment='User email of the linked channel'),
    sa.Column('watch_hour', sa.Float(), nullable=False, comment='Watch hour'),
    sa.Column('id', sa.UUID(), nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Creation date'),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Modified date'),
    sa.ForeignKeyConstraint(['user_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watch_hour_earn')
    op.drop_table('subscriber_earn')
    # ### end Alembic commands ###
