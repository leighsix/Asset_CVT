import sys
import os
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np


class AddAssetWindow(QtWidgets.QDialog):
    """자산 추가를 위한 다이얼로그 창"""
    def __init__(self, parent):
        super(AddAssetWindow, self).__init__(parent)
        self.setWindowTitle("자산 추가")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #ffffff;")
        self.initUI()

    def initUI(self):
        """UI 구성"""
        layout = QFormLayout()

        # 입력 필드 초기화
        self.asset_input = QLineEdit(self)
        self.importance_input = QLineEdit(self)
        self.vulnerability_sensitivity_input = QLineEdit(self)
        self.vulnerability_recovery_input = QLineEdit(self)
        self.threat_attack_input = QLineEdit(self)
        self.threat_monitoring_input = QLineEdit(self)

        # 입력 필드 레이아웃 추가
        layout.addRow(QLabel("자산 이름:"), self.asset_input)
        layout.addRow(QLabel("중요성:"), self.importance_input)
        layout.addRow(QLabel("취약성(민감도):"), self.vulnerability_sensitivity_input)
        layout.addRow(QLabel("취약성(복구 가능성):"), self.vulnerability_recovery_input)
        layout.addRow(QLabel("위협(공격 가능성):"), self.threat_attack_input)
        layout.addRow(QLabel("위협(감시 가능성):"), self.threat_monitoring_input)

        # 저장 버튼 초기화
        self.save_button = QPushButton("저장", self)
        self.save_button.setStyleSheet("background-color: #0078D4; color: white; border-radius: 5px; padding: 10px;")
        self.save_button.clicked.connect(self.save_data)

        layout.addRow(self.save_button)
        self.setLayout(layout)

    def save_data(self):
        """자산 정보를 데이터베이스에 저장"""
        name = self.asset_input.text()
        importance = self.importance_input.text()
        vulnerability_sensitivity = self.vulnerability_sensitivity_input.text()
        vulnerability_recovery = self.vulnerability_recovery_input.text()
        threat_attack = self.threat_attack_input.text()
        threat_monitoring = self.threat_monitoring_input.text()

        # 입력값 유효성 검사
        if name and importance.isdigit() and vulnerability_sensitivity.isdigit() and vulnerability_recovery.isdigit() and threat_attack.isdigit() and threat_monitoring.isdigit():
            self.parent().cursor.execute('''
                INSERT INTO assets (name, importance, vulnerability_sensitivity, vulnerability_recovery, threat_attack, threat_monitoring)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, int(importance), int(vulnerability_sensitivity), int(vulnerability_recovery), int(threat_attack), int(threat_monitoring)))
            self.parent().conn.commit()
            QMessageBox.information(self, "Success", "Asset added successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid asset information.")