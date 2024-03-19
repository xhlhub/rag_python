# 使用官方Python基础镜像，这里以Python 3.10为例
FROM python:3.10-slim-buster

# 设置工作目录
WORKDIR /app

# 复制项目所需的文件到镜像的工作目录
COPY requirements.txt .
COPY . .

# 安装项目依赖
RUN python -m venv /opt/venv
RUN pip install --no-cache-dir -r requirements.txt


# 设置环境变量（如果需要的话）
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露容器内的端口（比如Web应用的80端口）
EXPOSE 3001

# 定义容器启动时执行的命令
CMD ["python", "main.py"]