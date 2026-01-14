"""时间工具模块"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    获取当前 UTC 时间

    返回不带时区信息的 datetime 对象（naive datetime），
    以确保与 PostgreSQL 的 timestamp 类型兼容。

    Returns:
        datetime: 当前 UTC 时间（无时区）
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
