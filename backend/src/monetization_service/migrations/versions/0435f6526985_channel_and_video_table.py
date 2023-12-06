"""channel_and_video_table

Revision ID: 0435f6526985
Revises: fad5080477ee
Create Date: 2023-11-10 22:44:08.560731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0435f6526985'
down_revision = 'fad5080477ee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel',
    sa.Column('user_email', sa.String(), nullable=False, comment='User email of the linked channel'),
    sa.Column('channel_name', sa.String(), nullable=False, comment='Channel name'),
    sa.Column('channel_link', sa.String(), nullable=False, comment='Channel link'),
    sa.Column('is_selected', sa.Boolean(), nullable=False, comment='Channel is selected or not'),
    sa.Column('id', sa.UUID(), nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Creation date'),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Modified date'),
    sa.ForeignKeyConstraint(['user_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('video',
    sa.Column('user_email', sa.String(), nullable=False, comment='User email of the linked video'),
    sa.Column('video_link', sa.String(), nullable=False, comment='Video link'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='Video is activated or not'),
    sa.Column('id', sa.UUID(), nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Creation date'),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Modified date'),
    sa.ForeignKeyConstraint(['user_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint("user_vid_channel", 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("user_vid_channel", 'user', type_='unique')
    op.drop_table('video')
    op.drop_table('channel')
    # ### end Alembic commands ###
