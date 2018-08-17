#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Eric

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os.path
from .logger import Logger
import time

logger = Logger(logger='BasePage').getlog()


class BasePage(object):
    
    def __init__(self, driver):
        """
        :param driver:打开浏览器驱动
        """
        self.driver = driver

    def get_page_title(self):
        """获取页面title"""
        logger.info("当前页面的title为： %s" % self.driver.title)
        return self.driver.title
    
    def find_element(self, *loc):
        try:
            # 元素可见时，返回查找到的元素；以下入参为元组的元素，需要加*
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            logger.warning('找不到定位元素: %s' % loc[1])
            raise
        except TimeoutException:
            logger.warning('查找元素超市: %s' % loc[1])
    
    def get_screent_img(self):
        """将页面截图下来"""
        file_path = os.path.join(os.path.abspath('.'), 'Screenshots')
        now = time.strftime("%Y-%m-%d_%H_%M_%S_")
        screen_name = os.path.join(file_path, now + '.png')
        try:
            self.driver.get_screent_as_file(screen_name)
            logger.info("页面已截图，截图的路径在项目： /Screenshots/路径下")
        except NameError as ne:
            logger.error("失败截图 %s" % ne)
            self.get_screent_img()
    
    def send_key(self, loc, text):
        logger.info('清空文本框内容: %s' % loc[1])
        self.find_element(*loc).clear()
        time.sleep(0.3)
        logger.info('输入内容方式 by %s: %s' % (loc[0], loc[1]))
        logger.info('输入内容: %s' % text)
        try:
            self.find_element(*loc).send_keys(text)
        except Exception as e:
            logger.error("输入内容失败 %s" % e)
            self.get_screent_img()
    
    def click(self, loc):
        logger.info('点击元素 by %s: %s' % (loc[0], loc[1]))
        try:
            self.find_element(*loc).click()
        except AttributeError as e:
            logger.error("无法点击元素: %s" % e)
            raise

    def clear(self, loc):
        """输入文本框清空操作"""
        element = self.find_element(*loc)
        try:
            element.clear()
            logger.info("清空文本框内容")
        except NameError as e:
            logger.error("清空文本框内容失败: %s" % e)
            self.get_screent_img()

    def move_to_element(self, loc):
        """
        鼠标悬停操作
        Usage:
        element = ('id', 'xxx')
        driver.move_to_element(element)
        """
        element = self.find_element(*loc)
        ActionChains(self.driver).move_to_element(element).perform()

    def back(self):
        """浏览器返回窗口"""
        self.driver.back()
        logger.info('返回上一个页面')
    
    def forward(self):
        """浏览器前进下一个窗口"""
        self.driver.forward()
        logger.info('前进到下一个页面')
        
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info('等待 %d 秒' % seconds)

    def close(self):
        """关闭浏览器"""
        try:
            self.driver.close()
            logger.info('关闭浏览器窗口')
        except NameError as ne:
            logger.error('关闭浏览器窗口失败 %s' % ne)

    def quit(self):
        """退出浏览器"""
        self.driver.quit()

    def get_title(self):
        """获取title"""
        return self.driver.title
    
    def get_text(self, loc):
        """获取文本"""
        element = self.find_element(*loc)
        return element.text
    
    def get_attribute(self, loc, name):
        """获取属性"""
        element = self.find_element(*loc)
        return element.get_attribute(name)
    
    def js_execute(self, js):
        """执行js"""
        return self.driver.execte_script(js)

    def js_focus_element(self, loc):
        """聚焦元素"""
        target = self.find_element(*loc)
        self.driver.execte_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        """滚动到顶部"""
        js = "window.scrollTo(0, 0)"
        self.driver.execte_script(js)

    def js_scroll_end(self):
        """滚动到底部"""
        js = "window.scrollTo(0, document.body.scrollHeight)"
        self.driver.execte_script(js)

    def select_by_index(self, loc, index):
        """通过索引， index是索引第几个，从0开始"""
        element = self.find_element(*loc)
        Select(element).select_by_index(index)

    def select_by_value(self, loc, value):
        """通过value属性"""
        element = self.find_element(*loc)
        Select(element).select_by_value(value)

    def select_by_text(self, loc, text):
        """通过文本值定位"""
        element = self.find_element(*loc)
        Select(element).select_by_visible_text(text)

    def is_text_in_element(self, loc, text, timeout=10):
        """判断文本在元素里，没定位到元素返回False, 定位到元素返回判断结果布尔值"""
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element(loc, text))
        except TimeoutException:
            logger.error("元素没有定位到： %s" % loc)
            return False
        else:
            return result

    def is_text_in_value(self, loc, value, timeout=10):
        """
        判断元素的value值，没定位到元素返回False，定位到元素返回判断结果布尔值
        result = driver.text_in_element(element, text)
        """
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element_value(loc, value))
        except TimeoutException:
            logger.error("元素没有定位到： %s" % loc)
            return False
        else:
            return result

    def is_title(self, title, timeout=10):
        """判断title完全等于"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        """判断title包含"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result
    
    def is_selected(self, loc, timeout=10):
        """判断元素被被选中，返回布尔值"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(loc))
        return result

    def is_selected_be(self, loc, selected=True, timeout=10):
        """
        判断元素的状态，selected是期望的参数True/False
        返回布尔值
        """
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(loc, selected))
        return result

    def is_alert_present(self, timeout=10):
        """
        判断页面是否有alert
        有，返回alert(注意这里返回alert，不是True)
        没有，返回False
        """
        result = WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        return result
    
    def is_visibility(self, loc, timeout=10):
        """元素可见返回本身，不可见返回False"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(loc))
        return result

    def is_invisibility(self, loc, timeout=10):
        """元素可见返回本身，不可见返回True,没找到元素也返回True"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(loc))
        return result

    def is_clickable(self, loc, timeout=10):
        """元素可以点击返回本身，不可以点击返回False"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(loc))
        return result

    def is_located(self, loc, timeout=10):
        """判断元素有没有被定位到（并不意味着可见），定位到返回element，没定位到但会False"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(loc))
        return result
