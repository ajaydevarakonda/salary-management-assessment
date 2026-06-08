"""add currency to employees

Revision ID: a1b2c3d4e5f6
Revises: 533df0f1f59a
Create Date: 2026-06-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "533df0f1f59a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "employees",
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="USD"),
    )
    op.alter_column("employees", "currency", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("employees", "currency")
