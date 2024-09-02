# login_codemao.com
import time

from colorama.ansi import Fore, Style # pip install colorama      #==0.4.6
from selenium.webdriver.common.by import By # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException as noee
from selenium.common.exceptions import TimeoutException as toe
from selenium.common.exceptions import ElementClickInterceptedException as ecie
from selenium.webdriver.remote.webdriver import WebDriver

# 使用讯飞星火辅助完成编程

class 定位控件失败(TimeoutError):
    pass

def 打印未登录网络提示():
    print(Fore.BLUE + "你还没有载入完到编程猫主站页面，可能是由于网络较差，正在尝试重新检查。")
    time.sleep(2.5)

def 检查登录信息(wait):
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".c-navigator--user_cont"))) # 定位到已登录的div控件
        print(Fore.GREEN + "已登录" + Style.RESET_ALL)
        return True
    except noee:
        打印未登录网络提示()
        return False
    except toe:
        打印未登录网络提示()
        return False


def 链接主站失败():
    raise 定位控件失败("多次定位编程猫网页的用户控件失败，可能是因为网络较差，请检查网络后重试。\n如果仍然失败, 可能是程序版本过于落后。")

"""
访问社区用户页并检查是否登录
"""
def 检查并自动登录猫站(
        编程猫账号 : str, 
        编程猫密码 : str,
        driver : WebDriver, # 必须已经打开网页
        URL = "https://shequ.codemao.cn/user"
        , max_retry = 10
    ) :
    """
    driver -> 浏览器实例 必须已经打开网页\n
    URL -> 猫站网址
    访问主站的速度可能比较缓慢, 这里我们默认访问user界面\n
    max_retry --> 最大重试次数
    """ 
    driver.get(URL)
    retry_ = 0 # 重置尝试次数信息                  
    wait = WebDriverWait(driver, 10) # 等待网页载入

    while 1:
        try:
            # 定位到未登录的div控件
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".c-navigator--not_login"))) 
            time.sleep(0.5)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".c-navigator--avatar")))[0].click() # 按下登录按钮
        except (noee,toe,ecie):
            if 检查登录信息(wait):
                break
            elif retry_ > max_retry :
                链接主站失败()
            else:
                continue
    
        # 自动登录
        driver.find_element(By.CSS_SELECTOR,'div.commons-styles--input-border:nth-child(1) > input:nth-child(1)').send_keys(编程猫账号)
        driver.find_element(By.CSS_SELECTOR,'div.commons-styles--input-border:nth-child(2) > input:nth-child(1)').send_keys(编程猫密码)
        driver.find_element(By.CSS_SELECTOR, '#login_button').click()
        print(Fore.BLUE + "你还没有登录到编程猫,已尝试自动登录" + Fore.LIGHTBLACK_EX + "\n等待三秒后重新检查")
        # 这里等待一秒后重新进入循环
        wait._timeout = 1
        time.sleep(1.5)
    
    print(Fore.LIGHTBLACK_EX + "完成登录状态检查" + Style.RESET_ALL)
    
    return True