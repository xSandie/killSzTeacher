# 如何使用
##  🥂 小白4步上手篇
> 耗时**3-5分钟**，所需环境一台安装windows10的较为流畅的电脑。
1. 添加作者微信，微信号sandiexiang，获取最新程序百度网盘链接，解压压缩包，其中有名为killWindows.exe的、可双击运行的程序。
2. 安装链接中的旧版本谷歌浏览器。
3. 登陆深圳中小幼教师教育网，打开至所需刷课的**课程播放页面**，复制链接地址，准备粘贴入刷课程序中。
4. 双击运行刷课程序，输入账号密码，点击开始刷课，等待程序自动运行，若开启失败，关闭重新启动即可。
## 🥂 二次开发篇
### 技术方案简介
> 本项目基于 python3.7
- 使用以selenium+chrome为主的web自动化测试的那套方案，为使项目能自动播放flash特采用旧版本chrome及对应驱动。

- 验证码使用sklearn的knn方法，训练了一个简易神经网络，具体方案见 gen.py、model_my.py、split_img.py三个文件。

- 界面使用tkinter，使用pyinstaller进行打包，具体打包配置见killWindows.spec。

### 主要文件及其功能

1. killWindows.py

    窗体程序设计。

2. killSZzhongxiaoyou.py

    爬虫的主体部分。

3. killWindows.spec

    打包的配置，打包代码
    ```
    pyinstaller -F killWindows.spec
    ```
    运行后会在dist目录下生成可执行文件。

### TODO
- [ ] 重新生成验证码训练神经网络，目前准确率较低（测试集99.54%，实际使用只有约70%）。
- [ ] 自动重新登录。
- [ ] 退出时关闭浏览器。
- [ ] 代码美化，现在代码是一坨😂。

