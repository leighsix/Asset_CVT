import sys
import os
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np


class LanguageSelectionWindow(QtWidgets.QDialog):
    """언어 선택을 위한 다이얼로그 창"""
    def __init__(self, parent):
        super(LanguageSelectionWindow, self).__init__(parent)
        self.setWindowTitle("언어 선택")
        self.setMinimumSize(300, 200)
        self.initUI()

    def initUI(self):
        """UI 구성"""
        layout = QVBoxLayout()

        self.label = QLabel("언어를 선택하세요:", self)
        layout.addWidget(self.label)

        # 한국어 버튼
        self.korean_button = QPushButton("한국어", self)
        self.korean_button.clicked.connect(lambda: self.select_language("ko"))
        layout.addWidget(self.korean_button)

        # 영어 버튼
        self.english_button = QPushButton("English", self)
        self.english_button.clicked.connect(lambda: self.select_language("en"))
        layout.addWidget(self.english_button)

        # 아랍어 버튼
        self.arabic_button = QPushButton("العربية", self)
        self.arabic_button.clicked.connect(lambda: self.select_language("ar"))
        layout.addWidget(self.arabic_button)

        self.setLayout(layout)

    def select_language(self, lang):
        """선택한 언어를 설정하고 다이얼로그를 닫음"""
        self.parent().set_language(lang)
        self.close()

