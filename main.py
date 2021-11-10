import configparser
import os
import time
from typing import List

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import functools
from selenium.webdriver.support.wait import WebDriverWait
from helper import enter_iframe_by_id, load_page
from selenium.webdriver.chrome.options import Options

chromeOpitons = Options()
prefs = {
    "profile.managed_default_content_settings.images": 1,
    "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
    "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,

}
chromeOpitons.add_experimental_option('prefs', prefs)

root_dir = os.path.split(os.path.realpath(__file__))[0]  # 按照路径将文件名和路径分割开
# config.ini文件路径
config_filepath = os.path.join(root_dir, 'config.ini')  # 路径拼接
config = configparser.ConfigParser()  # ConfigParser 是用来读取配置文件的包
config.read(config_filepath, encoding='utf-8-sig')

courses_number = 0  # 总共有几节课
sections_number = 0  # 这节课有几个单元（阶段）
activities_number = 0  # 这个单元（阶段）有几个活动
driver = webdriver.Chrome(os.path.join(root_dir, "chromedriver"), options=chromeOpitons)


# 进行登陆


def login(global_driver):
    login_url = config.get('account', 'url')
    ac = config.get('account', 'account')
    pswd = config.get('account', 'password')
    global_driver.get(login_url)
    with enter_iframe_by_id(driver, str(config.get('id', 'login_frame'))):
        global_driver.find_element_by_id('user_code').send_keys(ac)
        global_driver.find_element_by_id('password').send_keys(pswd)
        time.sleep(5)
        all_login_btn = global_driver.find_element_by_class_name(config.get("cls", "login_btn")).click()


def enter_study(global_driver):
    global_driver.get(config.get('account', 'course_list_url'))

    # global_driver.implicitly_wait(10)  # 隐式等待是告诉WebDriver去等待一定的时间后去查找元素
    all_course_btns: List = WebDriverWait(global_driver, 30).until(EC.presence_of_all_elements_located((
        By.CLASS_NAME, config.get("cls", "study_btn"))))
    # all_course_btns: List = global_driver.find_elements_by_class_name(config.get("cls", "study_btn"))
    courses_number = len(all_course_btns)
    course = all_course_btns[int(config.get("number", "this_course")) - 1]
    course.click()

    windows = global_driver.window_handles
    current_window = global_driver.current_window_handle
    for new_window in windows:
        if new_window != current_window:
            global_driver.switch_to.window(new_window)
            break

    # global_driver.implicitly_wait(10)  # 隐式等待是告诉WebDriver去等待一定的时间后去查找元素
    all_sections_btns = global_driver.find_elements_by_class_name(config.get("cls", "enter_section_btn"))
    stages = global_driver.find_elements_by_class_name(config.get("cls", "section_stage"))
    sections_number = len(all_sections_btns)
    this_section = int(config.get("number", "this_section")) - 1
    stage = stages[this_section]
    ActionChains(global_driver).move_to_element(stage).perform()
    section = all_sections_btns[this_section]
    section.click()

    all_activity_btns = global_driver.find_elements_by_class_name(config.get("cls", "enter_activity_btn"))
    activities_number = len(all_activity_btns)
    activity = all_activity_btns[int(config.get("number", "this_activity")) - 1]
    ActionChains(global_driver).move_to_element(activity).perform()
    activity.click()


login(driver)
enter_study(driver)
time.sleep(5)  # Let the user actually see something!
driver.quit()

# global_driver.find_elements_by_class_name(config.get("cls", "enter_section_btn"))
