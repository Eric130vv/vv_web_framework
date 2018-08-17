#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Eric

import os
import time
import unittest
from Reports.Runner.HTMLTestRunner3_en import HTMLTestRunner


base_path = os.path.abspath('.')
case_path = os.path.join(base_path, 'TestCase')
result_path = os.path.join(base_path, 'Reports')


def create_suite():
    """创建测试用例集"""
    test_suite = unittest.TestSuite()
    # 查找测试用例目录下符合规则的用例
    discover = unittest.defaultTestLoader.discover(
        start_dir=case_path,
        pattern='*_case.py',
        top_level_dir=None
    )

    for test_case in discover:
        test_suite.addTests(test_case)
    return test_suite


def report_info():
    # 获取系统当前时间
    now = time.strftime("_%Y-%m-%d_%H_%M_%S")
    day = time.strftime("%Y-%m-%d")

    # 定义测试报告每天路径和报告名称
    result_paths = os.path.join(result_path, day)
    file_name = os.path.join(result_paths, 'Result' + now + '.html')
    return result_paths, file_name


def main():
    test_suite = create_suite()
    result_paths, file_name = report_info()
    if not os.path.exists(result_paths):
        os.mkdir(result_paths)
    with open(file_name, 'wb') as fp:
        runner = HTMLTestRunner(
            stream=fp,
            title='自动化测试报告',
            description=''
        )
        runner.run(test_suite)


if __name__ == '__main__':
    main()
