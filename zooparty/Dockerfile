FROM python:3.9-slim

WORKDIR /app

# 复制项目文件
COPY . .

# 安装系统依赖和Python包
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask paramiko

EXPOSE 5000

CMD ["python", "app.py"]