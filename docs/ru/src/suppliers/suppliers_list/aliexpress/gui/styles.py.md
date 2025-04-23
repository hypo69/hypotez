# Модуль стилей для элементов GUI AliExpress

## Обзор

Модуль `styles.py` содержит общие функции для стилизации элементов пользовательского интерфейса (UI) в GUI AliExpress. В частности, он предоставляет функцию для установки фиксированного размера виджетов.

## Подробнее

Этот модуль предоставляет удобные инструменты для стандартизации внешнего вида элементов интерфейса, что способствует единообразию и улучшению пользовательского опыта. Функция `set_fixed_size` позволяет легко задавать фиксированные размеры для виджетов, что полезно для поддержания консистентности в различных частях приложения.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `set_fixed_size`

```python
def set_fixed_size(widget: QtWidgets.QWidget, width: int, height: int):
    """ Set a fixed size for a given widget """
    widget.setFixedSize(width, height)
```

**Назначение**: Устанавливает фиксированный размер для заданного виджета.

**Параметры**:
- `widget` (QtWidgets.QWidget): Виджет, для которого необходимо установить фиксированный размер.
- `width` (int): Ширина виджета.
- `height` (int): Высота виджета.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Как работает функция**:
Функция `set_fixed_size` принимает виджет `widget` и устанавливает его фиксированные размеры, используя методы `setFixedSize`. Это гарантирует, что виджет не будет изменять свой размер в зависимости от содержимого или изменений в макете.

**Примеры**:

```python
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
import sys

# Пример использования в приложении PyQt6
app = QApplication(sys.argv)
window = QWidget()
button = QPushButton("Кнопка", window)
set_fixed_size(button, 100, 50)  # Устанавливаем фиксированный размер кнопки: 100x50 пикселей
window.show()
sys.exit(app.exec())
```
```python
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
import sys

# Пример использования в приложении PyQt6
app = QApplication(sys.argv)
window = QWidget()
label = QLabel("Метка", window)
set_fixed_size(label, 150, 30)  # Устанавливаем фиксированный размер метки: 150x30 пикселей
window.show()
sys.exit(app.exec())