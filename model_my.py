import os

import joblib
import numpy as np
import cv2
from sklearn import neighbors

from split_img import noise_remove_cv2, cut_vertical

# print(list(os.listdir("cut_captcha")))

# x = []
# y = []
#
# for i in range(10):
#     label = str(i)
#     for pic_full_name in os.listdir(os.path.join("cut_captcha", label)):
#         img = cv2.imread(os.path.join("cut_captcha",label, pic_full_name))
#         im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         ret, im_inv = cv2.threshold(im_gray, 150, 255, 0)  # >150灰度值的设置成255
#         img_clear = noise_remove_cv2(im_inv, 1)
#         pix = np.array(img_clear)
#         one_pic = pix.ravel()
#         x.append(list(one_pic))
#         y.append(label)
#
# train_x = np.array(x)
# train_y = np.array(y)
#
# model = neighbors.KNeighborsClassifier(n_neighbors=10)
# model.fit(train_x, train_y)
#
# joblib.dump(model, "theta.pkl")
model = joblib.load("theta.pkl")

# 验证



# pic_full_names = list(os.walk("test"))[0][2]
# for pic_full_name in pic_full_names:
#     if not "png" in pic_full_name:
#         continue
#     # 读图片+降噪
#     img = cv2.imread(os.path.join("test", pic_full_name))
#     # 转换为灰度图
#     im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, im_inv = cv2.threshold(im_gray, 150, 255, 0)  # >150灰度值的设置成255
#     img_clear = noise_remove_cv2(im_inv, 1)
#     label = pic_full_name.split(".")[0]
#     # 必须得切割
#     # 垂直分割投影法分割图片
#     label_list = list(label)
#     img_list = cut_vertical(img_clear)
#
#     for i, lb in zip(img_list, label_list):
#         resize_img = cv2.resize(i, (15, 30))  # 重新定义大小
#         pix = np.array(resize_img)
#         one_pic = pix.ravel()
#         x.append(list(one_pic))
#         y.append(lb)
# 读图片+降噪
def recogn_code(file_name):
    x = []
    y = []
    img = cv2.imread(file_name)
    # 转换为灰度图
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, im_inv = cv2.threshold(im_gray, 150, 255, 0)  # >150灰度值的设置成255
    img_clear = noise_remove_cv2(im_inv, 1)
    # label = pic_full_name.split(".")[0]
    # 必须得切割
    # 垂直分割投影法分割图片
    # label_list = list(label)
    img_list = cut_vertical(img_clear)

    for i in img_list:
        resize_img = cv2.resize(i, (15, 30))  # 重新定义大小
        pix = np.array(resize_img)
        one_pic = pix.ravel()
        x.append(list(one_pic))
        # y.append(lb)

    predict_y = model.predict(np.array(x))
    n = ""
    for i in predict_y:
        n += i
    return n
# print(n)
# print(predict_y == np.array(y))

# pix = np.array(img_clear)
# one_pic = pix.ravel()
# x.append(list(one_pic))
# y.append(label)
