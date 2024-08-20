import sys
import os
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
from pdfdialog import PDFDialog

class CVTCalculationWindow(QtWidgets.QDialog):
    """CVT 계산을 위한 다이얼로그 창"""
    def __init__(self, parent):
        super(CVTCalculationWindow, self).__init__(parent)
        self.setWindowTitle("자산 CVT 산출")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #ffffff;")
        self.initUI()

    def initUI(self):
        """UI 구성"""
        layout = QVBoxLayout()

        # 결과 테이블 초기화
        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels(["우선순위", "자산", "중요성", "취약성", "위협", "합계"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setStyleSheet("QTableWidget {background-color: #f9f9f9;}")

        # 계산 버튼 초기화
        self.calculate_button = QPushButton("CVT 계산", self)
        self.calculate_button.setStyleSheet("background-color: #0078D4; color: white; border-radius: 5px; padding: 10px;")
        self.calculate_button.clicked.connect(self.calculate_cvt)

        # 출력 버튼 초기화
        self.print_button = QPushButton("출력", self)
        self.print_button.setStyleSheet("background-color: #FF9800; color: white; border-radius: 5px; padding: 10px;")
        self.print_button.clicked.connect(self.print_data)

        # 종료 버튼 초기화
        self.exit_button = QPushButton("종료", self)
        self.exit_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 10px;")
        self.exit_button.clicked.connect(self.close)

        # 가중치 및 랭크 선택 라디오 버튼
        self.weighted_radio = QtWidgets.QRadioButton("가중치 적용", self)
        self.rank_radio = QtWidgets.QRadioButton("랭크", self)
        self.weighted_radio.setChecked(True)  # 기본값으로 가중치 적용 선택

        # 가중치 입력 필드 초기화
        self.weight_importance = QLineEdit(self)
        self.weight_importance.setPlaceholderText("중요성 가중치")
        self.weight_importance.setText("1")

        self.weight_vulnerability = QLineEdit(self)
        self.weight_vulnerability.setPlaceholderText("취약성 가중치")
        self.weight_vulnerability.setText("1")

        self.weight_threat = QLineEdit(self)
        self.weight_threat.setPlaceholderText("위협 가중치")
        self.weight_threat.setText("1")

        # 레이아웃에 위젯 추가
        layout.addWidget(self.weighted_radio)
        layout.addWidget(self.weight_importance)
        layout.addWidget(self.weight_vulnerability)
        layout.addWidget(self.weight_threat)
        layout.addWidget(self.rank_radio)
        layout.addWidget(self.results_table)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.print_button)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

    def calculate_cvt(self):
        """CVT 계산 수행"""
        self.parent().cursor.execute('SELECT * FROM assets')
        results = self.parent().cursor.fetchall()
        cvt_data = []

        for row in results:
            name = row[1]
            importance = row[2]
            vulnerability = row[3] + row[4]  # 취약성 = 민감도 + 복구 가능성
            threat = row[5] + row[6]  # 위협 = 공격 가능성 + 감시 가능성

            if self.weighted_radio.isChecked():
                # 가중치 적용 방식
                total = (importance * int(self.weight_importance.text()) +
                         vulnerability * int(self.weight_vulnerability.text()) +
                         threat * int(self.weight_threat.text()))
            else:
                # 랭크 방식
                rank_importance = len(results) - sorted([r[2] for r in results]).index(importance)
                rank_vulnerability = len(results) - sorted([r[3] + r[4] for r in results]).index(vulnerability)
                rank_threat = len(results) - sorted([r[5] + r[6] for r in results]).index(threat)

                std_importance = np.std([r[2] for r in results])
                std_vulnerability = np.std([r[3] + r[4] for r in results])
                std_threat = np.std([r[5] + r[6] for r in results])

                total = (rank_importance * std_importance +
                         rank_vulnerability * std_vulnerability +
                         rank_threat * std_threat)

            cvt_data.append((total, name, importance, vulnerability, threat))

        # 우선순위에 따라 정렬
        cvt_data.sort(reverse=True, key=lambda x: x[0])

        # 테이블에 결과 표시
        self.display_results(cvt_data)

    def display_results(self, cvt_data):
        """CVT 계산 결과를 테이블에 표시"""
        self.results_table.setRowCount(0)  # 기존 데이터 초기화
        for index, (total, name, importance, vulnerability, threat) in enumerate(cvt_data):
            self.results_table.insertRow(index)
            self.results_table.setItem(index, 0, QTableWidgetItem(str(index + 1)))  # 우선순위
            self.results_table.setItem(index, 1, QTableWidgetItem(name))  # 자산
            self.results_table.setItem(index, 2, QTableWidgetItem(str(importance)))  # 중요성
            self.results_table.setItem(index, 3, QTableWidgetItem(str(vulnerability)))  # 취약성
            self.results_table.setItem(index, 4, QTableWidgetItem(str(threat)))  # 위협
            self.results_table.setItem(index, 5, QTableWidgetItem(str(total)))  # 합계

    def print_data(self):
        """CVT 계산 결과를 PDF로 출력"""
        pdf_dialog = PDFDialog(self)
        pdf_dialog.exec_()
