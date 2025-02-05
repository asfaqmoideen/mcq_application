"""add column type in submission table

Revision ID: 68d0dc718854
Revises: cc71eb328f03
Create Date: 2025-02-04 13:21:47.864301

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "68d0dc718854"
down_revision: Union[str, None] = "cc71eb328f03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "submissions",
        sa.Column("type", sa.String(), nullable=False, server_default="None"),
    )


def downgrade() -> None:
    op.drop_column("submissions", "type")
