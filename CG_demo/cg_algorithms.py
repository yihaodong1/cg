#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if math.fabs(x0 - x1) > math.fabs(y0 - y1):
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
        else:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (x1 - x0) / (y1 - y0)
            for y in range(y0, y1 + 1):
                result.append((int(x0 + k * (y - y0)), y))

    elif algorithm == 'Bresenham':
        steep = math.fabs(y0 - y1) > math.fabs(x0 - x1)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        deltax = x1 - x0
        deltay = math.fabs(y1 - y0)
        error = int(deltax / 2)
        ystep = 1 if y0 < y1 else -1
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                result.append((y, x))
            else:
                result.append((x, y))
            error = error - deltay
            if error < 0:
                y = y + ystep
                error = error + deltax
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    a = math.fabs(x0 - x1) / 2
    b = math.fabs(y0 - y1) / 2
    center = [int((x0 + x1) / 2), int((y0 + y1) / 2)]
    xpos, ypos = 0, int(b)
    d = b**2 + a**2 * (ypos - 0.5)**2 - a**2 * b**2
    result = []
    tmp = []
    while a**2 * ypos > b**2 * xpos:
        tmp.append([xpos, ypos])
        if d < 0:
            d = d + b**2 * ((xpos * 2) + 3)
            xpos = xpos + 1
        else:
            d = d + b**2 * ((xpos * 2) + 3) + a**2 * (-(ypos * 2) + 2)
            xpos = xpos + 1
            ypos = ypos - 1

    d = b**2 * (xpos + 0.5) * (xpos + 0.5) + a**2 * (ypos - 1) * (ypos - 1) - a**2 * b**2
    while ypos > 0:
        tmp.append([xpos, ypos])
        if d < 0:
            d = d + b**2 * ((xpos * 2) + 2) + a**2 * (-(ypos * 2) + 3)
            xpos = xpos + 1
            ypos = ypos - 1
        else:
            d = d + a**2 * (-(ypos * 2) + 3)
            ypos = ypos - 1
    result = []
    result = result + [[pos[0]+center[0], pos[1] + center[1]] for pos in tmp]
    result = result + [[-pos[0]+center[0], pos[1] + center[1]] for pos in tmp]
    result = result + [[pos[0]+center[0], -pos[1] + center[1]] for pos in tmp]
    result = result + [[-pos[0]+center[0], -pos[1] + center[1]] for pos in tmp]
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    pass


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for pos in p_list:
        pos[0] = pos[0] + dx
        pos[1] = pos[1] + dy
        result.append(pos)
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def encode(x, y, x_min, y_min, x_max, y_max):
    """编码
    """
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8
    code = 0
    if x < x_min:
        code = code | LEFT
    elif x > x_max:
        code = code | RIGHT
    if y < y_min:
        code = code | BOTTOM
    elif y > y_max:
        code = code | TOP
    return code

def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if algorithm == 'Cohen-Sutherland':
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8
        x_0, y_0 = x0, y0
        x_1, y_1 = x1, y1
        while(True):
            c0 = encode(x_0, y_0, x_min, y_min, x_max, y_max)
            c1 = encode(x_1, y_1, x_min, y_min, x_max, y_max)
            if c0 == 0 and c1 == 0:
                return [[x_0, y_0], [x_1, y_1]]
            elif c0 & c1 != 0:
                return [[0, 0], [0, 0]]
            else:
                result = []
                if c0 != 0:
                    if c0 & LEFT:
                        x_0, y_0 = x_min, int(y0 + (y1 - y0) / (x1 - x0) * (x_min - x0))
                    elif c0 & RIGHT:
                        x_0, y_0 = x_max, int(y0 + (y1 - y0) / (x1 - x0) * (x_max - x0))
                    elif c0 & BOTTOM:
                        x_0, y_0 = int(x0 + (x1 - x0) / (y1 - y0) * (y_min - y0)), y_min
                    elif c0 & TOP:
                        x_0, y_0 = int(x0 + (x1 - x0) / (y1 - y0) * (y_max - y0)), y_max
                if c1 != 0:
                    if c1 & LEFT:
                        x_1, y_1 = x_min, int(y1 + (y1 - y0) / (x1 - x0) * (x_min - x1))
                    elif c1 & RIGHT:
                        x_1, y_1 = x_max, int(y1 + (y1 - y0) / (x1 - x0) * (x_max - x1))
                    elif c1 & BOTTOM:
                        x_1, y_1 = int(x1 + (x1 - x0) / (y1 - y0) * (y_min - y1)), y_min
                    elif c1 & TOP:
                        x_1, y_1 = int(x1 + (x1 - x0) / (y1 - y0) * (y_max - y1)), y_max


    elif algorithm == 'Liang-Barsky':
        result = []
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]

        p = [x0-x1, x1-x0, y0-y1, y1-y0]
        q = [x0-x_min, x_max-x0, y0-y_min, y_max-y0]
        u0, u1 = 0, 1

        for i in range(4):
            if p[i] < 0:
                u0 = max(u0, q[i]/p[i])
            elif p[i] > 0:
                u1 = min(u1, q[i]/p[i])
            elif (p[i] == 0 and q[i] < 0):
                result = [[0,0], [0,0]]
                return result
            if u0 > u1:
                result = [[0,0], [0,0]]
                return result

        res_x0, res_y0, res_x1, res_y1 = x0, y0, x1, y1
        if u0 > 0:
            res_x0 = int(x0 + u0*(x1-x0) + 0.5)
            res_y0 = int(y0 + u0*(y1-y0) + 0.5)
        if u1 < 1:
            res_x1 = int(x0 + u1*(x1-x0) + 0.5)
            res_y1 = int(y0 + u1*(y1-y0) + 0.5)
        result = [[res_x0, res_y0], [res_x1, res_y1]]

        return result
