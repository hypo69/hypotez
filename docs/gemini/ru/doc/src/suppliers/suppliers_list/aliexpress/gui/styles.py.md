# Модуль `src.suppliers.aliexpress.gui.styles`

## Обзор

Модуль `src.suppliers.aliexpress.gui.styles` предоставляет функции для настройки стилей элементов пользовательского интерфейса (UI) в приложении для работы с поставщиками AliExpress. 

## Подробнее

Этот модуль содержит набор функций, которые помогают  установить  фиксированный размер для элементов UI, созданных с использованием библиотеки PyQt6. Эти стили используются для  обеспечения  консистентности и удобства использования интерфейса.

## Функции

### `set_fixed_size`

**Назначение**: Установка фиксированного размера для виджета.

**Параметры**:

- `widget` (QtWidgets.QWidget): Виджет, для которого нужно установить размер.
- `width` (int): Ширина виджета в пикселях.
- `height` (int): Высота виджета в пикселях.

**Возвращает**:

- `None`

**Пример**:

```python
from PyQt6 import QtWidgets
from src.suppliers.aliexpress.gui.styles import set_fixed_size

# Создание виджета
widget = QtWidgets.QLabel("Пример виджета")

# Установка фиксированного размера
set_fixed_size(widget, 200, 50)
```

**Как работает функция**:

Функция `set_fixed_size`  использует метод `setFixedSize` из класса `QtWidgets.QWidget`, который устанавливает фиксированный размер для заданного виджета.  Метод `setFixedSize`  принимает два аргумента: ширину и высоту в пикселях.

**Примеры**:

```python
# Пример 1: Установка размера виджета
from PyQt6 import QtWidgets
from src.suppliers.aliexpress.gui.styles import set_fixed_size

widget = QtWidgets.QPushButton("Кнопка")
set_fixed_size(widget, 100, 30)  # Установка размера кнопки

# Пример 2:  Изменение размера виджета
widget = QtWidgets.QLabel("Текст")
set_fixed_size(widget, 150, 40)  # Изменение размера метки
```