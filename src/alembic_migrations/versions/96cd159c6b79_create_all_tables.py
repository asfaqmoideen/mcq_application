"""Create all tables

Revision ID: 96cd159c6b79
Revises:
Create Date: 2025-01-07 15:02:41.852803

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "96cd159c6b79"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

userrole = postgresql.ENUM("admin", "user", name="userrole")


def upgrade():
    op.create_table(
        "users",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("admin", "user", name="userrole"),
            nullable=False,
            server_default="user",
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP(), server_default=sa.func.current_timestamp()
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "mcqs",
        sa.Column("mcq_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("question", sa.String(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_option", sa.String(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at", sa.TIMESTAMP(), server_default=sa.func.current_timestamp()
        ),
        sa.PrimaryKeyConstraint("mcq_id"),
        sa.ForeignKeyConstraint(["created_by"], ["users.user_id"]),
        sa.UniqueConstraint("question"),
    )

    op.create_table(
        "user_history",
        sa.Column("history_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("total_score", sa.Float(), nullable=False),
        sa.Column("percentage", sa.Float(), nullable=False),
        sa.Column("total_attempts", sa.Integer(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column(
            "attempted_at", sa.TIMESTAMP(), server_default=sa.func.current_timestamp()
        ),
        sa.PrimaryKeyConstraint("history_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
    )


def downgrade():
    userrole.drop(op.get_bind(), checkfirst=True)
    op.drop_table("mcqs")
    op.drop_table("user_history")
    op.drop_table("users")
    op.execute("DROP TYPE userrole")
