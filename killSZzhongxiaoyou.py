import configparser
import os
import re
import time
from io import BytesIO
from typing import List

import pytesseract
import requests
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from helper import enter_iframe_by_id
from helper_class import Info
from model_my import recogn_code

from mp4 import Mp4info

root_dir = os.path.split(os.path.realpath(__file__))[0]  # 按照路径将文件名和路径分割开
# config.ini文件路径
config_filepath = os.path.join(root_dir, 'config.ini')  # 路径拼接
config = configparser.ConfigParser()  # ConfigParser 是用来读取配置文件的包
config.read(config_filepath, encoding='utf-8-sig')

# courses_number = 0  # 总共有几节课
# sections_number = 0  # 这节课有几个单元（阶段）
# activities_number = 0  # 这个单元（阶段）有几个活动

def init_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument(r'--user-data-dir=' + config.get("account", "google_setting"))  # 设置个人资料路径
    driver = webdriver.Chrome(os.path.join(root_dir, "chromedriver.exe"), options=options)
    driver.maximize_window()
    return driver


def login(global_driver, info:Info):
    login_url = config.get('account', 'url')
    ac = info.account
    pswd = info.password
    global_driver.get(login_url)
    with enter_iframe_by_id(global_driver, str(config.get('id', 'login_frame'))) as frame_loc:
        global_driver.find_element_by_id('user_code').send_keys(ac)
        global_driver.find_element_by_id('password').send_keys(pswd)

        get_save_code(global_driver, frame_loc)
        code = recogn_code("code.png")
        global_driver.find_element_by_id("code").send_keys(code)

        time.sleep(5)

        all_login_btn = global_driver.find_element_by_class_name(config.get("cls", "login_btn")).click()


def enter_study(global_driver, info:Info):
    global_driver.get(info.course_url)
    first_play_video(global_driver)
    # 获取课程列表，并开始刷
    while find_unfinished(global_driver):
        # 有未完成的课程
        try:
            kill_single_course(global_driver)
        except Exception as e:
            pass
        global_driver.refresh()
        time.sleep(10)


def find_unfinished(global_driver):
    play_list_tables = global_driver.find_elements_by_class_name(config.get("cls", "course_table"))
    for idx, table in enumerate(play_list_tables):
        # 找到第一个没刷完的视频
        if "已完成" in table.get_attribute("innerHTML"):
            continue
        tr = table.find_element_by_class_name(config.get("cls", "video_tr"))
        tr.click()
        print("当前第", idx + 1, "课，", "总", len(play_list_tables), "课")
        break
    else:
        # 刷完了
        return False
    return True


def kill_single_course(global_driver):
    time.sleep(30)
    html = global_driver.execute_script("return document.documentElement.outerHTML")
    pattern = r"file=(.+?)&"
    mp4_video = re.findall(pattern, html)[0]
    file = Mp4info(mp4_video)
    video_duration: float = file.get_duration()
    sleep_time = int(video_duration) + 120
    print(sleep_time)
    time.sleep(sleep_time)


# 使得看视频网址生效
def make_available(global_driver):
    global_driver.get(config.get('account', 'course_list_url'))
    all_course_btns: List = WebDriverWait(global_driver, 30).until(EC.presence_of_all_elements_located((
        By.CLASS_NAME, config.get("cls", "study_btn"))))
    courses_number = len(all_course_btns)
    course = all_course_btns[int(config.get("number", "this_course")) - 1]
    course.click()
    time.sleep(1)


# 第一次点击，进入播放界面
def first_play_video(global_driver):
    videos = global_driver.find_elements_by_class_name(config.get("cls", "video_tr"))
    videos[0].click()
    time.sleep(30)


# 切换到新窗口
def change2new_window(global_driver):
    windows = global_driver.window_handles
    current_window = global_driver.current_window_handle
    for new_window in windows:
        if new_window != current_window:
            global_driver.switch_to.window(new_window)
            break


def get_save_code(global_driver, frame_loc):
    # 通过网页截图然后进行截取
    code_img_ele = WebDriverWait(global_driver, 20).until(
        EC.presence_of_element_located((By.ID, 'safecode')))
    # im = Image.open(BytesIO(code_img_ele.screenshot("code.png")))
    global_driver.save_screenshot('screenshot.png')

    left = frame_loc[0] + code_img_ele.location['x']
    top = frame_loc[1] + code_img_ele.location['y']
    right = frame_loc[0] + code_img_ele.location['x'] + code_img_ele.size['width']
    bottom = frame_loc[1] + code_img_ele.location['y'] + code_img_ele.size['height']

    im = Image.open('screenshot.png')
    im = im.crop((left, top, right, bottom))
    print((left, top, right, bottom))
    im.save('code.png')
    # global_driver.save_screenshot("screenshot.png")  # 对整个浏览器页面进行截图


    # pic_location = code_img_ele.get_location()
    # pic_size = code_img_ele.get_size()
    # left = code_img_ele.location['x']
    # top = code_img_ele.location['y']
    # right = code_img_ele.location['x'] + code_img_ele.size['width']
    # bottom = code_img_ele.location['y'] + code_img_ele.size['height']

    # im = im.crop((left, top, right, bottom))  # 对浏览器截图进行裁剪
    # 开始识别
    # 自行训练神经网络


if __name__ == '__main__':
    # recog_code(123)
    try:
        driver = init_driver()
        login(driver)
        time.sleep(5)
        make_available(driver)
        change2new_window(driver)
        enter_study(driver)
    except Exception as e:
        pass


