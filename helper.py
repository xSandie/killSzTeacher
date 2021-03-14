# 切换到视频播放器frame
from contextlib import contextmanager

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@contextmanager  # 上下文管理器
def enter_iframe_by_id(global_driver, frame_id: str):
    # global_driver.switch_to.frame(frame_id)  # 元素定位
    _iframe = WebDriverWait(global_driver, 30).until(EC.presence_of_all_elements_located((
        By.ID, frame_id)))[
        0]  # 等待30秒直到能切换进iframe '''判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement'''
    left, top, right, bottom = int(_iframe.location['x']) , int(_iframe.location['y']), int(_iframe.location['x'] + _iframe.size['width']), int(_iframe.location['y'] + _iframe.size['height'])
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
