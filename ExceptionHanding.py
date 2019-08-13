#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functools import wraps
from AppiumStepRunner import AppiumStepRunner

# 写一个函数装饰器 用来处理每个操作步骤之前的异常判断；目前看仅需要写一个；就是登陆的函数装饰器
# 异常判断不能写类装饰器；写作类装饰器后没办法被类函数调用


# 思路所有的异常处理可以封装成这一个类；在 __call__ 里判断需要处理哪个异常 调用对应函数即可
# 权限弹窗处理需要判断是否有弹窗 知道没有权限弹窗时停止
class Authorizewinwow(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        pass



class ExceptionHanding(object):
    def __init__(self):
        pass

    def loginhanding(self):
        pass
