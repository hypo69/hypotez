### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой главное окно приложения для управления рекламными кампаниями. Он включает в себя несколько вкладок для редактирования JSON, управления кампаниями и продуктами. Также предоставляет меню для работы с файлами и редактирования текста.

Шаги выполнения
-------------------------
1. **Инициализация приложения**:
   - Создается экземпляр класса `QtWidgets.QApplication`.
   - Устанавливается event loop для асинхронных операций с использованием `QEventLoop` и `asyncio`.

2. **Создание главного окна**:
   - Создается экземпляр класса `MainApp`, который является главным окном приложения.
   - Задается заголовок окна и его размеры.
   - Добавляются вкладки: "JSON Editor", "Campaign Editor" и "Product Editor".
   - Для каждой вкладки создаются соответствующие редакторы: `CampaignEditor`, `CategoryEditor` и `ProductEditor`.
   - Создается меню с опциями для работы с файлами и редактирования текста.

3. **Запуск приложения**:
   - Главное окно отображается с помощью `main_app.show()`.
   - Запускается event loop для обработки событий и асинхронных операций.

4. **Обработка действий пользователя**:
   - **Открытие файла**: При выборе "Open" в меню "File" открывается диалоговое окно для выбора JSON-файла. Выбранный файл загружается в редактор JSON.
   - **Сохранение файла**: При выборе "Save" в меню "File" изменения сохраняются в зависимости от активной вкладки.
   - **Выход из приложения**: При выборе "Exit" в меню "File" приложение закрывается.
   - **Копирование и вставка**: При выборе "Copy" или "Paste" в меню "Edit" текст копируется или вставляется из буфера обмена в активный текстовый виджет.

Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/gui/main.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress.gui
    :platform: Windows, Unix
    :synopsis:

"""


""" Main window interface for managing advertising campaigns """

import sys
import asyncio
from PyQt6 import QtWidgets, QtGui
from qasync import QEventLoop

from product import ProductEditor
from campaign import CampaignEditor
from category import CategoryEditor

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        """ Initialize the main application with tabs """
        super().__init__()
        self.setWindowTitle("Main Application with Tabs")
        self.setGeometry(100, 100, 1800, 800)

        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create the JSON Editor tab and add it to the tab widget
        self.tab1 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab1, "JSON Editor")
        self.promotion_app = CampaignEditor(self.tab1, self)

        # Create the Campaign Editor tab and add it to the tab widget
        self.tab2 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab2, "Campaign Editor")
        self.campaign_editor_app = CategoryEditor(self.tab2, self)

        # Create the Product Editor tab and add it to the tab widget
        self.tab3 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab3, "Product Editor")
        self.product_editor_app = ProductEditor(self.tab3, self)

        self.create_menubar()

    def create_menubar(self):
        """ Create a menu bar with options for file operations and edit commands """
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_action = QtGui.QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        save_action = QtGui.QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        exit_action = QtGui.QAction("Exit", self)
        exit_action.triggered.connect(self.exit_application)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")
        copy_action = QtGui.QAction("Copy", self)
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        paste_action = QtGui.QAction("Paste", self)
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)

        open_product_action = QtGui.QAction("Open Product File", self)
        open_product_action.triggered.connect(self.product_editor_app.open_file)
        file_menu.addAction(open_product_action)

    def open_file(self):
        """ Open a file dialog to select and load a JSON file """
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "JSON files (*.json)")
        if not file_path:
            return

        if self.tab_widget.currentIndex() == 0:
            self.load_file(file_path)

    def save_file(self):
        """ Save the current file """
        current_index = self.tab_widget.currentIndex()
        if current_index == 0:
            self.promotion_app.save_changes()
        elif current_index == 2:
            self.product_editor_app.save_product()

    def exit_application(self):
        """ Exit the application """
        self.close()

    def copy(self):
        """ Copy selected text to the clipboard """
        widget = self.focusWidget()
        if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
            widget.copy()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "No text widget in focus to copy.")

    def paste(self):
        """ Paste text from the clipboard """
        widget = self.focusWidget()
        if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
            widget.paste()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "No text widget in focus to paste.")

    def load_file(self, campaign_file):
        """ Load the JSON file """
        try:
            self.promotion_app.load_file(campaign_file)
        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")

def main():
    """ Initialize and run the application """
    app = QtWidgets.QApplication(sys.argv)

    # Create an event loop for asynchronous operations
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_app = MainApp()
    main_app.show()

    # Run the event loop
    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main()