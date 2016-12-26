# -*- coding: utf-8 -*-

import unittest

class MyTest1(unittest.TestCase):
    def __init__(self,name):
        self.name = name

    def test_method_a(self,name=None):
        print('1')
        pass
    def test_method_b(self,name=None):
        print('2')
        pass


