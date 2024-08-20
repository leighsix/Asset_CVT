import sys
import os
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
from editasset import EditAssetWindow


class ViewAssetsWindow(QtWidgets.QDialog):
    """저장된 자산을 보여주는 창"""
    def __init__(self, parent):
        super(ViewAssetsWindow, self).__init__(parent)
        self.setWindowTitle("자산 현황")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #ffffff;")
        self.initUI()

    def initUI(self):
        """UI 구성"""
        layout = QVBoxLayout()

        # 자산 테이블 초기화
        self.assets_table = QTableWidget(self)
        self.assets_table.setColumnCount(6)
        self.assets_table.setHorizontalHeaderLabels(["자산", "중요성", "민감도", "복구 가능성", "공격 가능성", "감시 가능성"])
        self.assets_table.horizontalHeader().setStretchLastSection(True)
        self.assets_table.setAlternatingRowColors(True)
        self.assets_table.setStyleSheet("QTableWidget {background-color: #f9f9f9;}")

        self.load_assets()  # 자산 로드

        # 수정 버튼 초기화
        self.edit_button = QPushButton("수정", self)
        self.edit_button.setStyleSheet("background-color: #0078D4; color: white; border-radius: 5px; padding: 10px;")
        self.edit_button.clicked.connect(self.edit_asset)

        # 종료 버튼 초기화
        self.exit_button = QPushButton("종료", self)
        self.exit_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 10px;")
        self.exit_button.clicked.connect(self.close)

        layout.addWidget(self.assets_table)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

    def load_assets(self):
        """데이터베이스에서 자산 정보를 로드하여 테이블에 표시"""
        self.parent().cursor.execute('SELECT * FROM assets ORDER BY name')
        results = self.parent().cursor.fetchall()
        self.assets_table.setRowCount(0)  # 기존 데이터 초기화
        for row in results:
            self.assets_table.insertRow(self.assets_table.rowCount())
            for i in range(1, 7):
                self.assets_table.setItem(self.assets_table.rowCount() - 1, i - 1, QTableWidgetItem(str(row[i])))

    def edit_asset(self):
        """선택된 자산을 수정하기 위한 창 열기"""
        selected_row = self.assets_table.currentRow()
        if selected_row >= 0:
            asset_id = self.parent().cursor.execute('SELECT id FROM assets ORDER BY name').fetchall()[selected_row][0]
            self.edit_window = EditAssetWindow(self, asset_id)
            self.edit_window.exec_()
            self.load_assets()  # 수정 후 자산 목록 새로 고침
        else:
            QMessageBox.warning(self, "선택 오류", "수정할 자산을 선택하세요.")

