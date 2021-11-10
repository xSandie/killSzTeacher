from distutils.core import setup
import py2exe

setup(console=["killWindows.py"],data_files = [('.',['info.pkl','theta.pkl']),('.',["chromedriver.exe",])])


