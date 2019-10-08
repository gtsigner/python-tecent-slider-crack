# coding:utf-8
from selenium import webdriver
import os
import signal
import time

global driver


def sig_handler(sig, frame):
    print("收到退出信号：", sig)
    driver.close()


def start_chrome():
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-web-security')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://aq.qq.com/v2/uv_aq/html/reset_pwd/pc_reset_pwd_input_account.html')
    # 获取图片
    time.sleep(1)
    driver.execute_script('$("iframe")[1].contentDocument.querySelector("#tcaptcha_trigger").click()')
    time.sleep(2)
    url = driver.execute_script('return $("#tcaptcha_iframe")[0].contentDocument.querySelector("#slideBg").src')
    # 1.拦截所有请求


# https://www.jianshu.com/p/1531e12f8852
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    start_chrome()
