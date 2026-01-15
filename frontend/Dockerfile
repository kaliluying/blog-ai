# ========== 前端构建阶段 ==========
FROM node:22-alpine AS builder

# 安装依赖
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci

# 复制源代码并构建
COPY frontend/ .
RUN npm run build

# ========== 生产阶段 ==========
FROM nginx:alpine

# 清理默认配置
RUN rm -rf /etc/nginx/conf.d/default.conf

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制自定义 Nginx 配置
COPY frontend/nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
