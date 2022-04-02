#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: LiuKun
# date:   2022-04-01

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
