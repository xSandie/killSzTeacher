import os
import pickle
import time
import tkinter as tk
from tkinter import ttk
import threading
from multiprocessing import Process

from helper_class import Info
from killSZzhongxiaoyou import init_driver, login, make_available, change2new_window, enter_study


# with open("info.pkl", "wb") as f:
#     pickle.dump(info, f, 0)


# 获取

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

    # 首次进入
    def first_enter(self):
        self.window.title("中小幼刷课脚本")
        self.window.geometry('800x800')

        tk.Label(self.window, text='账号👇', font=('微软雅黑', 12)).pack()
        username_entry = tk.Entry(self.window, textvariable=self.account)
        username_entry.pack()
        tk.Label(self.window, text='密码👇', font=('微软雅黑', 12)).pack()
        password_entry = tk.Entry(self.window, textvariable=self.password)
        password_entry.pack()
        tk.Label(self.window, text='课程网址👇', font=('微软雅黑', 12)).pack()
        course_url_entry = tk.Entry(self.window, textvariable=self.course_url)
        course_url_entry.pack()

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
    def second_enter(self,info):
        self.account.set(info.account)
        self.password.set(info.password)
        self.course_url.set(info.course_url)

        self.window.title("中小幼刷课脚本")
        self.window.geometry('800x800')

        tk.Label(self.window, text='账号👇', font=('微软雅黑', 12)).pack()
        username_entry = tk.Entry(self.window, textvariable=self.account)
        username_entry.pack()
        tk.Label(self.window, text='密码👇', font=('微软雅黑', 12)).pack()
        password_entry = tk.Entry(self.window, textvariable=self.password)
        password_entry.pack()
        tk.Label(self.window, text='课程网址👇', font=('微软雅黑', 12)).pack()
        course_url_entry = tk.Entry(self.window, textvariable=self.course_url)
        course_url_entry.pack()

        self.start_btn = tk.Button(self.window, text="开始刷课", command=self.prepare_killer)
        self.start_btn.pack()

        os.system('notepad readme.txt')
        self.window.wm_attributes('-topmost', 1)

        self.window.mainloop()

    def prepare_killer(self):
        print(self.account.get(), self.password.get(), self.course_url.get())
        self.start_btn["state"] = tk.DISABLED
        tk.Message(self.window, text="脚本正在运行，将会打开浏览器，如运行失败，请关闭后再重启。", font=('微软雅黑', 12), bg='yellow', width=600).pack()
        info = Info(account=self.account.get(),
                    password=self.password.get(),
                    course_url=self.course_url.get())
        with open("info.pkl", "wb") as f:
            pickle.dump(info, f, 0)
        run_killer(info)


def run_killer(info):
    driver = init_driver()
    try:
        login(driver, info)
        time.sleep(5)
        make_available(driver)
        change2new_window(driver)
        enter_study(driver, info)
    except Exception as e:
        print(e)
        driver.quit()


if __name__ == '__main__':
    VisWindow().start()
