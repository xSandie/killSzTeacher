import multiprocessing
import os
import pickle
import time
import tkinter as tk
import tkinter.messagebox
import threading
import configparser
import os
import re
import time
from typing import List
import os

from helper import get_save_driver, judge_os
from helper_class import Info
from killSZzhongxiaoyou import init_driver, login, make_available, change2new_window, enter_study


# with open("info.pkl", "wb") as f:
#     pickle.dump(info, f, 0)
def panel_windows():
    try:
        with open("info.pkl", "rb") as f:
            info: Info = pickle.load(f)
        # todo 有存储过信息，提示是否继续刷课
    except FileNotFoundError as e:
        # todo 从未存储过信息，直接打开空页面
        pass


class VisWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.account = tk.StringVar()
        self.password = tk.StringVar()
        self.course_url = tk.StringVar()
        self.chrome_version = tk.StringVar()
        self.chrome_location = tk.StringVar()

    # 首次进入
    def first_enter(self):
        self.chrome_location.set("如无异常可不填写")
        self.chrome_version.set("初次使用时填写即可")

        self.window.title("中小幼刷课脚本")
        self.window.geometry('800x900')

        tk.Label(self.window, text='账号👇', font=('微软雅黑', 12)).pack()
        username_entry = tk.Entry(self.window, textvariable=self.account)
        username_entry.pack()
        tk.Label(self.window, text='密码👇', font=('微软雅黑', 12)).pack()
        password_entry = tk.Entry(self.window, textvariable=self.password)
        password_entry.pack()
        tk.Label(self.window, text='课程网址👇', font=('微软雅黑', 12)).pack()
        course_url_entry = tk.Entry(self.window, textvariable=self.course_url)
        course_url_entry.pack()
        tk.Label(self.window, text='谷歌浏览器版本👇', font=('微软雅黑', 12)).pack()
        chrome_version_entry = tk.Entry(self.window, textvariable=self.chrome_version)
        chrome_version_entry.pack()
        tk.Label(self.window, text='谷歌浏览器位置👇', font=('微软雅黑', 12)).pack()
        chrome_location_entry = tk.Entry(self.window, textvariable=self.chrome_location)
        chrome_location_entry.pack()

        self.start_btn = tk.Button(self.window, text="开始刷课", command=self.prepare_killer)
        self.start_btn.pack()

        os.system('notepad readme.txt')
        self.window.wm_attributes('-topmost', 1)

        self.window.mainloop()

    def start(self):
        try:
            with open("info.pkl", "rb") as f:
                info: Info = pickle.load(f)
            self.second_enter(info)
            # todo 有存储过信息，提示是否继续刷课
        except FileNotFoundError as e:
            # todo 从未存储过信息，直接打开空页面
            self.first_enter()

    # 再次进入
    def second_enter(self, info):
        self.account.set(info.account)
        self.password.set(info.password)
        self.course_url.set(info.course_url)
        self.chrome_version.set(info.chrome_version)
        self.chrome_location.set(info.chrome_location)

        self.window.title("中小幼刷课脚本")
        self.window.geometry('800x900')

        tk.Label(self.window, text='账号👇', font=('微软雅黑', 12)).pack()
        username_entry = tk.Entry(self.window, textvariable=self.account)
        username_entry.pack()
        tk.Label(self.window, text='密码👇', font=('微软雅黑', 12)).pack()
        password_entry = tk.Entry(self.window, textvariable=self.password)
        password_entry.pack()
        tk.Label(self.window, text='课程网址👇', font=('微软雅黑', 12)).pack()
        course_url_entry = tk.Entry(self.window, textvariable=self.course_url)
        course_url_entry.pack()
        tk.Label(self.window, text='谷歌浏览器版本👇', font=('微软雅黑', 12)).pack()
        chrome_version_entry = tk.Entry(self.window, textvariable=self.chrome_version)
        chrome_version_entry.pack()
        tk.Label(self.window, text='谷歌浏览器位置👇', font=('微软雅黑', 12)).pack()
        chrome_location_entry = tk.Entry(self.window, textvariable=self.chrome_location)
        chrome_location_entry.pack()

        self.start_btn = tk.Button(self.window, text="开始刷课", command=self.prepare_killer)
        self.start_btn.pack()

        os.system('notepad readme.txt')
        self.window.wm_attributes('-topmost', 1)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.mainloop()

    def close_window(self):
        # 关闭窗口
        self.window.destroy()

    def can_run(self):
        account = self.account.get()
        password = self.password.get()
        course_url = self.course_url.get()
        chrome_version = self.chrome_version.get()
        # chrome_location = self.chrome_location.get()
        if all([account, password, course_url, chrome_version]):
            return True
        return False

    def prepare_killer(self):
        if not self.can_run():
            tk.messagebox.showwarning('提示', '请至少填写完前4项')
            return

        self.start_btn["state"] = tk.DISABLED
        tk.Message(self.window, text="脚本正在运行，将会打开浏览器，如运行失败，请关闭后再重启。", font=('微软雅黑', 12), bg='yellow', width=600).pack()
        info = Info(account=self.account.get(),
                    password=self.password.get(),
                    course_url=self.course_url.get(),
                    chrome_version=self.chrome_version.get(),
                    chrome_location=self.chrome_location.get(),
                    )
        os_type = judge_os()

        file_name = {
            "mac": "chromedriver",
            "win": "chromedriver.exe",
        }[os_type]

        if os.path.exists(file_name):
            pass
        else:
            get_save_driver(version=self.chrome_version.get(), os_type=os_type)

        with open("info.pkl", "wb") as f:
            pickle.dump(info, f, 0)
        T = threading.Thread(target=run_killer, args=(info, file_name))
        T.daemon = True
        T.start()


def run_killer(info, driver_name, chrome_path: str = None):
    driver = init_driver(driver_name, chrome_path)
    try:
        login(driver, info)
        time.sleep(5)
        make_available(driver)
        change2new_window(driver)
        enter_study(driver, info)
    except Exception as e:
        print(e)
        driver.quit()
        run_killer(info, driver_name=driver_name)


if __name__ == '__main__':
    VisWindow().start()
