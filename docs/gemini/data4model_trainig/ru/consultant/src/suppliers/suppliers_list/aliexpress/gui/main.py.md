### **Анализ кода модуля `main.py`**

## \file /src/suppliers/suppliers_list/aliexpress/gui/main.py

Модуль предоставляет основной интерфейс графического приложения для управления рекламными кампаниями на AliExpress.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован, используются классы для организации интерфейса.
  - Применение `QTabWidget` для разделения функциональности по вкладкам.
  - Наличие базовой обработки исключений при загрузке файлов.
- **Минусы**:
  - Отсутствует подробная документация классов и методов.
  - Смешаны стили комментариев (где-то `#`, где-то docstrings, где-то ничего).
  - Нет логирования ошибок.
  - Не используются аннотации типов.
  - Не все строки в коде соответствуют PEP8 (например, импорты).
  - Не используется `j_loads` для чтения JSON файлов.

**Рекомендации по улучшению:**

1.  **Добавить Docstring и комментарии**:
    *   Дополнить docstring для всех классов и методов, включая описание параметров, возвращаемых значений и возможных исключений.
    *   Перевести существующие docstring на русский язык.
    *   Комментарии должны быть на русском языке и соответствовать стандарту оформления.

2.  **Логирование**:
    *   Добавить логирование всех ошибок с использованием `logger.error` из модуля `src.logger`.

3.  **Использовать `j_loads`**:
    *   Заменить стандартное `open` и `json.load` на `j_loads` для чтения JSON файлов.

4.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных и параметров функций.

5.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках обработки исключений.

6.  **Улучшить стиль кода**:
    *   Следовать стандарту PEP8 для форматирования кода (пробелы вокруг операторов, порядок импортов и т.д.).
    *   Использовать одинарные кавычки для строк.

7.  **Обработка файлов**:
    *   Улучшить обработку ошибок при работе с файлами, добавить проверку существования файлов.

**Оптимизированный код:**

```python
## \file /src/suppliers/suppliers_list/aliexpress/gui/main.py
# -*- coding: utf-8 -*-\n
#! .pyenv/bin/python3

"""
Модуль для создания основного окна интерфейса для управления рекламными кампаниями.
==============================================================================

Модуль содержит класс :class:`MainApp`, который является основным окном приложения
и включает в себя вкладки для редактирования JSON, управления кампаниями и редактирования продуктов.

Пример использования
----------------------

>>> app = QtWidgets.QApplication(sys.argv)
>>> main_app = MainApp()
>>> main_app.show()
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from PyQt6 import QtWidgets, QtGui, QtCore
from qasync import QEventLoop

from src.logger import logger  # Импортируем logger
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress.gui.campaign import CampaignEditor
from src.suppliers.suppliers_list.aliexpress.gui.category import CategoryEditor
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor
from src.utils.jjson import j_loads_ns, j_dumps
from styles import set_fixed_size


class MainApp(QtWidgets.QMainWindow):
    """
    Основное окно приложения с вкладками для JSON Editor, Campaign Editor и Product Editor.
    """

    def __init__(self) -> None:
        """
        Инициализирует основное окно приложения с вкладками.
        """
        super().__init__()
        self.setWindowTitle('Main Application with Tabs')
        self.setGeometry(100, 100, 1800, 800)

        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Создаем вкладку JSON Editor и добавляем ее в tab_widget
        self.tab1 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab1, 'JSON Editor')
        self.promotion_app = CampaignEditor(self.tab1, self)

        # Создаем вкладку Campaign Editor и добавляем ее в tab_widget
        self.tab2 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab2, 'Campaign Editor')
        self.campaign_editor_app = CategoryEditor(self.tab2, self)

        # Создаем вкладку Product Editor и добавляем ее в tab_widget
        self.tab3 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab3, 'Product Editor')
        self.product_editor_app = ProductEditor(self.tab3, self)

        self.create_menubar()

    def create_menubar(self) -> None:
        """
        Создает меню с опциями для операций с файлами и командами редактирования.
        """
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        open_action = QtGui.QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        save_action = QtGui.QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        exit_action = QtGui.QAction('Exit', self)
        exit_action.triggered.connect(self.exit_application)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('Edit')
        copy_action = QtGui.QAction('Copy', self)
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        paste_action = QtGui.QAction('Paste', self)
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)

        open_product_action = QtGui.QAction('Open Product File', self)
        open_product_action.triggered.connect(self.product_editor_app.open_file)
        file_menu.addAction(open_product_action)

    def open_file(self) -> None:
        """
        Открывает диалоговое окно для выбора и загрузки JSON файла.
        """
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File', '', 'JSON files (*.json)')
        if not file_path:
            return

        if self.tab_widget.currentIndex() == 0:
            self.load_file(file_path)

    def save_file(self) -> None:
        """
        Сохраняет текущий файл в зависимости от активной вкладки.
        """
        current_index = self.tab_widget.currentIndex()
        if current_index == 0:
            self.promotion_app.save_changes()
        elif current_index == 2:
            self.product_editor_app.save_product()

    def exit_application(self) -> None:
        """
        Завершает работу приложения.
        """
        self.close()

    def copy(self) -> None:
        """
        Копирует выделенный текст в буфер обмена.
        """
        widget = self.focusWidget()
        if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
            widget.copy()
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'No text widget in focus to copy.')

    def paste(self) -> None:
        """
        Вставляет текст из буфера обмена.
        """
        widget = self.focusWidget()
        if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
            widget.paste()
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'No text widget in focus to paste.')

    def load_file(self, campaign_file: str) -> None:
        """
        Загружает JSON файл.
        Args:
            campaign_file (str): Путь к файлу кампании.
        """
        try:
            self.promotion_app.load_file(campaign_file)
        except Exception as ex:
            logger.error('Failed to load JSON file', ex, exc_info=True)  # Логируем ошибку
            QtWidgets.QMessageBox.critical(self, 'Error', f'Failed to load JSON file: {ex}')


def main() -> None:
    """
    Инициализирует и запускает приложение.
    """
    app = QtWidgets.QApplication(sys.argv)

    # Создаем event loop для асинхронных операций
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_app = MainApp()
    main_app.show()

    # Запускаем event loop
    with loop:
        loop.run_forever()


if __name__ == '__main__':
    main()