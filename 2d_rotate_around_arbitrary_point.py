# -*- coding: utf-8 -*-
# 功能：
# 绘制一个五边形，可以绕任意点进行2d旋转
# 操作说明：
# 鼠标双击改变旋转的锚点，键盘a键逆时针旋转，d键顺时针旋转，当然...是在右手系下

import numpy as np
import cv2

# 旋转的锚点，初始化为原点
anchor_point = (0, 0)
# 旋转角度
rotate_theta = 0.0
# 变换结果
source_points = np.array([[100, 100, 1], [200, 50, 1], [300, 50, 1], [400, 100, 1], [250, 300, 1]], np.int32)
destination_points = source_points.copy()

# 定义鼠标回调，双击会修改旋转的锚点
def mouse_func(event, x, y, flags, param):
    global anchor_point
    global rotate_theta
    global source_points
    global destination_points
    if event == cv2.EVENT_LBUTTONDBLCLK:
        anchor_point = (x, y)
        cv2.circle(img_canvas, anchor_point, 3, (255, 0, 0), -1)
        cv2.imshow('canvas', img_canvas)
        # 双击之后改变了锚点，转角也应该清零，不然在上次累积的转角上继续，看起来有跳变
        rotate_theta = 0
        # 同时应该要把变换源图形改成目前更改过的图形
        source_points = destination_points


# 根据锚点和旋转角度计算变换矩阵
def calculate_trans_mat(theta, anchor):
    theta = theta * np.pi / 180
    matrix_trans = np.array([[np.cos(theta), -np.sin(theta), -anchor[0] * np.cos(theta) + anchor[1] * np.sin(theta) + anchor[0]],
                       [np.sin(theta), np.cos(theta), -anchor[0] * np.sin(theta) - anchor[1] * np.cos(theta) + anchor[1]],
                       [0, 0, 1]])
    return matrix_trans


# 实际施行变换
def perform_trans(points, trans_matrix):
    # 转置之后每一列都是一个点的坐标
    pts_array = points.transpose()
    # 直接用所有点的坐标构成的矩阵右乘变换矩阵结果得到所有的变换之后的坐标
    pts_array = trans_matrix.dot(pts_array)
    pts_array = pts_array.transpose()
    return pts_array


def draw_polygon(pts_list_, img_):
    slice_t = pts_list_[:, :2]
    pts = slice_t.copy()
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img_, [pts.astype(int)], True, (0, 255, 255), 3)
    cv2.circle(img_, anchor_point, 3, (255, 0, 0), -1)


cv2.namedWindow('canvas')
cv2.setMouseCallback('canvas', mouse_func)
img = np.zeros((720, 1280, 3), np.uint8)
img_canvas = img.copy()


# 旋转之前绘制源图形
ppp = source_points[:, :2]
ppp = ppp.copy()
ppp = ppp.reshape((-1, 1, 2))
cv2.polylines(img_canvas, [ppp], True, (0, 255, 255), 3)
cv2.imshow('canvas', img_canvas)

while True:

    key = cv2.waitKey(0) & 0xFF
    img_canvas = img.copy()

    if key == ord('a'):
        rotate_theta += 5
        matrix = calculate_trans_mat(rotate_theta, anchor_point)
        destination_points = perform_trans(source_points, matrix)
        draw_polygon(destination_points, img_canvas)
        cv2.imshow('canvas', img_canvas)
    if key == ord('d'):
        rotate_theta -= 5
        matrix = calculate_trans_mat(rotate_theta, anchor_point)
        destination_points = perform_trans(source_points, matrix)
        draw_polygon(destination_points, img_canvas)
        cv2.imshow('canvas', img_canvas)
    if key == 27:
        break


cv2.destroyAllWindows()
