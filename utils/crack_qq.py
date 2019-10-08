#!/usr/bin/env python    
# encoding: utf-8
import random
import cv2
import numpy as np
import pandas as pd
import math
from PIL import Image
import os


# x方向一阶导中值
def get_dx_median(dx, x, y, w, h):
    return np.median(dx[y:(y + h), x])


# 预处理
def pre_process(img_path):
    img = cv2.imread(img_path, 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转成灰度图像

    _, binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)  # 将灰度图像转成二值图像

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 查找轮廓

    rect_area = []
    rect_arc_length = []
    cnt_infos = {}

    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) < 5000 or cv2.contourArea(cnt) > 25000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cnt_infos[i] = {'rect_area': w * h,  # 矩形面积
                        'rect_arclength': 2 * (w + h),  # 矩形周长
                        'cnt_area': cv2.contourArea(cnt),  # 轮廓面积
                        'cnt_arclength': cv2.arcLength(cnt, True),  # 轮廓周长
                        'cnt': cnt,  # 轮廓
                        'w': w,
                        'h': h,
                        'x': x,
                        'y': y,
                        'mean': np.mean(np.min(img[y:(y + h), x:(x + w)], axis=2)),  # 矩形内像素平均
                        }
        rect_area.append(w * h)
        rect_arc_length.append(2 * (w + h))
    dx = cv2.Sobel(img, -1, 1, 0, ksize=5)

    return img, dx, cnt_infos


def qq_mark_pos(img_path):
    img, dx, cnt_infos = pre_process(img_path)
    h, w = img.shape[:2]
    df = pd.DataFrame(cnt_infos).T
    df.head()
    df['dx_mean'] = df.apply(lambda x: get_dx_median(dx, x['x'], x['y'], x['w'], x['h']), axis=1)
    df['rect_ratio'] = df.apply(lambda v: v['rect_arclength'] / 4 / math.sqrt(v['rect_area'] + 1), axis=1)
    df['area_ratio'] = df.apply(lambda v: v['rect_area'] / v['cnt_area'], axis=1)
    df['score'] = df.apply(lambda x: abs(x['rect_ratio'] - 1), axis=1)

    result = df.query('x>0').query('area_ratio<2').query('rect_area>5000').query('rect_area<20000').sort_values(
        ['mean', 'score', 'dx_mean']).head(2)
    if len(result):
        x_left = result.x.values[0]
        # cv2.line(img, (x_left, 0), (x_left, h), color=(255, 0, 255))
        # plt.imshow(img)
        # plt.show()
    return result


def get_track_list(distance):
    """
    模拟轨迹 假装是人在操作
    """
    # 初速度
    v = 0
    # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    t = 0.22
    # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    tracks = []
    # 当前的位移
    current = 0
    # 到达mid值开始减速
    mid = distance * 7 / 8

    distance += 20  # 先滑过一点，最后再反着滑动回来
    # a = random.randint(1,3)
    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a = random.randint(2, 4)  # 加速运动
        else:
            a = -random.randint(3, 5)  # 减速运动

        # 初速度
        v0 = v
        # 0.2秒时间内的位移
        s = v0 * t + 0.5 * a * (t ** 2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))

        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t

    # 反着滑动到大概准确位置
    for i in range(8):
        tracks.append(-random.randint(2, 3))
    for i in range(4):
        tracks.append(-random.randint(1, 3))
    return tracks


if __name__ == "__main__":
    img_path = "../tmp/a.jpg"
    if not os.path.exists(img_path):
        print("文件不存在")
    res = qq_mark_detect(img_path)
    print(res.x.values[0])
