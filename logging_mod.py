# -*- coding: utf-8 -*-
from reusepatterns.singletones import SingletonByName
import time


# Заметка, можно применить стратегию если добавить стратегию логирования
class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text)
