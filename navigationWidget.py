#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2020/2/27 11:56
# @Email    : spirit_az@foxmail.com
# @Name     : navigationWidget.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
#                                        |asset|shot
# ——————————————————————————————————————————————————
# (typeName|shot) | (assetName|eps_name) | task_name | pipeline |

# ----------------------------------------------------------------------------------------------------
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import math

# ----------------------------------------------------------------------------------------------------
class _mode(object):
    # -True:横向, False:纵向
    __isH = True
    # - {0:居中, 1:(左|上), 2:(右|下)}
    __match = 0
    # dis
    __dis = 80

    # 控件滑动后的数值记录
    __offset = 0

    # 颜色
    __selColor = QtCore.Qt.white
    __unSelColor = QtCore.Qt.gray

    @property
    def isH(self):
        return self.__isH

    @isH.setter
    def isH(self, val):
        self.__isH = val

    @property
    def match(self):
        return self.__match

    @match.setter
    def match(self, val):
        self.__match = val

    @property
    def dis(self):
        return self.__dis

    @dis.setter
    def dis(self, val):
        self.__dis = val

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, val):
        self.__offset = val

    @property
    def selColor(self):
        return self.__selColor

    @selColor.setter
    def selColor(self, QColor):
        self.__selColor = QColor

    @selColor.deleter
    def selColor(self):
        self.__selColor = QtCore.Qt.white

    @property
    def unSelColor(self):
        return self.__unSelColor

    @unSelColor.setter
    def unSelColor(self, QColor):
        self.__unSelColor = QColor

    @unSelColor.deleter
    def unSelColor(self):
        self.__unSelColor = QtCore.Qt.gray


class navigationTitle(QtWidgets.QWidget, _mode):
    currentItemChanged = QtCore.pyqtSignal([int, str])

    def __init__(self, isH=True, match=0, dis=80, parent=None):
        super(navigationTitle, self).__init__(parent)
        self.setMouseTracking(True)
        # 背景颜色
        self.backgroundColor = QtGui.QColor("#ffffff")
        self.currentIndex = 0
        # item 个数
        self.listItems = []
        # 当前选择的项索引
        self.currentIndex = 0
        # 当前光标所在位置的项索引
        self.cursorIndex = -1
        # 鼠标当前位置，用于滑动
        self.c_pos = QtCore.QPoint()
        # 滑动数值
        self.slider = 0

        # 横向还是纵向
        self.isH = isH
        # 布局规则： 左|上， 中间， 右|下
        self.match = match
        # 每一个部件的占位长度
        self.dis = dis
        # 标准初始位置
        self.cOffset = 0

    def offsetChangedIndex(self, val):
        """

        :param val:  1: 右|下， 2: 左上
        :return:
        """
        currentIndex = self.currentIndex
        minVal = 0
        maxVal = len(self.listItems) - 1
        # 得到当前index
        currentIndex += val
        if currentIndex < minVal:
            currentIndex = minVal
        elif currentIndex > maxVal:
            currentIndex = maxVal
        # 如果没有变动，就不执行
        if currentIndex == self.currentIndex:
            return
        # 执行切换
        self.setCurrentIndex(currentIndex)

    def setCurrentIndex(self, idx):
        """
        切换当前所选的界面
        :param idx:
        :return:
        """
        self.currentIndex = idx
        self.currentItemChanged.emit(idx, self.listItems[idx])
        self.update()

    def addItem(self, item):
        """
        添加一个分页
        :param item: 分页的名称
        :return:
        """
        self.listItems.append(item)
        self.update()

    def setItems(self, items):
        """
        设置所有的分页
        :param items:  当前所有分页的名称
        :return:
        """
        self.listItems = items
        self.update()

    def setOffset(self, val):
        """
        item的滑动效果
        :param val:
        :return:
        """
        self.offset = val
        self.update()

    def __getPos(self):
        """
        得到每一个item的pos
        :return: [width, height]
        """
        isH, match = self.isH, self.match
        itemLength = len(self.listItems)
        itemsDis = self.dis * itemLength

        h, w = self.height(), self.width()

        # 得到坐标位置
        tDis = w if isH else h
        if match == 0:
            self.cOffset = (tDis - itemsDis) * 0.5
        elif match == 1:
            self.cOffset = 0
        else:
            self.cOffset = tDis - itemsDis

        self.cOffset += self.offset
        self.cOffset += self.slider

        Xs = [[self.cOffset + i * self.dis, 0] for i in range(itemLength)]
        if not isH:
            list(map(lambda x: x.reverse(), Xs))

        return Xs

    def setBackGroundColor(self, QColor):
        self.backgroundColor = QColor
        self.update()

    def paintEvent(self, evt):
        """
        绘制背景
        :param evt:
        :return:
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # 画背景色
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawRect(self.rect())

        # 得到item的位置坐标
        pos = self.__getPos()

        # 画子项

        pSize = (self.dis, self.height()) if self.isH else (self.width(), self.dis)

        for (i, (x, y)) in enumerate(pos):
            itemPath = QtGui.QPainterPath()
            if self.isH:
                rectX, rectY = pSize[0] - 1, pSize[1] / 10 - 1
                rectPx, rectPy = x, y + pSize[1] * 0.9 + 1
            else:
                rectX, rectY = pSize[0] / 30 - 1, pSize[1] - 1
                rectPx, rectPy = x, y
            itemPath.addRect(QtCore.QRectF(rectPx, rectPy, rectX, rectY))

            # 设置绘制字体
            font = QtGui.QFont()
            font.setFamily('Microsoft Yahei')
            font.setPointSize(12)

            if i == self.currentIndex and i == self.cursorIndex:
                font.setPointSize(16)
            elif i == self.currentIndex or i == self.cursorIndex:
                font.setPointSize(15)

            painter.setFont(font)

            # 开始绘制
            if i == self.currentIndex:
                painter.setPen(self.selColor)
                painter.fillPath(itemPath, self.selColor)
                painter.drawText(QtCore.QRect(x, y, pSize[0], pSize[1]),
                                 QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, self.listItems[i])
            elif i == self.cursorIndex:
                painter.setPen(self.selColor)
                painter.drawText(QtCore.QRect(x, y, pSize[0], pSize[1]),
                                 QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, self.listItems[i])

            else:
                painter.setPen(self.unSelColor)
                painter.drawText(QtCore.QRect(x, y, pSize[0], pSize[1]),
                                 QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, self.listItems[i])

        painter.end()

    def mouseMoveEvent(self, event):
        """
        中间为滑动效果，其他为鼠标经过效果
        :param event:
        :return:
        """
        if event.buttons() == QtCore.Qt.MiddleButton:
            if self.m_pressed:
                movePos = event.globalPos() - self.c_pos
                self.slider = movePos.x() if self.isH else movePos.y()
                event.accept()
                self.update()
        else:
            evtL = event.x() if self.isH else event.y()
            evtL -= self.cOffset
            idx = int(evtL / self.dis)
            if idx >= len(self.listItems):
                idx = -1
            if idx < len(self.listItems) and idx != self.cursorIndex:
                self.update()
                self.cursorIndex = idx

    def mousePressEvent(self, QMouseEvent):
        """
        中间为滑动效果，其他为选中效果
        :param QMouseEvent:
        :return:
        """
        if QMouseEvent.buttons() == QtCore.Qt.MiddleButton:
            self.c_pos = QMouseEvent.globalPos()  # - self.pos() # type: QtCore.QPoint
            self.m_pressed = True
        elif QMouseEvent.button() == QtCore.Qt.RightButton:
            # 恢复初始化位置
            self.setOffset(0)
        else:
            evtL = QMouseEvent.x() if self.isH else QMouseEvent.y()
            evtL -= self.cOffset
            idx = int(evtL / self.dis)
            if 0 <= idx < len(self.listItems):
                self.currentIndex = idx
                self.currentItemChanged.emit(idx, self.listItems[idx])
                self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_pressed = False
        self.offset += self.slider
        self.slider = 0

    def leaveEvent(self, QMouseEvent):
        self.cursorIndex = -1
        self.update()


class navigationWidget(QtWidgets.QWidget):
    def __init__(self, isH=True, match=0, dis=80, fixSize=40, parent=None):
        """
        # 竖向
        uiH = navigationWidget(isH=False, match=0, dis=40, fixSize=120)
        # 横向
        uiV = navigationWidget(isH=True, match=0, dis=120, fixSize=40)

        :param isH:  title为横向还是竖向
        :param match:  对齐关系， 左上|居中|右下
        :param dis: item的占位
        :param fixSize: title的占位
        :param parent:父物体控件
        """
        super(navigationWidget, self).__init__(parent=parent)
        if isH:
            lay = QtWidgets.QVBoxLayout(self)
        else:
            lay = QtWidgets.QHBoxLayout(self)
        lay.setSpacing(0)
        # lay.setContentsMargins(0, 0, 0, 0)
        self.navigationTitle = navigationTitle(isH, match, dis, self)
        if isH:
            self.navigationTitle.setFixedHeight(fixSize)
        else:
            self.navigationTitle.setFixedWidth(fixSize)

        lay.addWidget(self.navigationTitle)

        self.centralWidget = QtWidgets.QWidget(self)
        lay.addWidget(self.centralWidget)

        self.currentItemChanged = self.navigationTitle.currentItemChanged

    def setItems(self, items):
        items = ['%s' % item for item in items]
        self.navigationTitle.setItems(items)

    def setSelectColor(self, QColor):
        self.navigationTitle.selColor = QColor

    def setUnSelectColor(self, QColor):
        self.navigationTitle.unSelColor = QColor

    def setBackGroundColor(self, QColor):
        self.navigationTitle.setBackGroundColor(QColor)

    def _tmpInitUI(self):
        self.label = QtWidgets.QLabel('当前是第0页', self.centralWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        lay = QtWidgets.QHBoxLayout()
        self.centralWidget.setLayout(lay)
        lay.addWidget(self.label)
        self.currentItemChanged.connect(self._tmpClicked)

    def _tmpClicked(self, int, str):
        self.label.setText('当前是第{}页'.format(int))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # 页码0
    titleList = ['页码%d' % i for i in range(50)]
    # # 竖向
    uiH = navigationWidget(isH=False, match=1, dis=40, fixSize=120)
    # 设置分页数
    uiH.setItems(titleList)
    # 设置尺寸
    uiH.resize(600, 400)
    # 设置背景颜色
    uiH.setBackGroundColor(QtGui.QColor("#E4E4E4"))
    # 设置颜色
    uiH.setSelectColor(QtGui.QColor('#2CA7F8'))
    uiH.setUnSelectColor(QtGui.QColor('#202020'))
    # 显示窗口
    uiH._tmpInitUI()
    uiH.show()
    # 横向
    uiV = navigationWidget(isH=True, match=1, dis=120, fixSize=40)
    # 设置分页数
    uiV.setItems(titleList)
    # 设置尺寸
    uiV.resize(600, 400)
    # 设置背景颜色
    uiV.setBackGroundColor(QtGui.QColor("#E4E4E4"))
    # 设置颜色
    uiV.setSelectColor(QtGui.QColor('#2CA7F8'))
    uiV.setUnSelectColor(QtGui.QColor('#202020'))
    # 显示窗口
    uiV._tmpInitUI()
    uiV.show()
    app.exec_()
