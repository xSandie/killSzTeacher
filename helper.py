# 切换到视频播放器frame
import os
import zipfile
from contextlib import contextmanager

import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import platform

from constant import root_dir


def judge_os() -> str:
    print(platform.system())
    if platform.system() == 'Windows':
        return 'win'
    elif platform.system() == 'Linux':
        return 'linux'
    elif platform.system() == 'Darwin':
        return 'mac'
    return 'other'


@contextmanager  # 上下文管理器
def enter_iframe_by_id(global_driver, frame_id: str):
    # global_driver.switch_to.frame(frame_id)  # 元素定位
    _iframe = WebDriverWait(global_driver, 30).until(EC.presence_of_all_elements_located((
        By.ID, frame_id)))[
        0]  # 等待30秒直到能切换进iframe '''判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement'''
    left, top, right, bottom = int(_iframe.location['x']), int(_iframe.location['y']), int(
        _iframe.location['x'] + _iframe.size['width']), int(_iframe.location['y'] + _iframe.size['height'])
    global_driver.switch_to.frame(_iframe)
    yield (left, top, right, bottom)
    global_driver.switch_to.default_content()


def load_page(driver, func, *args):
    try:
        func(*args)
    except Exception as e:
        print(e)
        driver.execute_script('window.stop()')


from urllib.parse import quote_plus as url_quoteplus
from urllib.parse import urlsplit
from selenium.webdriver.common.by import By as WebBy
from selenium.webdriver.support.ui import Select as WebSelect


def allow_flash(driver, url):
    def _base_url(url):
        if url.find("://") == -1:
            url = "http://{}".format(url)
        urls = urlsplit(url)
        return "{}://{}".format(urls.scheme, urls.netloc)

    def _shadow_root(driver, element):
        return driver.execute_script("return arguments[0].shadowRoot", element)

    base_url = _base_url(url)
    driver.get("chrome://settings/content/siteDetails?site={}".format(url_quoteplus(base_url)))

    actions = ActionChains(driver)
    actions = actions.send_keys(Keys.TAB * 12)
    actions = actions.send_keys(Keys.SPACE)
    actions = actions.send_keys("a")
    actions = actions.send_keys(Keys.ENTER)
    actions.perform()


def get_save_driver(version: str, os_type: str = "win"):
    file_name = "chromedriver_win32.zip" if os_type == "win" else "chromedriver_mac64.zip"
    if os.path.exists(os.path.join(root_dir, file_name)):
        os.remove(os.path.join(root_dir, file_name))
    version = version.strip()
    driver_download_url = f"http://npm.taobao.org/mirrors/chromedriver/{version}/{file_name}"
    r = requests.get(driver_download_url)
    file_name = os.path.join(root_dir, file_name)
    with open(f'{file_name}', 'wb') as code:
        code.write(r.content)
    zip_file = zipfile.ZipFile(f'{file_name}')
    zip_list = zip_file.namelist()  # 压缩文件清单，可以直接看到压缩包内的各个文件的明细
    for f in zip_list:  # 遍历这些文件，逐个解压出来，
        zip_file.extract(f, root_dir)


if __name__ == '__main__':
    judge_os()
