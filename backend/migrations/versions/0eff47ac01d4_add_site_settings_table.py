"""Add site_settings table

Revision ID: 0eff47ac01d4
Revises: 9d4dd6bbfa89
Create Date: 2026-01-21 19:41:29.847595

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0eff47ac01d4"
down_revision: Union[str, Sequence[str], None] = "9d4dd6bbfa89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add site_settings table."""
    op.create_table(
        "site_settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("key", sa.String(100), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("site_settings_pkey")),
        sa.UniqueConstraint("key", name=op.f("site_settings_key_key")),
    )
    op.create_index(op.f("ix_site_settings_id"), "site_settings", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema - drop site_settings table."""
    op.drop_index(op.f("ix_site_settings_id"), table_name="site_settings")
    op.drop_table("site_settings")
