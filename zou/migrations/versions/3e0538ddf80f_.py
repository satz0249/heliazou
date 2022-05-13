"""add columns: notifications_mattermost_{enabled,userid}

Revision ID: 3e0538ddf80f
Revises: a66508788c53
Create Date: 2021-11-12 15:31:19.621953

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "3e0538ddf80f"
down_revision = "a66508788c53"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person",
        sa.Column(
            "notifications_mattermost_enabled", sa.Boolean(), nullable=True
        ),
    )
    op.add_column(
        "person",
        sa.Column(
            "notifications_mattermost_userid",
            sa.String(length=60),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("person", "notifications_mattermost_userid")
    op.drop_column("person", "notifications_mattermost_enabled")
    # ### end Alembic commands ###
