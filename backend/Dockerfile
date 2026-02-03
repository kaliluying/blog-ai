# ========== 后端构建阶段 ==========
FROM python:3.12-slim AS builder

# 安装 build 依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 uv
RUN pip install --no-cache-dir uv

# 安装项目依赖
COPY backend/pyproject.toml ./
RUN uv pip install --system -r pyproject.toml

# ========== 生产阶段 ==========
FROM python:3.12-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从 builder 复制已安装的包
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用代码
COPY backend/ .

# 创建数据库表（运行时由 main.py 处理）
RUN chmod +x /app/entrypoint.sh || true

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
