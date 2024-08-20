import sys
import os
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np


class PDFDialog(QtWidgets.QDialog):
    """PDF 출력 다이얼로그 창"""
    def __init__(self, parent):
        super(PDFDialog, self).__init__(parent)
        self.setWindowTitle("PDF 출력")
        self.setMinimumSize(300, 200)
        self.setStyleSheet("background-color: #ffffff;")
        self.initUI()

    def initUI(self):
        """UI 구성"""
        layout = QVBoxLayout()

        self.file_name_input = QLineEdit(self)
        self.file_name_input.setPlaceholderText("파일 이름 입력 (예: output.pdf)")
        layout.addWidget(self.file_name_input)

        # PDF 저장 버튼 초기화
        self.save_button = QPushButton("PDF 저장", self)
        self.save_button.setStyleSheet("background-color: #0078D4; color: white; border-radius: 5px; padding: 10px;")
        self.save_button.clicked.connect(self.save_pdf)

        # 종료 버튼 초기화
        self.exit_button = QPushButton("종료", self)
        self.exit_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 10px;")
        self.exit_button.clicked.connect(self.close)

        layout.addWidget(self.save_button)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

    def save_pdf(self):
        """PDF 파일로 CVT 계산 결과 저장"""
        file_name = self.file_name_input.text()
        if not file_name.endswith('.pdf'):
            file_name += '.pdf'

        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        c.drawString(100, height - 100, "CVT Calculation Results")
        c.drawString(100, height - 120, "우선순위  자산  중요성  취약성  위협  합계")

        for row in range(self.parent().results_table.rowCount()):
            priority = self.parent().results_table.item(row, 0).text()
            asset = self.parent().results_table.item(row, 1).text()
            importance = self.parent().results_table.item(row, 2).text()
            vulnerability = self.parent().results_table.item(row, 3).text()
            threat = self.parent().results_table.item(row, 4).text()
            total = self.parent().results_table.item(row, 5).text()

            c.drawString(100, height - 140 - (row * 20), f"{priority}  {asset}  {importance}  {vulnerability}  {threat}  {total}")

        c.save()  # PDF 저장
        QMessageBox.information(self, "Success", f"PDF 파일이 '{file_name}'로 저장되었습니다.")
        self.close()

