import os
import sys
root_dir = os.path.split(os.path.realpath(__file__))[0]  # 按照路径将文件名和路径分割开
sys.path.append(fr'{root_dir}')