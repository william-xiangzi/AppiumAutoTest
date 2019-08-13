#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 装饰器:函数被装饰后 再次调用时 会一并调用装饰器
# 装饰器用法相当于 fun_test = decorator(fun_test)
# https://blog.csdn.net/gezailushang/article/details/84291092

from functools import wraps


def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction


class ShowFunName(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print('function name:', self._func.__name__)
        return self._func(self)


class ShowClassName(object):
    def __init__(self, func):
        self._cls = func

    def __call__(self):
        print('class name:', self._cls.__name__)
        return self._cls(self)


# @a_new_decorator
# def decoratortest():
#     print("TestAdorner")
#
# decoratortest()


class logit(object):
    def __init__(self, func):
        self.func = func

    def __call__(self):
        @wraps(self.func)
        def wrapped_function(*args, **kwargs):
            print("Now in logit __call__" + self.__name__ )
            return self.func(*args, **kwargs)
        return wrapped_function

    def notify(self):
        # logit只打日志，不做别的
        pass



class Newtest(object):
    def __init__(self):
        pass

    @staticmethod
    @ShowFunName
    def decoratest(self):
        print("There is in class newtest def decoratest")
        return "Now in decoratest"


test = Newtest()
test.decoratest()

print(test.decoratest)
