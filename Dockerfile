# 基础镜像
FROM python:3.9-alpine
# 作者信息
LABEL LIUKUN="liukunup@outlook.com"

# 默认时区
ARG TIMEZONE="Asia/Shanghai"
ENV TZ ${TIMEZONE}

# FLASK框架配置
ENV FLASK_APP main.py
ENV FLASK_CONFIG docker

# 设置超级管理员
ENV SUPER_ADMIN Administrator

# 数据库配置
ENV MYSQL_HOST 127.0.0.1
ENV MYSQL_PORT 3306
ENV MYSQL_USERNAME root
ENV MYSQL_PASSWORD 123456
ENV MYSQL_DATABASE database

# 工作路径
WORKDIR /home/FlaskBoot

# 环境部署
COPY requirements requirements
RUN    python -m venv venv \
    && venv/bin/python3 -m pip install --upgrade pip \
    && . venv/bin/activate \
    && venv/bin/pip install -r requirements/docker.txt

# 拷贝源文件
COPY server server
COPY migrations migrations
COPY main.py entrypoint.sh ./

# 端口暴露
EXPOSE 5000

# 程序入口
ENTRYPOINT ["./entrypoint.sh"]
