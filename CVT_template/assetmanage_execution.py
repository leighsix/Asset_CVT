import sys
import os
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
from assetmanager import AssetManager




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AssetManager()  # 자산 관리 프로그램의 메인 윈도우 생성
    window.show()  # 윈도우 표시
    sys.exit(app.exec_())  # 애플리케이션 실행
