# -*- coding: utf-8 -*-

import numpy as np
import cv2


# 转rgb并显示
def convert_update(*args):

    channel_one = cv2.getTrackbarPos('channel_one', 'control')
    channel_two = cv2.getTrackbarPos('channel_two', 'control') / 100.0
    channel_three = cv2.getTrackbarPos('channel_three', 'control') / 100.0

    img = np.zeros((600, 800, 3), np.float32)
    img[:, :, 0] = channel_one
    img[:, :, 1] = channel_two
    img[:, :, 2] = channel_three
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    cv2.imshow('converted_img', img)


# 控制面板创建
def control_window():

    cv2.namedWindow('control', 0)
    cv2.createTrackbar('channel_one', 'control', 180, 360, convert_update)
    cv2.createTrackbar('channel_two', 'control', 50, 100, convert_update)
    cv2.createTrackbar('channel_three', 'control', 50, 100, convert_update)

cv2.namedWindow('converted_img')
control_window()
cv2.waitKey(0)
cv2.destroyAllWindows()
