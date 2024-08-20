import sys
import os
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
from addasset import AddAssetWindow
from langselection import LanguageSelectionWindow
from editasset import EditAssetWindow
from cvtcalculation import CVTCalculationWindow
from viewasset import ViewAssetsWindow

class AssetManager(QtWidgets.QMainWindow):
    """자산 관리 프로그램의 메인 윈도우"""
    def __init__(self):
        super(AssetManager, self).__init__()

        # UI 파일 경로 설정
        ui_file_path = os.path.join(os.path.dirname(__file__), 'myapp.ui')

        # UI 파일이 존재하지 않으면 기본 UI 파일 생성
        if not os.path.exists(ui_file_path):
            self.create_default_ui_file(ui_file_path)

        uic.loadUi(ui_file_path, self)  # UI 파일 로드

        self.language = "ko"  # 기본 언어 설정
        self.language_button = QPushButton("언어 설정", self)  # 언어 설정 버튼 정의
        self.initUI()  # UI 초기화
        self.create_database()  # 데이터베이스 생성

    def create_default_ui_file(self, ui_file_path):
        """기본 UI 파일을 생성"""
        default_ui_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <ui version="4.0">
         <class>MainWindow</class>
         <widget class="QMainWindow" name="MainWindow">
          <widget class="QWidget" name="centralwidget">
           <widget class="QPushButton" name="add_asset_button">
            <property name="text">
             <string>자산 추가</string>
            </property>
           </widget>
           <widget class="QPushButton" name="view_assets_button">
            <property name="text">
             <string>자산 보기</string>
            </property>
           </widget>
           <widget class="QPushButton" name="calculate_cvt_button">
            <property name="text">
             <string>CVT 계산</string>
            </property>
           </widget>
           <widget class="QPushButton" name="exit_button">
            <property name="text">
             <string>종료</string>
            </property>
           </widget>
          </widget>
         </widget>
         <resources/>
         <connections/>
        </ui>
        '''
        # UI 파일 생성
        with open(ui_file_path, 'w', encoding='utf-8') as ui_file:
            ui_file.write(default_ui_content)
        print(f"기본 UI 파일이 생성되었습니다: {ui_file_path}")

    def set_language(self, lang):
        """선택한 언어를 설정하고 UI를 업데이트"""
        self.language = lang
        self.update_ui_language()

    def update_ui_language(self):
        """UI의 언어를 업데이트"""
        if self.language == "ko":
            self.add_asset_button.setText("자산 추가")
            self.view_assets_button.setText("자산 보기")
            self.calculate_cvt_button.setText("CVT 계산")
            self.exit_button.setText("종료")
            self.language_button.setText("언어 설정")
        elif self.language == "en":
            self.add_asset_button.setText("Add Asset")
            self.view_assets_button.setText("View Assets")
            self.calculate_cvt_button.setText("Calculate CVT")
            self.exit_button.setText("Exit")
            self.language_button.setText("Language Settings")
        elif self.language == "ar":
            self.add_asset_button.setText("إضافة أصل")
            self.view_assets_button.setText("عرض الأصول")
            self.calculate_cvt_button.setText("حساب CVT")
            self.exit_button.setText("خروج")
            self.language_button.setText("إعدادات اللغة")

        # UI 업데이트 후 연결된 기능 재설정
        self.initUI()

    def initUI(self):
        """UI 구성 및 버튼 초기화"""
        self.setWindowTitle("자산 관리 프로그램")
        self.setMinimumSize(800, 600)  # 최소 크기 설정
        self.setStyleSheet("background-color: #f0f0f0;")  # 배경 색상 설정

        # 버튼 스타일
        button_style = "background-color: #0078D4; color: white; font-size: 16px; border-radius: 5px; padding: 10px;"
        self.add_asset_button.setStyleSheet(button_style)
        self.view_assets_button.setStyleSheet(button_style)
        self.calculate_cvt_button.setStyleSheet(button_style)
        self.exit_button.setStyleSheet(button_style)

        # 언어 설정 버튼 스타일
        self.language_button.setStyleSheet("background-color: #6A6A6A; color: white; font-size: 16px; border-radius: 5px; padding: 10px;")
        self.language_button.clicked.connect(self.open_language_selection)  # 언어 선택 창 열기

        # 버튼 클릭 이벤트 연결
        self.add_asset_button.clicked.connect(self.open_add_asset_window)
        self.view_assets_button.clicked.connect(self.open_view_assets_window)
        self.calculate_cvt_button.clicked.connect(self.open_cvt_calculation_window)
        self.exit_button.clicked.connect(self.close)

        # 레이아웃에 버튼 추가
        layout = QVBoxLayout(self.centralwidget)  # 중앙 위젯에 레이아웃 추가
        layout.addWidget(self.add_asset_button)
        layout.addWidget(self.view_assets_button)
        layout.addWidget(self.calculate_cvt_button)
        layout.addWidget(self.exit_button)

        # 언어 버튼을 오른쪽 상단에 배치
        self.language_button.setGeometry(QtCore.QRect(self.width() - 150, 10, 140, 30))
        self.language_button.setParent(self)  # 부모를 설정하여 위치 조정

        # 레이아웃에 언어 버튼 추가
        layout.addWidget(self.language_button)

    def open_language_selection(self):
        """언어 선택 창 열기"""
        self.language_selection_window = LanguageSelectionWindow(self)
        self.language_selection_window.exec_()

    def create_database(self):
        """SQLite 데이터베이스 생성 및 테이블 설정"""
        self.conn = sqlite3.connect('assets.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                importance INTEGER,
                vulnerability_sensitivity INTEGER,
                vulnerability_recovery INTEGER,
                threat_attack INTEGER,
                threat_monitoring INTEGER
            )
        ''')
        self.conn.commit()

    def open_add_asset_window(self):
        """자산 추가 창 열기"""
        self.add_asset_window = AddAssetWindow(self)
        self.add_asset_window.show()

    def open_view_assets_window(self):
        """자산 보기 창 열기"""
        self.view_assets_window = ViewAssetsWindow(self)
        self.view_assets_window.show()

    def open_cvt_calculation_window(self):
        """CVT 계산 창 열기"""
        self.cvt_calculation_window = CVTCalculationWindow(self)
        self.cvt_calculation_window.show()

    def closeEvent(self, event):
        """창 닫기 이벤트 처리 - 데이터베이스 연결 종료"""
        self.conn.close()  # 데이터베이스 연결 종료

