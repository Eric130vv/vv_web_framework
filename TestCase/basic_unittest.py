#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Eric

import unittest
from Librarys.logger import Logger


class basic_unittest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger(logger='测试用例').getlog()
        cls.logger.info('--------测试开始--------')
    
    @classmethod
    def tearDownClass(cls):
        cls.logger.info('--------测试结束--------')
