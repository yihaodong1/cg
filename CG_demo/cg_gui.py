#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QDialog,
    QSlider,
    QVBoxLayout,
    QInputDialog,
    QMessageBox,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QPen
from PyQt5.QtCore import QRectF, Qt

class NewWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.s1 = QSlider(Qt.Horizontal)
        self.s2 = QSlider(Qt.Horizontal)
        self.s3 = QSlider(Qt.Horizontal)

        self.s1.setMinimum(0)
        self.s1.setMaximum(255)
        self.s1.setValue(0)
        self.s1.setTickPosition(QSlider.TicksBelow)
        self.s1.setTickInterval(5)
        self.s1.setStyleSheet("""
            QSlider::groove:horizontal {
                background-color: #ddd;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
                background-color: red;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background-color: red;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
        """)
        self.value_label1 = QLabel(str(self.s1.value()))
        self.value_label1.setAlignment(Qt.AlignCenter)  # 居中对齐
        # 连接滑块的 valueChanged 信号到更新标签的槽函数
        self.s1.valueChanged.connect(self.update_label1)

        self.value_label2 = QLabel(str(self.s2.value()))
        self.value_label2.setAlignment(Qt.AlignCenter)  # 居中对齐
        # 连接滑块的 valueChanged 信号到更新标签的槽函数
        self.s2.valueChanged.connect(self.update_label2)

        self.value_label3 = QLabel(str(self.s3.value()))
        self.value_label3.setAlignment(Qt.AlignCenter)  # 居中对齐
        # 连接滑块的 valueChanged 信号到更新标签的槽函数
        self.s3.valueChanged.connect(self.update_label3)

        self.s2.setMinimum(0)
        self.s2.setMaximum(255)
        self.s2.setValue(0)
        self.s2.setTickPosition(QSlider.TicksBelow)
        self.s2.setTickInterval(5)
        self.s2.setStyleSheet("""
            QSlider::groove:horizontal {
                background-color: #ddd;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
                background-color: green;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background-color: green;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
        """)

        self.s3.setMinimum(0)
        self.s3.setMaximum(255)
        self.s3.setValue(0)
        self.s3.setTickPosition(QSlider.TicksBelow)
        self.s3.setTickInterval(5)
        self.s3.setStyleSheet("""
            QSlider::groove:horizontal {
                background-color: #ddd;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
                background-color: blue;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background-color: blue;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
        """)
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)  # 点击后关闭弹窗

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.s1)
        self.layout.addWidget(self.value_label1)
        self.layout.addWidget(self.s2)
        self.layout.addWidget(self.value_label2)
        self.layout.addWidget(self.s3)
        self.layout.addWidget(self.value_label3)
        self.layout.addWidget(self.ok_button)
        self.setLayout(self.layout)
        self.setWindowTitle('子窗口')
        self.resize(280, 230)
    def update_label1(self):
        # 更新标签显示当前滑块的值
        self.value_label1.setText(str(self.s1.value()))

    def update_label2(self):
        # 更新标签显示当前滑块的值
        self.value_label2.setText(str(self.s2.value()))

    def update_label3(self):
        # 更新标签显示当前滑块的值
        self.value_label3.setText(str(self.s3.value()))

    def get_slider_value(self):
        # 返回滑块的当前值
        return self.s1.value(), self.s2.value(), self.s3.value()



class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.pen = QPen(QColor(0,0,0))

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.temp_algorithm = None
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_clip(self, algorithm, item_id):
        self.status = 'clip'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_translate(self, item_id):
        self.status = 'translate'
        self.temp_id = item_id

    def start_rotate(self, item_id):
        self.status = 'rotate'
        self.temp_id = item_id

    def start_scale(self, item_id):
        self.status = 'scale'
        self.temp_id = item_id

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.pen)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            if(self.temp_item == None):
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.pen)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y])
        elif self.status == 'curve':
            if(event.button() == Qt.LeftButton):
                if(self.temp_item == None):
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.pen)
                    self.scene().addItem(self.temp_item)
                else:
                    self.temp_item.p_list.append([x, y])
        elif self.status == 'clip':
            if(self.selected_id != ''):
                p_list = self.item_dict[self.selected_id].p_list
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y], p_list], self.temp_algorithm, self.pen)
                self.item_dict[self.selected_id].p_list = alg.clip(p_list,\
                                                                   x, y, x, y, self.temp_algorithm)
        elif self.status == 'scale':
            if(self.selected_id != ''):
                p_list = self.item_dict[self.selected_id].p_list
                centerx = int(sum(pos[0] for pos in p_list) / len(p_list))
                centery = int(sum(pos[1] for pos in p_list) / len(p_list))
                radius = math.sqrt((x - centerx)**2 + (y - centery)**2)
                self.temp_item = MyItem(self.temp_id, self.status, [[centerx, centery, radius], p_list], self.temp_algorithm, self.pen)
                self.item_dict[self.selected_id].p_list = alg.rotate(p_list, centerx, centery, 0)

        elif self.status == 'rotate':
            if(self.selected_id != ''):
                p_list = self.item_dict[self.selected_id].p_list
                centerx = int(sum(pos[0] for pos in p_list) / len(p_list))
                centery = int(sum(pos[1] for pos in p_list) / len(p_list))
                self.temp_item = MyItem(self.temp_id, self.status, [[centerx, centery], [x, y], p_list], self.temp_algorithm, self.pen)
                self.item_dict[self.selected_id].p_list = alg.rotate(p_list, centerx, centery, 0)

        elif self.status == 'translate':
            if(self.selected_id != ''):
                p_list = self.item_dict[self.selected_id].p_list
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y, 0, 0]], self.temp_algorithm, self.pen)
                self.item_dict[self.selected_id].p_list = alg.translate(p_list, 0, 0)

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def cal_theta(self, x1, y1, x2, y2):
        cos_theta = (x1 * x2 + y1 * y2) / (math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2))
        sin_theta = (x1 * y2 - x2 * y1) / (math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2))
        theta = math.atan(sin_theta / cos_theta) * 180 / math.pi
        if cos_theta < 0 and sin_theta < 0:
            theta -= 180
        elif cos_theta < 0 and sin_theta > 0:
            theta += 180
        return theta

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        if self.status == 'polygon':
            self.temp_item.p_list[-1] = [x, y]
            startx, starty = self.temp_item.p_list[0]
            endx, endy = self.temp_item.p_list[-1]
             #多边形，最少为三角形
            if(len(self.temp_item.p_list) >= 4\
                   and math.fabs((endx - startx)**2 + (endy - starty)**2) < 100):# 100 to be discussed
                self.temp_item.p_list[-1] = self.temp_item.p_list[0]
        elif self.status == 'clip':
            if(self.selected_id != ''):
                self.temp_item.p_list[1] = [x, y]
                startx, starty = self.temp_item.p_list[0]
                p_list = self.temp_item.p_list[2]
                x0 = min(startx, x)
                y0 = min(starty, y)
                x1 = max(startx, x)
                y1 = max(starty, y)
                self.item_dict[self.selected_id].p_list = alg.clip(p_list, \
                                                                   x0, y0, x1, y1, self.temp_algorithm)
        elif self.status == 'scale':
            if(self.selected_id != ''):
                centerx, centery, start_r = self.temp_item.p_list[0]
                p_list = self.temp_item.p_list[1]
                radius = math.sqrt((x - centerx)**2 + (y - centery)**2)
                self.item_dict[self.selected_id].p_list = alg.scale(p_list, \
                                                                   centerx, centery, radius / start_r)

        elif self.status == 'rotate':
            if(self.selected_id != ''):
                centerx, centery= self.temp_item.p_list[0]
                startx, starty = self.temp_item.p_list[1]
                p_list = self.temp_item.p_list[2]
                theta = int(self.cal_theta(startx - centerx, starty - centery, x - centerx, y - centery))
                self.item_dict[self.selected_id].p_list = alg.rotate(p_list, \
                                                                   centerx, centery, theta)

        elif self.status == 'translate':
            if(self.selected_id != ''):
                startx, starty, dx, dy = self.temp_item.p_list[0]
                self.temp_item.p_list[0][2] = x - startx
                self.temp_item.p_list[0][3] = y - starty
                self.item_dict[self.selected_id].p_list = alg.translate(self.item_dict[self.selected_id].p_list,\
                                                                   x - startx - dx, y - starty - dy)
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line' or self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
            self.temp_item = None
        elif self.status == 'polygon':
            startx, starty = self.temp_item.p_list[0]
            endx, endy = self.temp_item.p_list[-1]
             #多边形，最少为三角形
            if(len(self.temp_item.p_list) >= 4\
                   and math.fabs((endx - startx)**2 + (endy - starty)**2) < 100):# 100 to be discussed
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
                self.temp_item = None
        elif self.status == 'curve':
            if(event.button() == Qt.RightButton and self.temp_item != None):
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
                self.temp_item = None

        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', pen: QPen = QPen(QColor(0,0,0)), parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.pen = pen

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.pen)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            # item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            if len(self.p_list) >= 2:
                item_pixels = []
                for i in range(len(self.p_list) - 1):
                    item_pixels = item_pixels + alg.draw_line(self.p_list[i: i + 2], self.algorithm)
                for p in item_pixels:
                    painter.drawPoint(*p)
                if self.selected:
                    painter.setPen(QColor(255, 0, 0))
                    painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line' or\
            self.item_type == 'polygon' or\
            self.item_type == 'ellipse' or\
            self.item_type == 'curve':
            xmin = min(pos[0] for pos in self.p_list)
            ymin = min(pos[1] for pos in self.p_list)
            w = max(pos[0] for pos in self.p_list) - xmin
            h = max(pos[1] for pos in self.p_list) - ymin
            return QRectF(xmin - 1, ymin - 1, w + 2, h + 2)

            # x0, y0 = self.p_list[0]
            # x1, y1 = self.p_list[1]
            # x = min(x0, x1)
            # y = min(y0, y1)
            # w = max(x0, x1) - x
            # h = max(y0, y1) - y
            # return QRectF(x - 1, y - 1, w + 2, h + 2)
        # elif self.item_type == 'polygon':
        #     pass
        # elif self.item_type == 'ellipse':
        #     pass
        # elif self.item_type == 'curve':
        #     pass


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        set_pen_act.triggered.connect(self.set_pen_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        translate_act.triggered.connect(self.translate_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        scale_act.triggered.connect(self.scale_action)
        rotate_act.triggered.connect(self.rotate_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def reset_canvas_action(self):
        self.list_widget.currentTextChanged.disconnect(self.canvas_widget.selection_changed)
        self.canvas_widget.clear_selection()
        self.scene.clear()
        self.list_widget.clear()
        self.item_cnt = 0
        self.canvas_widget.item_dict = {}
        self.canvas_widget.selected_id = ''
        self.canvas_widget.status = ''
        self.canvas_widget.temp_algorithm = ''
        self.canvas_widget.temp_id = ''
        self.canvas_widget.temp_item = None
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

    def set_pen_action(self):
        # name, ok = QInputDialog.getText(self.central_widget, "修改姓名", '请输入姓名')
        
        new = NewWindow()
        new.show()
        if new.exec_() == QDialog.Accepted:
            # 如果用户点击“确定”，获取滑块的值并更新标签
            r,g,b = new.get_slider_value()
            self.canvas_widget.pen = QPen(QColor(r, g, b))
        self.canvas_widget.clear_selection()

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('中点圆算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip('Cohen-Sutherland', self.get_id())
        self.statusBar().showMessage('Cohen-Sutherland算法裁剪')

    def clip_liang_barsky_action(self):
        pass

    def translate_action(self):
        self.canvas_widget.start_translate(self.get_id())
        if self.canvas_widget.selected_id != '':
            self.statusBar().showMessage('平移')
        else:
            self.statusBar().showMessage('请先选择一个图元')

    def rotate_action(self):
        self.canvas_widget.start_rotate(self.get_id())
        if self.canvas_widget.selected_id != '':
            self.statusBar().showMessage('旋转')
        else:
            self.statusBar().showMessage('请先选择一个图元')

    def scale_action(self):
        self.canvas_widget.start_scale(self.get_id())
        if self.canvas_widget.selected_id != '':
            self.statusBar().showMessage('缩放')
        else:
            self.statusBar().showMessage('请先选择一个图元')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
