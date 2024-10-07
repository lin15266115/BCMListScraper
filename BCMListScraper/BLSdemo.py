"""BCMlistScraper的调用示范"""


import BCMListScraper as bls
from selenium import webdriver
import time

# https://nemo.codemao.cn/w/226095175
# cb64b05c-4daa-410d-95dd-1ea44cf08d39

启动器 = webdriver.Firefox()

运行 = bls.自动化脚本接口(启动器)

运行.打开作品("https://nemo.codemao.cn/w/226095175")

输出列表 = 运行.置接口列表("//*[@id=\"cb64b05c-4daa-410d-95dd-1ea44cf08d39\"]")

while 1:
    time.sleep(0.2)
    print(输出列表.列表内容)