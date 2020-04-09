#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Time      : 2020/4/9 16:17
# Email     : spirit_az@foxmail.com
# File      : gifPlayer.py
__author__ = 'ChenLiang.Miao'
# import --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
from PyQt5 import QtWidgets as QtWidgets
from PyQt5 import QtGui as QtGui
from PyQt5 import QtCore as QtCore


# function +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
class gifPlayer(QtWidgets.QWidget):
    # 拖拽判定
    m_pressed = False

    def __init__(self, filename, parent=None):
        super(gifPlayer, self).__init__(parent=parent)

        # 自动填充
        self.setAutoFillBackground(True)
        # 可推拽
        self.setMouseTracking(True)
        # 无边框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.movie_screen = QtWidgets.QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)

        # Create the layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        # 加载动图
        self.movie = QtGui.QMovie(filename, QtCore.QByteArray(), self)
        # 设置尺寸
        self.resize(self.movie.scaledSize())
        # 缓存： 无限循环播放
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        # 播放速度为1
        self.movie.setSpeed(100)
        # 加载到UI中
        self.movie_screen.setMovie(self.movie)
        # 开始播放
        self.movie.start()

    # 设置窗口可被拖动+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--#
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.c_pos = event.globalPos() - self.pos()
            self.m_pressed = True

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.m_pressed:
                self.move(event.globalPos() - self.c_pos)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.m_pressed = False

    def keyPressEvent(self, QKeyEvent):
        # super(gifPlayer, self).keyPressEvent()
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers & QtCore.Qt.ControlModifier | modifiers & QtCore.Qt.ShiftModifier:
            print('active')

    def keyReleaseEvent(self, QKeyEvent):
        print('active close')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ui = gifPlayer('demo/gifPlayer.gif')
    ui.show()
    app.exec_()
