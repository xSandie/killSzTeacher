import os

import cv2
import numpy as np
from PIL import Image

# 图片95*30
from sklearn import neighbors


def count_number(num_list, num):
    """
    统计一维数组中某个数字的个数
    :param num_list:
    :param num:
    :return: num的数量
    """
    t = 0
    for i in num_list:
        if i == num:
            t += 1
    return t


def cut_vertical(img_list, cvalue=255):
    """
    投影法竖直切割图片的数组
    :param img_list: 传入的数据为一个由（二维）图片构成的数组，不是单纯的图片
    :param cvalue: 切割的值 同cut_level中的cvalue
    :return: 切割之后的图片的数组
    """
    # 如果传入的是一个普通的二值化的图片，则需要首先将这个二值化的图片升维为图片的数组
    if len(np.array(img_list).shape) == 2:
        img_list = img_list[None]
    r_list = []
    for img_i in img_list:
        end = 0
        for i in range(len(img_i.T)):
            if count_number(img_i.T[i], cvalue) >= img_i.shape[0]:
                star = end
                end = i
                if end - star > 1:
                    r_list.append(img_i[:, star:end])
    return r_list


# 去除噪点，去除孤立点，噪点
def noise_remove_cv2(image, k):
    def calculate_noise_count(img_obj, w, h):
        """
        计算邻域非白色的个数
        """
        count = 0
        width, height = img_obj.shape
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj[_w_, _h_] < 230:  # 二值化的图片设置为255
                    count += 1
        return count

    w, h = image.shape
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                image[_w, _h] = 255
                continue
            # 计算邻域pixel值小于255的个数
            pixel = image[_w, _h]
            if pixel == 255:
                continue

            if calculate_noise_count(image, _w, _h) < k:
                image[_w, _h] = 255
    return image


def train():
    x = []
    y = []
    t = 1
    new_image_path = "cut_captcha"
    pic_full_names = list(os.walk("captcha_predict"))[0][2]
    for pic_full_name in pic_full_names:
        if not "png" in pic_full_name:
            continue
        # 读图片+降噪
        img = cv2.imread(os.path.join("captcha_predict", pic_full_name))
        # 转换为灰度图
        im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, im_inv = cv2.threshold(im_gray, 150, 255, 0)  # >150灰度值的设置成255
        img_clear = noise_remove_cv2(im_inv, 1)
        label = pic_full_name.split(".")[0]
        # 必须得切割
        # 垂直分割投影法分割图片
        label_list = list(label)
        img_list = cut_vertical(img_clear)

        for i, lb in zip(img_list, label_list):
            resize_img = cv2.resize(i, (15, 30))  # 重新定义大小
            path = os.path.join(new_image_path, lb)
            if not os.path.exists(path):
                os.makedirs(path)
            # 这里可以对切割到的图片进行操作，显示出来或者保存下来
            cv2.imwrite(os.path.join(path, str(t) + '.png'), resize_img)
            t += 1

    # pix = np.array(img_clear)
    # one_pic = pix.ravel()
    # x.append(list(one_pic))
    # y.append(label)

# train_x = np.array(x)
# train_y = np.array(y)
#
# model = neighbors.KNeighborsClassifier(n_neighbors=10)
# model.fit(train_x, train_y)
#
# x = []
# y = []
# for label in os.listdir('test'):
#     img = cv2.imread(os.path.join("test", label))
#     # 转换为灰度图
#     im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, im_inv = cv2.threshold(im_gray, 150, 255, 0)  # >150灰度值的设置成255
#     img_clear = noise_remove_cv2(im_inv, 1)
#     pix = np.array(img_clear)
#     # pix = (pix > 180) * 1
#     pix = pix.ravel()
#     one_pic = pix.ravel()
#     x.append(list(one_pic))
#     y.append(label.split(".")[0])
#
# predict_y = model.predict(np.array(x))
# print(predict_y == np.array(y))
