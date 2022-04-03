# Flask-Server

基于Flask框架的服务器开发模板

## 入门第一课

- 配置虚拟环境

```shell
# 切换到此目录
cd Flask-Server
# 创建虚拟环境
python3 -m venv venv
# 激活虚拟环境
. venv/bin/activate
```

- 安装Flask

```shell
pip install Flask
```

- 运行Flask

```shell
export FLASK_APP=main
export FLASK_CONFIG=dev 
export FLASK_ENV=development
flask run
```

按 CTRL+C 关闭上述服务

- 使用MYSQL数据库

```shell
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_USERNAME=root
export MYSQL_PASSWORD=123456
export MYSQL_DATABASE=database
```

- 创建或销毁表

首次使用时需要先新建数据库，并使用如下命令创建表

```shell
flask create
```

如需要删除表

```shell
flask destroy
```

## FAQ

- 5000端口被占用

```text
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.
On macOS, try disabling the 'AirPlay Receiver' service from System Preferences -> Sharing.
```

解决方案一（推荐）

查找哪个程序在占用当前端口，然后杀掉对应的进程即可。

```shell
lsof -i :5000
kill -5 pid
```

解决方案二

启动时设置Port参数，使用其他端口。

```shell
flask run --port=8080
```
