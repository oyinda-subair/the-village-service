"""create user schema

Revision ID: add04d2b2bc4
Revises:
Create Date: 2022-09-01 13:02:25.321894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add04d2b2bc4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=256), nullable=True),
        sa.Column("surname", sa.String(length=256), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')