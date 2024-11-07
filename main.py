import configparser
import sys
import time
import random
import logging
from bili.script import headers_bili, getAllDynamic
from script.push import send_key, push, push_dynamic
from bili.index import bili_main


# 读取配置文件
def readConfig():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    if "data" in config:
        send_key["token"] = config["data"]["send_key"]
        headers_bili["Cookie"] = config["data"]["cookie_bili"]
    else:
        logging.error("配置文件未找到或格式错误")
        sys.exit(0)


# 写入日志
logging.basicConfig(
    filename="running.log",
    format="\n%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def Wlog(text):
    logging.error(text, exc_info=True)


def test(ii):
    if ii == 2:
        text = "测试...,test..."
        push("测试", text)
        logging.info(text)


def getAll():
    print("开始抓取动态数据")
    logging.info("开始抓取动态数据")
    getAllDynamic()


def main():
    ii = 0
    logging.info("进入 main 函数")  # 调试信息
    while True:
        ii += 1
        logging.info("当前轮次: " + str(ii))
        # test(ii)
        # bili_main()
        getAll(ii)
        s = random.randint(30, 80)
        time.sleep(s * 2)


if __name__ == "__main__":
    logging.info("------ 开始监控 ------")
    print("开始监控")
    try:
        readConfig()
        # main()
        getAll()
        # bili_main()
    except Exception as e:
        Wlog("程序异常退出: " + str(e))
        print("程序异常退出", e)
