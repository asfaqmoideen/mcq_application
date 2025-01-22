"""Add UserHistoryDetail table and update UserHistory model

Revision ID: 15f7c001ff58
Revises: 96cd159c6b79
Create Date: 2025-01-20 20:28:01.258686

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "15f7c001ff58"
down_revision: Union[str, None] = "96cd159c6b79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the user_history_details table
    op.create_table(
        "user_history_details",
        sa.Column(
            "detail_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        ),
        sa.Column("history_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mcq_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_answer", sa.String(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["history_id"], ["user_history.history_id"]),
        sa.ForeignKeyConstraint(["mcq_id"], ["mcqs.mcq_id"]),
    )

    # Drop the details column from the user_history table
    op.drop_column("user_history", "details")


def downgrade():
    # Add the details column back to the user_history table
    op.add_column("user_history", sa.Column("details", sa.JSON(), nullable=False))

    # Drop the user_history_details table
    op.drop_table("user_history_details")
