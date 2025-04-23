### **Инструкция по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот блок кода содержит модуль `styles.py`, который предназначен для применения общих стилей к элементам пользовательского интерфейса (UI) в приложении, использующем библиотеку PyQt6. В частности, здесь реализована функция `set_fixed_size`, которая устанавливает фиксированный размер для виджета.

Шаги выполнения
-------------------------
1. **Импорт модуля QtWidgets**: Импортируется модуль `QtWidgets` из библиотеки PyQt6, который содержит классы для создания элементов интерфейса.
2. **Определение функции set_fixed_size**: Определяется функция `set_fixed_size`, которая принимает виджет (`widget`), ширину (`width`) и высоту (`height`) в качестве аргументов.
3. **Установка фиксированного размера**: Внутри функции вызывается метод `setFixedSize` виджета, чтобы установить его фиксированный размер на заданные значения ширины и высоты.

Пример использования
-------------------------

```python
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget
import sys
# from src.suppliers.suppliers_list.aliexpress.gui.styles import set_fixed_size  # Assuming styles.py is in the specified path

def set_fixed_size(widget: QtWidgets.QWidget, width: int, height: int):
    """ Set a fixed size for a given widget """
    widget.setFixedSize(width, height)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создание виджета (например, кнопки)
    button = QPushButton("Кнопка")

    # Применение фиксированного размера к кнопке
    set_fixed_size(button, 200, 50)  # Устанавливаем ширину 200 и высоту 50 пикселей

    # Отображение виджета
    button.show()

    sys.exit(app.exec())