"""add column certificate in user_history table

Revision ID: 8af2b7fef7bd
Revises: 68d0dc718854
Create Date: 2025-02-04 19:15:28.968007

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8af2b7fef7bd"
down_revision: Union[str, None] = "68d0dc718854"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_history",
        sa.Column("certificate", sa.String(255), nullable=True),
    )

    op.execute("UPDATE user_history SET certificate = '' WHERE certificate IS NULL")

    op.alter_column("user_history", "certificate", nullable=False)


def downgrade() -> None:
    op.drop_column("user_history", "certificate")
