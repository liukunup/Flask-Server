# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022-09-10 22:54:00
# description: Bean

from typing import TypeVar

# 基础类型包装
Integer = TypeVar("Integer", int, None)
Float = TypeVar("Float", float, None)
Bytes = TypeVar("Bytes", bytes, None)


class BaseBean(object):
    """ Bean抽象类 """

    def __init__(self):
        pass
