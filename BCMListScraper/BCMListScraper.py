import login_codemao as lcmao
import re
import time

from colorama.ansi import Fore, Style

from selenium import webdriver #pip install selemium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as toe
from selenium.common.exceptions import NoSuchElementException as noee


class 自动化脚本接口:
    # 初始化
    def __init__(self, driver: WebDriver, 网址: str) -> None:
        self.URL = 网址
        self.driver = driver
        self.driver.get(网址)
        self.列表内容 = []
        print("已进入目标网址,接下来你需要打开nemo端的自动化应用脚本")

    def 置接口列表(self,list_XPATH: str,更新一次延时=0.5):
        """事实获取接口的列表"""
        self.list_all = self.driver.find_element(By.XPATH, list_XPATH)
    
        while True :
            self.列表内容 = []
            try:
                list_new_ = self.list_all.find_elements(By.CSS_SELECTOR, '.list-value')
                for list_one in list_new_ :
                    html_text = list_one.get_attribute('outerHTML')
                    pattern = r'(?<=<span class="list-value">).*(?=</span>)' # 使用正则匹配处理列表项的HTML文本
                    match = re.search(pattern, html_text).group()
                    self.列表内容.append(match)
                #print(self.列表内容)
            except (noee,toe,IndexError):
                pass
            time.sleep(更新一次延时)


# 调用示范
if __name__ == "__main__" :
    def 打印重试内容或抛出超时异常(retry):
        retry__ = retry + 1
        # 重试次数大于10时，程序将会停止
        if retry >= 10:
            raise lcmao.定位控件失败("多次定位编程猫作品启动按钮尝试失败，请检查网络后重试。\n如果仍然失败, 可能是程序版本过于落后。")
        print("定位启动按钮失败, 正在尝试重新定位")
        time.sleep(2.5)
        return retry__

    bcmname = "" # 猫账号
    bcmkey = "" # 猫密码

    浏览器 = webdriver.Firefox()
    lcmao.检查并自动登录猫站(bcmname, bcmkey, 浏览器)
    a = 自动化脚本接口(浏览器,"https://?")  # 你的猫作品页**注意不是社区页**
    wait = WebDriverWait(浏览器, 10)
    retry_ = 0
    while 1 :
        try :
            # 定位到作品开始按钮
            container = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".CUI-player-cover-play-btn")))
        except  (toe,noee):
            retry_ = 打印重试内容或抛出超时异常(retry_)
    
        # 按下启动按钮
        # 退出循环
        container[0].click()
        break
    input()
    a.置接口列表('//*[@id="********-****-****-****-************"]') # 从浏览器复制你要下载的列表的XPATH