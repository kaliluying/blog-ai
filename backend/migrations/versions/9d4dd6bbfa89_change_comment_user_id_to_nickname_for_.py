"""Change comment user_id to nickname for anonymous comments

Revision ID: 9d4dd6bbfa89
Revises: 0e969687e30b
Create Date: 2026-01-14 22:38:15.707124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by alembic.
revision: str = '9d4dd6bbfa89'
down_revision: Union[str, Sequence[str], None] = '0e969687e30b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: change user_id to nickname for anonymous comments."""
    # 添加新 nickname 列
    op.add_column('comments', sa.Column('nickname', sa.String(50), nullable=False, server_default='匿名用户'))

    # 更新现有记录的 nickname（设置为 '匿名用户' 作为默认值）
    op.execute("UPDATE comments SET nickname = '匿名用户' WHERE nickname IS NULL")

    # 删除旧的 user_id 列
    op.drop_index(op.f('ix_comments_user_id'), table_name='comments')
    op.drop_column('comments', 'user_id')


def downgrade() -> None:
    """Downgrade schema: revert nickname back to user_id."""
    # 添加回 user_id 列
    op.add_column('comments', sa.Column('user_id', sa.INTEGER(), nullable=False, server_default='0'))
    op.create_index(op.f('ix_comments_user_id'), 'comments', ['user_id'], unique=False)

    # 删除 nickname 列
    op.drop_column('comments', 'nickname')
