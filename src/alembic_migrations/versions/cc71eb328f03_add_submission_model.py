"""add submission model

Revision ID: cc71eb328f03
Revises: 15f7c001ff58
Create Date: 2025-02-04 08:06:50.901997

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "cc71eb328f03"
down_revision: Union[str, None] = "15f7c001ff58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "submissions",
        sa.Column(
            "submission_id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.user_id"),
            nullable=True,
        ),
        sa.Column("total_questions", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
    )

    op.add_column(
        "user_history",
        sa.Column(
            "submission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("submissions.submission_id"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("user_history", "submission_id")
    op.drop_table("submissions")
