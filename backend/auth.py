"""
认证模块

提供密码哈希、JWT 令牌生成和验证功能。
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from pwdlib import PasswordHash

import os
from dotenv import load_dotenv

load_dotenv()

# 密码哈希器（使用推荐的 Argon2 算法）
password_hash = PasswordHash.recommended()

# JWT 配置
SECRET_KEY: str = os.getenv("JWT_SECRET", "")
if not SECRET_KEY:
    # 使用安全的默认密钥（仅开发环境使用）
    import secrets

    SECRET_KEY = secrets.token_hex(32)
    import warnings

    warnings.warn(
        "JWT_SECRET not set, using auto-generated secret key. "
        "Set JWT_SECRET in .env for production use.",
        UserWarning,
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_EXPIRE_MINUTES", "1440")
)  # 默认 24 小时

# 管理员密码
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")  # 可选的预哈希密码


def verify_admin_password(password: str) -> bool:
    """验证管理员密码

    支持两种验证方式：
    1. 如果设置了 ADMIN_PASSWORD_HASH，使用 Argon2 哈希验证
    2. 否则使用明文比较（向后兼容）
    """
    if ADMIN_PASSWORD_HASH:
        # 使用 Argon2 哈希验证
        return password_hash.verify(password, ADMIN_PASSWORD_HASH)
    else:
        # 明文比较（向后兼容）
        return password == ADMIN_PASSWORD


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配"""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT 访问令牌

    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量

    Returns:
        str: JWT 令牌字符串
    """
    to_encode = data.copy()

    # 确保 sub 是字符串（JWT 标准要求）
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    解码 JWT 令牌

    Args:
        token: JWT 令牌字符串

    Returns:
        dict: 解码后的数据

    Raises:
        HTTPException: 令牌无效或过期
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_admin_token(token: str) -> bool:
    """
    验证管理员 JWT 令牌

    Args:
        token: JWT 令牌字符串

    Returns:
        bool: 令牌有效返回 True，无效返回 False
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 检查是否是管理员令牌
        return payload.get("type") == "admin"
    except JWTError:
        return False


def create_admin_token() -> str:
    """
    创建管理员 JWT 令牌

    Returns:
        str: JWT 管理员令牌
    """
    return create_access_token({"sub": "admin", "type": "admin"})
