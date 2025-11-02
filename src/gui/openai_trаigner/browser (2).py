## \file /src/gui/openai_trаigner/browser (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.gui.openai_trаigner 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.gui.openai_trаigner """


import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

class FramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Убираем рамки окна
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Создаём виджет для отображения HTML
        self.browser = QWebEngineView()
        self.browser.setUrl("https://www.chatgpt.com")

        # Верхняя панель с кнопками
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("background-color: #333;")

        self.minimize_button = QPushButton("Свернуть в трей", self.title_bar)
        self.minimize_button.clicked.connect(self.hide_to_tray)

        self.fullscreen_button = QPushButton("Открыть на весь экран", self.title_bar)
        self.fullscreen_button.clicked.connect(self.showFullScreen)

        self.close_button = QPushButton("Закрыть", self.title_bar)
        self.close_button.clicked.connect(self.close)

        # Layout для кнопок в верхней панели
        title_bar_layout = QHBoxLayout(self.title_bar)
        title_bar_layout.addWidget(self.minimize_button)
        title_bar_layout.addWidget(self.fullscreen_button)
        title_bar_layout.addWidget(self.close_button)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Основной layout окна
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.browser)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Центральный виджет и установка layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Установка размеры окна
        self.resize(800, 600)

        # Системный трей
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))

        # Контекстное меню для иконки в трее
        tray_menu = QMenu()
        restore_action = QAction("Восстановить", self)
        restore_action.triggered.connect(self.showNormal)
        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self.quit_app)

        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)

        # Установка меню для иконки в трее
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    # Метод для минимизации окна в трей
    def hide_to_tray(self):
        self.hide()

    # Метод для закрытия приложения
    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    # Метод для перемещения окна мышью
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Чтобы приложение оставалось в трее

    window = FramelessWindow()
    window.show()

    sys.exit(app.exec())
