"""user constants

Revision ID: dcf5062af3f9
Revises: 87e4b8e35f1e
Create Date: 2023-11-16 12:01:35.256270

"""
from alembic import op
import sqlalchemy as sa

from src.monetization_service.models.user import UserTypeConstants
from src.monetization_service.queries.table import insert_to_table_by_model

# revision identifiers, used by Alembic.
revision = 'dcf5062af3f9'
down_revision = '87e4b8e35f1e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_type_constants',
    sa.Column('user_type_id', sa.Integer(), nullable=False, comment='User Type ID'),
    sa.Column('user_type_name', sa.String(), nullable=True, comment='User Type name'),
    sa.Column('watch_hour_ratio', sa.Float(), nullable=False, comment='Watch Hour Ratio'),
    sa.Column('subscriber_ratio', sa.Float(), nullable=False, comment='Subscriber Ratio'),
    sa.Column('id', sa.UUID(), nullable=False, comment='ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Creation date'),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Modified date'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_type_id')
    )
    conn = op.get_bind()
    user_type_data = [
        {
            "user_type_id": 0,
            "user_type_name": "Super Admin",
            "watch_hour_ratio": 1,
            "subscriber_ratio": 1,
        },
        {
            "user_type_id": 1,
            "user_type_name": "Free User",
            "watch_hour_ratio": 0.5,
            "subscriber_ratio": 0.5,
        },
        {
            "user_type_id": 2,
            "user_type_name": "Premium User",
            "watch_hour_ratio": 0.9,
            "subscriber_ratio": 0.9,
        }

    ]
    insert_query = insert_to_table_by_model(
        UserTypeConstants, user_type_data
    )
    conn.execute(insert_query)

    op.create_foreign_key(None, 'user', 'user_type_constants', ['user_type'], ['user_type_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_table('user_type_constants')
    # ### end Alembic commands ###
