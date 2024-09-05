import login_codemao as lcmao
import re
import time
import threading

from selenium.webdriver.common.by import By#pip install selemium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as toe
from selenium.common.exceptions import NoSuchElementException as noee


class 自动化脚本接口:
    # 初始化
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.列表内容 = []
        

    def 打开作品(self,网址):
        self.driver.get(网址)
        self.wait = WebDriverWait(self.driver, 10)
        print("已进入目标网址,接下来您需要打开nemo端的自动化应用脚本")
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
            except  (toe,noee):
                if retry_ >= 10:
                    raise lcmao.定位控件失败("多次定位编程猫作品启动按钮尝试失败，请检查网络后重试。\n如果仍然失败, 可能是程序版本过于落后。")
                print("定位启动按钮失败, 正在尝试重新定位")
                time.sleep(2.5)

    def 置接口列表(self,list_XPATH: str,更新一次延时=0.5):
        """实时获取接口的列表"""
        t = threading.Thread(target=读取列表,args=(self,list_XPATH, 更新一次延时))
        t.start() # 使用多线程


def 读取列表(self:自动化脚本接口,list_XPATH: str,更新一次延时):
    self.list_all = self.driver.find_element(By.XPATH, list_XPATH)
    while True :
        列表内容 = []
        try:
            list_new_ = self.list_all.find_elements(By.CSS_SELECTOR, '.list-value')
            for list_one in list_new_ :
                html_text = list_one.get_attribute('outerHTML')
                pattern = r'(?<=<span class="list-value">).*(?=</span>)' # 使用正则匹配处理列表项的HTML文本
                match = re.search(pattern, html_text).group()
                列表内容.append(match)
            self.列表内容 = 列表内容
        except (noee,toe,IndexError):
            print("错误,未找到该列表")
            time.sleep(0.5)
            pass
        time.sleep(更新一次延时)
