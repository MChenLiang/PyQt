#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2020/3/2 16:25
# @Email    : spirit_az@foxmail.com
# @Name     : pageWidget.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
from functools import partial
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import QSS


# ----------------------------------------------------------------------------------------------------
# 页码数
class pageLineEditor(QtWidgets.QLineEdit):
    textModified = QtCore.pyqtSignal(str)

    def __init__(self, index, parent=None):
        self._before = str(index)
        super(pageLineEditor, self).__init__(self._before, parent)
        self.setFrame(False)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.returnPressed.connect(self.checkText)

        self.setFixedWidth(25)

        self.setStyleSheet(QSS.page_lineEdit)

    def setMax(self, index):
        self.validator = QtGui.QIntValidator(1, index, self)
        self.setValidator(self.validator)

    def setText(self, p_str):
        self._before = str(p_str)
        super(pageLineEditor, self).setText(self._before)

    def focusInEvent(self, event):
        if event.reason() != QtCore.Qt.PopupFocusReason:
            self._before = self.text()
        super(pageLineEditor, self).focusInEvent(event)

    def focusOutEvent(self, event):
        if event.reason() != QtCore.Qt.PopupFocusReason:
            self.checkText()
        super(pageLineEditor, self).focusOutEvent(event)

    def checkText(self):
        if self._before != self.text():
            self._before = self.text()
            self.textModified.emit(self._before)


# 页码条里的label
class pageLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)

    __isSelected = False

    @property
    def isSelected(self):
        return self.__isSelected

    @isSelected.setter
    def isSelected(self, val):
        self.__isSelected = val

    @isSelected.deleter
    def isSelected(self):
        self.__isSelected = False

    def __init__(self, p_str, *args):
        p_str = str(p_str)
        super(pageLabel, self).__init__(p_str, *args)
        self.isLock = False
        self.setStyleSheet(QSS.page_noSelected)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(25, 25)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit(self.text())

    def setLock(self, val):
        if val:
            self.setText('...')
            self.isLock = True
        else:
            self.isLock = False
        self.setSelected(self.isSelected)

    def setSelected(self, val):
        self.isSelected = False
        if self.isLock:
            self.setStyleSheet(QSS.page_lock)
        elif val:
            self.setStyleSheet(QSS.page_selected)
            self.isSelected = True
        else:
            self.setStyleSheet(QSS.page_noSelected)

    def setText(self, p_str):
        super(pageLabel, self).setText(str(p_str))


# 页码条
class navigationpages(QtWidgets.QWidget):
    valueChanged = QtCore.pyqtSignal(int, int)
    itemChanged = QtCore.pyqtSignal(int)
    _pageMax = 10
    _totalNumber = 5000

    @property
    def totalNumber(self):
        return self._totalNumber

    @totalNumber.setter
    def totalNumber(self, val):
        self._totalNumber = val

    @totalNumber.deleter
    def totalNumber(self):
        self._totalNumber = 5000

    @property
    def pageMax(self):
        return self._pageMax

    @pageMax.setter
    def pageMax(self, val):
        self._pageMax = val
        self.lineEditor_current.setMax(val)
        # 把所有的页码都隐藏
        for page in self.numberPage:
            page.setHidden(True)

        # 把范围内的全部显示出来
        maxNum = self.pageMax if self.pageMax < 8 else 8
        for i in range(maxNum):
            page = self.numberPage[i]
            page.setHidden(False)

        # 初始化页数
        self.maxNumber.setText(str(val))
        # 设置最后一页为最大值
        self.label08.setText(self.pageMax)

        if self.pageMax == 8:
            self.label07.setText(7)

    @pageMax.deleter
    def pageMax(self):
        self._pageMax = 20

    def __init__(self, parent=None):
        super(navigationpages, self).__init__(parent)
        # 当前每页的可选条目
        self.pageItemN = [200, 500, 1000]
        # 当前每页条目
        self.pageItemNumber = self.pageItemN[1]
        # 当前页码
        self.pageNumber = 0
        self.initUI()
        self.btClicked()

    def initUI(self):
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        # 每页多少个
        self.itemNumber_001 = pageLabel(self.pageItemN[0])
        self.itemNumber_002 = pageLabel(self.pageItemN[1])
        self.itemNumber_002.setSelected(True)
        self.itemNumber_003 = pageLabel(self.pageItemN[2])

        self.itemNumber = [self.itemNumber_001, self.itemNumber_002, self.itemNumber_003]
        for l in self.itemNumber:
            l.setFixedWidth(40)
            lay.addWidget(l)
        # 加个弹簧顶起来
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        lay.addItem(spacerItem)
        # 页码
        label = QtWidgets.QLabel('Page')
        label.setAlignment(QtCore.Qt.AlignCenter)
        lay.addWidget(label)
        self.lineEditor_current = pageLineEditor(0, self)
        self.lineEditor_current.setMax(self.pageMax)
        lay.addWidget(self.lineEditor_current)
        label = QtWidgets.QLabel('of')
        label.setAlignment(QtCore.Qt.AlignCenter)
        lay.addWidget(label)
        self.maxNumber = QtWidgets.QLabel('%s' % self.pageMax)
        self.maxNumber.setAlignment(QtCore.Qt.AlignCenter)
        lay.addWidget(self.maxNumber)

        # 页码
        self.upPage = pageLabel('<<')
        self.label01 = pageLabel('1')
        self.label02 = pageLabel('2')
        self.label03 = pageLabel('3')
        self.label04 = pageLabel('4')
        self.label05 = pageLabel('5')
        self.label06 = pageLabel('6')
        self.label07 = pageLabel('...')
        self.label08 = pageLabel('10')
        self.dnPage = pageLabel('>>')

        self.numberPage = [self.label01, self.label02, self.label03, self.label04,
                           self.label05, self.label06, self.label07, self.label08]

        self.numberUpPage = [self.label01, self.label02, self.label03, self.label04,
                             self.label05, self.label06]

        self.numberDnPage = [self.label03, self.label04,
                             self.label05, self.label06, self.label07, self.label08]

        self.numberMdPage = [self.label03, self.label04, self.label05, self.label06]

        lay.addWidget(self.upPage)
        for l in self.numberPage:
            lay.addWidget(l)
        lay.addWidget(self.dnPage)

        self.setSelected(self.label01, 1)

    def btClicked(self):
        # 页码数
        for item in self.itemNumber:
            item.clicked.connect(self.itemNumber_clicked_connect)

        # 页码条
        for l in self.numberPage:
            l.clicked.connect(partial(self.setSelected, l))

        self.upPage.clicked.connect(partial(self.udPage, -1))
        self.dnPage.clicked.connect(partial(self.udPage, 1))

        # 页码条跳转到第几页
        self.lineEditor_current.textModified.connect(self.textModified_connect)

    def itemNumber_clicked_connect(self, val):
        val = int(val)
        if val == self.pageItemNumber:
            return

        if val not in self.pageItemN:
            return

        # 设置当前选择的pageItem
        for each in self.itemNumber:
            each.setSelected(False)

        for each in self.itemNumber:
            if each.text() == str(val):
                self.pageItemNumber = val
                each.setSelected(True)
                break

        # 重新设置page
        self.pageMax = int(self.totalNumber / val)
        print (self.pageMax )
        self.__setSelected(self.label01, 1)
        # 发出修改信号
        self.itemChanged.emit(val)
        print(u'每页可以加载由{}改为{}条数据'.format(self.pageItemNumber, val))
        self.current_valueChanged_connect(1)

    def textModified_connect(self, index):
        """
        编辑窗口输出
        :param index:
        :return:
        """
        index = int(index)
        if self.pageMax < 9:
            self.__setSelected(self.numberPage[index - 1], index)
            self.current_valueChanged_connect(index)
            return

        if index >= 6:
            number = index if index < self.pageMax - 3 else self.pageMax - 3
            self.__setSelected(self.label05, number)

        if index <= self.pageMax - 5:
            number = index if index > 4 else 4
            self.__setSelected(self.label04, number)

        for each in self.numberPage:
            if each.text() == str(index):
                self.__setSelected(each, index)
                self.current_valueChanged_connect(index)
                return

    @QtCore.pyqtSlot(int)
    def current_valueChanged_connect(self, index):
        """

        :param index: 得到当前页码，并发射信号
        :return:
        """
        self.pageNumber = index
        print(u'第{}页，可以加载{}条数据'.format(index, self.pageItemNumber))
        self.valueChanged.emit(index, self.pageItemNumber)

    def udPage(self, val):
        """
        翻页
        :param val: 1：向后一页，-1向前一页
        :return:
        """
        currentSel = None
        currentIndex = -1
        for (i, each) in enumerate(self.numberPage):
            if each.isSelected:
                currentSel = each
                currentIndex = i
                break
        if currentSel == self.label01 and val == -1:
            return
        if currentSel == self.label08 and val == 1:
            return
        if int(currentSel.text()) == self.pageMax and val == 1:
            return

        currentIndex += val
        nextSel = self.numberPage[currentIndex]
        self.setSelected(nextSel, nextSel.text())
        pass

    def setSelected(self, sender, index):
        """

        :param sender: 页码控件
        :param index: 第几页
        :return:
        """
        index = int(index)
        # 如果是当前页的话，跳过
        if index == self.pageNumber:
            return

        # 如果选择到了 ... 的控件，不执行
        if sender.isLock:
            return

        if sender == self.label01:
            self.__setSelected(sender, 1)
            # 触发信号发射出去
            self.lineEditor_current.setText(1)
            self.current_valueChanged_connect(1)
            return

        # 触发信号发射出去
        self.lineEditor_current.setText(index)
        self.current_valueChanged_connect(index)

        if sender == self.label03:
            if index > 3:
                self.__setSelected(self.label04, index)
                return
        if sender == self.label06:
            if index < self.pageMax - 2:
                self.__setSelected(self.label05, index)
                return

        self.__setSelected(sender, index)

    def __setSelected(self, sender, index):
        """
        页码变更后的窗口修改
        :param sender:
        :param index:
        :return:
        """
        for each in self.numberPage:
            each.setSelected(0)

        sender.setSelected(1)
        sender.setText(index)
        # 变小
        if sender == self.label04:
            if index < self.pageMax - 4:
                self.label07.setLock(True)
            if index <= 4:
                self.label02.setLock(False)
                for (i, label) in enumerate(self.numberUpPage):
                    label.setText(index - 3 + i)
            else:
                self.label02.setLock(True)
                for (i, label) in enumerate(self.numberMdPage):
                    label.setText(index - 1 + i)
            return

        # 变大
        if sender == self.label05:
            if index > 5:
                self.label02.setLock(True)
            if index < self.pageMax - 3:
                self.label07.setLock(True)
                for (i, label) in enumerate(self.numberMdPage):
                    label.setText(index - 2 + i)
            elif index == self.pageMax:
                for (i, label) in enumerate(self.numberDnPage):
                    label.setText(self.pageMax - 2 + i)
            else:
                self.label07.setLock(False)
                for (i, label) in enumerate(self.numberDnPage):
                    label.setText(self.pageMax - 5 + i)

            return

        # 最开头
        if sender == self.label01:
            if self.pageMax > 8:
                self.label07.setLock(True)
            self.label02.setLock(False)
            for (i, label) in enumerate(self.numberUpPage):
                label.setText(index + i)
            return

        if sender == self.label08:
            if index > 8:
                self.label02.setLock(True)
            self.label07.setLock(False)
            for (i, label) in enumerate(self.numberDnPage):
                label.setText(self.pageMax - 5 + i)
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    ui = navigationpages()
    ui.totalNumber = 5000
    ui.show()
    app.exec_()
