"""时间工具模块"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    获取当前 UTC 时间

    返回带时区信息的 datetime 对象（timezone-aware datetime），
    与 PostgreSQL 的 TIMESTAMP WITH TIME ZONE 类型兼容。

    Returns:
        datetime: 当前 UTC 时间（带时区）
    """
    return datetime.now(timezone.utc)
