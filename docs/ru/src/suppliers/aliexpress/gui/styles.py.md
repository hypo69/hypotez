# Модуль стилей для графического интерфейса AliExpress
## Обзор

Модуль `styles.py` содержит общие функции для стилизации элементов пользовательского интерфейса (UI) в графическом интерфейсе AliExpress. Он предоставляет инструменты для установки фиксированных размеров виджетов, что способствует созданию единообразного и предсказуемого интерфейса.

## Подробней

Модуль предоставляет функцию `set_fixed_size`, которая позволяет задавать фиксированные размеры для виджетов PyQt6. Это полезно для обеспечения консистентности размеров элементов интерфейса и предотвращения их автоматического изменения в зависимости от содержимого или макета.

## Функции

### `set_fixed_size`

```python
def set_fixed_size(widget: QtWidgets.QWidget, width: int, height: int):
    """ Set a fixed size for a given widget """
    widget.setFixedSize(width, height)
```

**Назначение**:
Устанавливает фиксированный размер для заданного виджета.

**Параметры**:
- `widget` (QtWidgets.QWidget): Виджет, для которого необходимо установить фиксированный размер.
- `width` (int): Ширина виджета в пикселях.
- `height` (int): Высота виджета в пикселях.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Вызывает исключения**:
- Отсутствуют.

**Как работает функция**:
Функция `set_fixed_size` принимает виджет `widget` и устанавливает для него фиксированные значения ширины `width` и высоты `height` с помощью метода `setFixedSize` класса `QtWidgets.QWidget`. Это гарантирует, что виджет не будет изменять свой размер автоматически.

**Примеры**:
```python
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
import sys
from src.suppliers.aliexpress.gui.styles import set_fixed_size
# Пример использования функции set_fixed_size
app = QApplication(sys.argv)
window = QWidget()
button = QPushButton("Кнопка", window)
set_fixed_size(button, 100, 50)  # Устанавливаем фиксированный размер кнопки: ширина 100, высота 50
window.show()
app.exec()
```
В этом примере создается кнопка и устанавливается ее фиксированный размер 100x50 пикселей.

```python
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
import sys
from src.suppliers.aliexpress.gui.styles import set_fixed_size

app = QApplication(sys.argv)
window = QWidget()
label = QLabel("Текст", window)
set_fixed_size(label, 200, 30)  # Устанавливаем фиксированный размер метки: ширина 200, высота 30
window.show()
app.exec()
```
В этом примере создается метка и устанавливается ее фиксированный размер 200x30 пикселей.