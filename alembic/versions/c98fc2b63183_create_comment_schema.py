"""Create comment schema

Revision ID: c98fc2b63183
Revises: b13b7f6a65e5
Create Date: 2022-10-15 16:29:22.294365

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = 'c98fc2b63183'
down_revision = 'b13b7f6a65e5'
branch_labels = None
depends_on = 'b13b7f6a65e5'


def upgrade() -> None:
    op.create_table('post',
                    sa.Column("id", UUID(), nullable=False, default=uuid.uuid4),
                    sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
                    sa.Column("post_id", UUID(as_uuid=True), sa.ForeignKey('post.id', ondelete='CASCADE'), nullable=False),
                    sa.Column("content", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
                    sa.Column("updated_at", sa.TIMESTAMP, nullable=True, server_default=sa.func.now()),
                    sa.PrimaryKeyConstraint("id"),
                    sa.ForeignKeyConstraint(('user_id',), ['user.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(('post_id',), ['post.id'], ondelete='CASCADE')
                    )

    op.create_index('ix_comment_id', 'comment', ['id'], unique=False)
    op.create_index('ix_user_id', 'comment', ['user_id'], unique=False)
    op.create_index('ix_post_id', 'comment', ['post_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_comment_id'), table_name='comment')
    op.drop_index(op.f('ix_user_id'), table_name='comment')
    op.drop_index(op.f('ix_post_id'), table_name='comment')

    op.drop_table('comment')
