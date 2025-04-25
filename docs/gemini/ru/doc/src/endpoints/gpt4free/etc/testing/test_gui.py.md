# Модуль для запуска графического интерфейса 
## Обзор

Этот файл запускает графический интерфейс для приложения `hypotez`.

## Подробнее

Данный файл импортирует функцию `run_gui` из модуля `g4f.gui`, которая запускает графический интерфейс приложения. 

## Функции

### `run_gui`

**Назначение**:  Функция запускает графический интерфейс приложения `hypotez`.
**Параметры**:  
- `None`
**Возвращает**: 
- `None`
**Вызывает исключения**: 
- `None`
**Примеры**:
```python
from g4f.gui import run_gui

run_gui()
```
```python
                import sys\nfrom pathlib import Path\nsys.path.append(str(Path(__file__).parent.parent.parent))\n\nfrom g4f.gui import run_gui\nrun_gui()\n\n