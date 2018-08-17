#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Eric

import os.path
from selenium import webdriver
from Librarys.logger import Logger
import yaml

logger = Logger(logger="BrowserDriver").getlog()

class BrowserDriver(object):
    # 获取相对路径
    base_path = os.path.abspath('.')
    driver_path = os.path.join(base_path, 'Drivers')
    chrome_driver = os.path.join(driver_path, 'chromedriver.exe')
    ie_driver = os.path.join(driver_path, 'IEDriverServer.exe')

    def __init__(self, driver):
        self.driver = driver
    
    def openbrowser(self, driver):
        # 读取配置文件
        file_path = os.path.join(self.base_path, 'conf')
        file_name = os.path.join(file_path, 'config.yaml')
        with open(file_name, 'r') as f:
            config = yaml.load(f.read())
        # 获取配置文件属性
        browser = config['browserType']['browserName']
        logger.info("选择的浏览器为: %s 浏览器" % browser)
        url = config['testUrl']['URL']
        logger.info("打开的URL为: %s" % url)
        if browser == "Firefox":
            driver = webdriver.Firefox()
            logger.info("启动火狐浏览器")
        elif browser == "Chrome":
            driver = webdriver.Chrome(self.chrome_driver)
            logger.info("启动谷歌浏览器")
        elif browser == "IE":
            driver = webdriver.Ie(self.ie_driver)
            logger.info("启动IE浏览器")

        driver.get(url)
        logger.info("打开URL: %s" % url)
        driver.maximize_window()
        logger.info("全屏当前窗口")
        driver.implicitly_wait(10)
        logger.info("设置10秒隐式等待时间")
        return driver
    
    def quit_browser(self):
        logger.info("关闭浏览器")
        self.driver.quit()
