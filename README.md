此项目用于从编程猫的作品内获取列表内容。
**该项目有待进一步测试和完善。**

此项目提供了一个附属的程序，用于自动登录编程猫

### 部分功能介绍

**创建一个实例**

    浏览器 = webdriver.Firefox() # 创建一个firefox浏览器实例
    a = 自动化脚本接口(浏览器) # 创建一个接口实例
**打开作品**

    a.打开作品("https://nemo.codemao.cn/w/") # 你的作品页
**读取作品内的列表**

    a.置接口列表('//*[@id="********-****-****-****-************"]') # 采用XPATH定位
