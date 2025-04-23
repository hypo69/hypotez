### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код представляет собой виджет `ProductEditor` для редактирования информации о товаре, загружаемой из JSON файла. Он предоставляет пользовательский интерфейс (UI) для открытия JSON файла, отображения основных данных товара (например, заголовок и детали) и подготовки товара с использованием асинхронной операции.

Шаги выполнения
-------------------------
1. **Инициализация `ProductEditor`**:
   - Создается экземпляр класса `ProductEditor`, который является виджетом `QtWidgets.QWidget`.
   - В конструкторе инициализируется UI через метод `setup_ui()` и устанавливаются соединения между сигналами и слотами через метод `setup_connections()`.

2. **Настройка UI (`setup_ui`)**:
   - Устанавливается заголовок окна ("Product Editor") и размеры окна (1800x800).
   - Создаются кнопки "Open JSON File" и "Prepare Product", а также label для отображения имени выбранного файла.
   - Кнопка "Open JSON File" соединяется с методом `open_file()`, а кнопка "Prepare Product" соединяется с методом `prepare_product_async()`.
   - Все виджеты добавляются в вертикальный layout.

3. **Открытие файла (`open_file`)**:
   - При нажатии на кнопку "Open JSON File" открывается диалоговое окно выбора файла.
   - Пользователь выбирает JSON файл. Если файл выбран, вызывается метод `load_file()` с путем к выбранному файлу.

4. **Загрузка файла (`load_file`)**:
   - Метод `load_file()` принимает путь к файлу.
   - Используется функция `j_loads_ns()` для загрузки JSON файла в объект `SimpleNamespace`, который сохраняется в атрибуте `self.data`.
   - Отображается имя файла в `file_name_label`.
   - Создается экземпляр класса `AliCampaignEditor` и вызывается метод `create_widgets()` для создания виджетов на основе загруженных данных.
   - В случае ошибки, отображается сообщение об ошибке.

5. **Создание виджетов (`create_widgets`)**:
   - Метод `create_widgets()` принимает данные (`data`) из загруженного JSON файла.
   - Удаляются все предыдущие виджеты, кроме кнопок "Open JSON File", "Prepare Product" и `file_name_label`.
   - Создаются label для отображения заголовка и деталей товара.
   - Добавление созданных label в layout.

6. **Подготовка продукта асинхронно (`prepare_product_async`)**:
   - Этот метод вызывается при нажатии на кнопку "Prepare Product".
   - Вызывает метод `prepare_product()` экземпляра `AliCampaignEditor` асинхронно.
   - В случае успеха, отображается сообщение об успехе. В случае ошибки - сообщение об ошибке.

Пример использования
-------------------------

```python
import sys
from PyQt6 import QtWidgets
from src.suppliers.suppliers_list.aliexpress.gui.product import ProductEditor

def main():
    app = QtWidgets.QApplication(sys.argv)
    editor = ProductEditor()
    editor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```
```python
## \file /src/suppliers/aliexpress/gui/product.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress.gui 
	:platform: Windows, Unix
	:synopsis:

"""




""" Window editor for products """



import header
import sys
from pathlib import Path
from types import SimpleNamespace
from PyQt6 import QtWidgets, QtGui, QtCore
from src.utils.jjson import j_loads_ns, j_dumps
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignEditor
from src.utils.qt import asyncSlot
from src.logger import logger

class ProductEditor(QtWidgets.QWidget):
    """
    Редактор продукта.

    Args:
        parent (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
        main_app (QtWidgets.QApplication, optional): Главное приложение. По умолчанию `None`.
    """
    data: SimpleNamespace = None
    language: str = 'EN'
    currency: str = 'USD'
    file_path: str = None
    editor: AliCampaignEditor = None

    def __init__(self, parent: QtWidgets.QWidget = None, main_app: QtWidgets.QApplication = None) -> None:
        """
        Инициализирует виджет `ProductEditor`.

        Args:
            parent (QtWidgets.QWidget, optional): Родительский виджет. По умолчанию `None`.
            main_app (QtWidgets.QApplication, optional): Главное приложение. По умолчанию `None`.
        """
        super().__init__(parent)
        self.main_app = main_app  # Функция сохраняет экземпляр MainApp

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self) -> None:
        """
        Настраивает пользовательский интерфейс.
        """
        self.setWindowTitle("Product Editor")
        self.resize(1800, 800)

        # Функция определяет компоненты UI
        self.open_button = QtWidgets.QPushButton("Open JSON File")
        self.open_button.clicked.connect(self.open_file)

        self.file_name_label = QtWidgets.QLabel("No file selected")
        
        self.prepare_button = QtWidgets.QPushButton("Prepare Product")
        self.prepare_button.clicked.connect(self.prepare_product_async)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.open_button)
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.prepare_button)

        self.setLayout(layout)

    def setup_connections(self) -> None:
        """
        Настраивает соединения сигнал-слот.
        """
        pass

    def open_file(self) -> None:
        """
        Открывает диалоговое окно для выбора и загрузки JSON-файла.
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "c:/user/documents/repos/hypotez/data/aliexpress/products",
            "JSON files (*.json)"
        )
        if not file_path:
            return  #  Если файл не выбран - выход

        self.load_file(file_path)

    def load_file(self, file_path: str) -> None:
        """
        Загружает JSON-файл.

        Args:
            file_path (str): Путь к JSON-файлу.

        Raises:
            Exception: Если не удается загрузить JSON-файл.
        """
        try:
            self.data = j_loads_ns(file_path)
            self.file_path = file_path
            self.file_name_label.setText(f"File: {self.file_path}")
            self.editor = AliCampaignEditor(file_path=file_path)
            self.create_widgets(self.data)
        except Exception as ex:
            logger.error(f"Не удалось загрузить JSON-файл: {ex}", ex, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load JSON file: {ex}")

    def create_widgets(self, data: SimpleNamespace) -> None:
        """
        Создает виджеты на основе данных, загруженных из JSON-файла.

        Args:
            data (SimpleNamespace): Данные продукта из JSON-файла.
        """
        layout = self.layout()

        # Функция удаляет предыдущие виджеты, кроме кнопки открытия файла и метки файла
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget not in [self.open_button, self.file_name_label, self.prepare_button]:
                widget.deleteLater()

        title_label = QtWidgets.QLabel(f"Product Title: {data.title}")
        layout.addWidget(title_label)

        # Дополнительные сведения о товаре
        product_details_label = QtWidgets.QLabel(f"Product Details: {data.details}")
        layout.addWidget(product_details_label)

    @asyncSlot()
    async def prepare_product_async(self) -> None:
        """
        Асинхронно подготавливает продукт.
        """
        if self.editor:
            try:
                await self.editor.prepare_product()
                QtWidgets.QMessageBox.information(self, "Success", "Product prepared successfully.")
            except Exception as ex:
                logger.error(f"Ошибка подготовки продукта: {ex}", ex, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to prepare product: {ex}")