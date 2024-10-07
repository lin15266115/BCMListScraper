import login_codemao as lcmao
import re
import time
import threading

from selenium.webdriver.common.by import By #pip install selemium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException as sere
from selenium.common.exceptions import TimeoutException as toe
from selenium.common.exceptions import NoSuchElementException as nsee
from typing import Callable

class 接口列表:
    def __init__(self,list_XPATH: str
                ,driver: WebDriver
                ,更新一次延时: float = 0.02
                ) -> None:
        self.driver = driver
        self.销毁 = False
        self.列表内容 = []
        self.XPATH =list_XPATH
        self.refresh_delay_time = 更新一次延时

    def 置接口列表(self):
        """实时获取接口的列表"""
        t = threading.Thread(target=self.读取列表,args=(self.XPATH,self.refresh_delay_time))
        t.start() # 使用多线程
        return t

    def 销毁列表(self):
        self.销毁 = True

    def 读取列表(self ,list_XPATH: str,更新一次延时):
        retry_ = 0
        while retry_ <= 10 :
            try:
                self.list_all = self.driver.find_element(By.XPATH, list_XPATH)
                break
            except (nsee,toe,IndexError):
                print("错误,未找到该列表",end="")
                time.sleep(0.5)
                retry_ += 1
                if retry_ >= 10:
                    raise ValueError("没有找到您提供的列表位置")
                else:
                    print("重试定位列表{retry_}/10")
    
        while True :
            列表内容 = []
            list_new_ = self.list_all.find_elements(By.CSS_SELECTOR, '.list-value')
            for list_one in list_new_ :
                try:
                   html_text = list_one.get_attribute('outerHTML')
                except sere:
                    print("元素已过期，无法获取其 outerHTML 属性")
                pattern = r'(?<=<span class="list-value">).*(?=</span>)' # 使用正则匹配处理列表项的HTML文本
                match = re.search(pattern, html_text).group()
                列表内容.append(match)
            self.列表内容 = 列表内容
    
            while self.销毁:
                break
            time.sleep(更新一次延时)
    

class 自动化脚本接口:
    # 初始化
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.列表内容 = []
        self.销毁列表 = False
        self.AllList: list[接口列表] = []

    def 打开作品(self,网址):
        self.driver.get(网址)
        self.wait = WebDriverWait(self.driver, 10)
        print("已进入目标网址,接下来您需要打开nemo端的自动化应用脚本")
        self.按下开始按钮()

    def 置接口列表(self,list_XPATH,更新一次延时:float = 0.02):
        list_ =接口列表(list_XPATH,self.driver,更新一次延时)
        list_.置接口列表()
        self.AllList.append(list_)
        return list_

    def 按下开始按钮(self):
        retry_ = 0
        while 1 :
            retry_ += 1
            try :
                # 定位到作品开始按钮
                container = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".CUI-player-cover-play-btn")))
                # 按下启动按钮
                # 退出循环
                container[0].click()
                break
            except  (toe,nsee,IndexError):
                if retry_ >= 10:
                    raise lcmao.定位控件失败("多次定位编程猫作品启动按钮尝试失败，请检查网络后重试。\n如果仍然失败, 可能是程序版本过于落后。")
                print("定位启动按钮失败, 正在尝试重新定位{retry_}")
                time.sleep(2.5)

    def 重新进入作品(self,启动接口的函数:Callable = None, args:tuple = None, kwargs:dict = None) :
        for list in self.AllList:
            list.销毁列表()
        self.driver.refresh()
        self.按下开始按钮()
        if args is not None and kwargs is not None:
            启动接口的函数(*args, **kwargs)
        elif args is not None:
            启动接口的函数(*args)
        elif kwargs is not None:
            启动接口的函数(**kwargs)
        else:
            启动接口的函数()
        for list in self.AllList:
            list.置接口列表()

if __name__ == "__main__" :
    pass