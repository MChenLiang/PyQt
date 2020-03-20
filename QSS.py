#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2020/2/25 18:43
# @Email    : spirit_az@foxmail.com
# @Name     : QSS.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
project_style_sheet = """
QComboBox {
    border: none;
    border-radius: 6px;
	font: 20px "Microsoft Yahei";
	background-color: rgba(0, 0, 0, 0);
 }

QComboBox::drop-down {
	border:none;
}
"""

project_style_sheet_w = """
QComboBox {
    border: 2px solid #aaa;
    border-radius: 6px;
	font: 20px "Microsoft Yahei";
	background-color: rgba(0, 0, 0, 0);
 }

QComboBox::drop-down {
	border:none;
}
"""

page_selected = """
QLabel{
    border: 1px solid #aaa;
    border-radius: 4px;
	font: 15px "Microsoft Yahei";

 }
"""

page_noSelected = """
QLabel{
    border: none;
	font: 12px "Microsoft Yahei";
 }

QLabel::drop-down {
	border:none;
}

QLabel::hover{
    border: 1px solid #aaa;
    border-radius: 4px;
	font: 15px "Microsoft Yahei";

 }

QLabel::pressed{
    border: none;
	font: 12px "Microsoft Yahei";

 }

"""

page_lock = """
QLabel{
    border: none;
	font: 12px "Microsoft Yahei";
 }
"""

page_lineEdit = """
QLineEdit{
    background:transparent;
    border-width: 0;
    font: 12px "Microsoft Yahei";
    border-style:outset}
"""