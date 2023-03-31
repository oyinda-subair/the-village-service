"""Create post schema

Revision ID: b13b7f6a65e5
Revises: add04d2b2bc4
Create Date: 2022-10-15 03:24:31.920749

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = 'b13b7f6a65e5'
down_revision = 'add04d2b2bc4'
branch_labels = None
depends_on = 'add04d2b2bc4'


def upgrade() -> None:
    op.create_table('post',
                    sa.Column("id", UUID(), nullable=False, default=uuid.uuid4),
                    sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("description", sa.Text(), nullable=True),
                    sa.Column("content", sa.Text(), nullable=False),
                    sa.Column("category", sa.String(), nullable=False),
                    sa.Column("image_url", sa.String(), nullable=True),
                    sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
                    sa.Column("updated_at", sa.TIMESTAMP, nullable=True, server_default=sa.func.now()),
                    sa.PrimaryKeyConstraint("id"),
                    sa.ForeignKeyConstraint(('user_id',), ['user.id'], ondelete='CASCADE'),
                    sa.UniqueConstraint('title')
                    )

    op.create_index('ix_user_id', 'post', ['user_id'], unique=False)
    op.create_index('ix_post_title', 'post', ['title'], unique=False)
    # op.create_unique_constraint('unique_title', 'post', ['title'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # op.drop_index(op.f('ix_post_id'), table_name='post')
    op.drop_index(op.f('ix_user_id'), table_name='post')
    op.drop_index(op.f('ix_post_title'), table_name='post')
    # op.drop_constraint("unique_title", "post")

    op.drop_table('post')
