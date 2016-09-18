# -*- coding: utf-8 -*-
# 功能：沿任意方向缩放
# 操作：a和d键改变缩放的方向，w和s键改变缩放的系数，r键复原，每次按键都会将原图在当前的角度+当前的缩放系数的配置下做一次缩放

import numpy as np
import cv2

# 多边形在自己的局部坐标系下的坐标
source_points = np.array([[100, 100, 1], [200, 50, 1], [300, 50, 1], [400, 100, 1], [250, 300, 1]], np.int32)
# 绘制坐标轴的范围
axis_x = np.array([[-500, 0, 1], [500, 0, 1]], np.int32)
axis_y = np.array([[0, -300, 1], [0, 300, 1]], np.int32)

# 多边形局部坐标系相对于屏幕坐标系的变换
base_trans_mat = np.array([[1, 0, 640], [0, 1, 360], [0, 0, 1]], np.int32)

# 缩放的方向
scaling_direction = 0.0
# 缩放的系数
scaling_factor = 1.0


# 把图形转换到屏幕坐标系下并绘制出来
def draw_object_in_screen_coordinate(img_canvas, source_points_screen, axis_x_screen, axis_y_screen, base_trans_matrix):

    # 坐标变成列
    source_points_screen = source_points_screen.transpose()
    axis_x_screen = axis_x_screen.transpose()
    axis_y_screen = axis_y_screen.transpose()

    # 右乘变换矩阵，亦即基的过渡矩阵
    source_points_screen = base_trans_matrix.dot(source_points_screen)
    axis_x_screen = base_trans_matrix.dot(axis_x_screen)
    axis_y_screen = base_trans_matrix.dot(axis_y_screen)

    # 变回行
    source_points_screen = source_points_screen.transpose()
    axis_x_screen = axis_x_screen.transpose()
    axis_y_screen = axis_y_screen.transpose()

    # 切片取前两列
    source_points_screen = source_points_screen[:, :2]
    source_points_screen = source_points_screen.copy()
    source_points_screen = source_points_screen.astype(int)
    axis_x_screen = axis_x_screen[:, :2]
    axis_x_screen = axis_x_screen.copy()
    axis_x_screen = axis_x_screen.astype(int)
    axis_y_screen = axis_y_screen[:, :2]
    axis_y_screen = axis_y_screen.copy()
    axis_x_screen = axis_x_screen.astype(int)

    # 绘制坐标系
    cv2.line(img_canvas, (axis_x_screen[0][0], axis_x_screen[0][1]), (axis_x_screen[1][0], axis_x_screen[1][1]), (255, 255, 0), 3)
    cv2.line(img_canvas, (axis_y_screen[0][0], axis_y_screen[0][1]), (axis_y_screen[1][0], axis_y_screen[1][1]), (255, 255, 0), 3)

    # 绘制多边形
    pts = source_points_screen.reshape((-1, 1, 2))
    cv2.polylines(img_canvas, [pts], True, (0, 255, 255), 3)


# 为缩放方向指针计算旋转矩阵
def calculate_rotate_mat(theta):
    theta = theta * np.pi / 180
    matrix_trans = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return matrix_trans


# 绘制缩放方向指针，对指针来说要做三步变换，1、标识转角的旋转；2、标识缩放系数的缩放；3、变基
def draw_scaling_pointer(img_canvas, mat_rotate, mat_scale, mat_trans_base):
    pointer = np.array([[0, 0, 1], [100, 0, 1]], np.int32)
    pointer = pointer.transpose()
    # 从左到右连接变基、缩放、旋转矩阵
    mat_compose = mat_trans_base.dot(mat_scale.dot(mat_rotate))
    pointer = mat_compose.dot(pointer)

    pointer = pointer.transpose()
    pointer = pointer[:, :2]
    pointer = pointer.copy()
    pointer = pointer.astype(int)

    cv2.line(img_canvas, (pointer[0][0], pointer[0][1]), (pointer[1][0], pointer[1][1]), (255, 0, 0), 3)


# 计算沿theta方向的缩放因子为k的变换矩阵
def calculate_scale_mat(theta, k):
    theta = theta * np.pi / 180
    matrix_scale_ = np.array([[1 + (k - 1) * np.cos(theta) * np.cos(theta), (k - 1) * np.cos(theta) * np.sin(theta), 0],
                             [(k - 1) * np.cos(theta) * np.sin(theta), 1 + (k - 1) * np.sin(theta) * np.sin(theta), 0],
                             [0, 0, 1]])
    return matrix_scale_


# 对多边形施行缩放变换
def perform_scale_trans(points, scale_matrix):
    points = points.transpose()
    points = scale_matrix.dot(points)
    points = points.transpose()
    points = points.astype(int)
    return points


cv2.namedWindow('canvas')
img = np.zeros((720, 1280, 3), np.uint8)
img_draw = img.copy()
draw_object_in_screen_coordinate(img_draw, source_points, axis_x, axis_y, base_trans_mat)
cv2.imshow('canvas', img_draw)

while True:

    key = cv2.waitKey(0) & 0xFF
    img_draw = img.copy()

    if key == ord('a'):
        scaling_direction += 5
    if key == ord('d'):
        scaling_direction -= 5
    if key == ord('w'):
        scaling_factor += 0.1
    if key == ord('s'):
        scaling_factor -= 0.1
    if key == ord('r'):
        scaling_direction = 0.0
        scaling_factor = 1.0
    if key == 27:
        break

    # 计算指针的旋转矩阵
    matrix_rotate = calculate_rotate_mat(scaling_direction)
    # 计算缩放矩阵
    matrix_scale = calculate_scale_mat(scaling_direction, scaling_factor)
    # 对多边形施行缩放
    polygon_points = perform_scale_trans(source_points, matrix_scale)
    draw_scaling_pointer(img_draw, matrix_rotate, matrix_scale, base_trans_mat)
    draw_object_in_screen_coordinate(img_draw, polygon_points, axis_x, axis_y, base_trans_mat)
    cv2.imshow('canvas', img_draw)


cv2.destroyAllWindows()