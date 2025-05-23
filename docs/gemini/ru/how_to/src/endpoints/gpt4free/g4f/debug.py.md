## Как использовать модуль `debug`
=========================================================================================

Описание
-------------------------
Модуль `debug` предоставляет инструменты для ведения журнала событий и обработки ошибок во время работы программы.

Шаги выполнения
-------------------------
1. **Инициализация**: Перед использованием функций модуля необходимо задать переменные конфигурации:
    - `logging`: Управляет включением/отключением ведения журнала. Значение `True` включает ведение журнала.
    - `version_check`: Управляет включением/отключением проверки версии. Значение `True` включает проверку.
    - `version`: Строка, содержащая версию программы.
    - `log_handler`: Функция, которая будет использоваться для записи сообщений в журнал. По умолчанию используется функция `print`.
    - `logs`: Список, который будет хранить записанные сообщения.
2. **Запись сообщений**:
    - Вызов функции `log` с произвольным количеством аргументов записывает эти аргументы в журнал, если `logging` установлено в `True`. 
3. **Обработка ошибок**:
    - Вызов функции `error` с произвольным количеством аргументов записывает сообщение об ошибке в поток ошибок (stderr), если `logging` установлено в `True`.
    - Функция `error` преобразует нестроковые аргументы в строки, добавив информацию о типе ошибки (или заданное имя ошибки) и её значение.

Пример использования
-------------------------

```python
import sys
from hypotez.src.endpoints.gpt4free.g4f.debug import log, error, logging, version_check, version

# Включение ведения журнала
logging = True

# Запись сообщения в журнал
log("Это тестовое сообщение")

# Симуляция ошибки
try:
    1 / 0
except ZeroDivisionError as e:
    error(f"Деление на ноль!", e)

# Проверка версии (только если version_check = True)
if version_check:
    # Проверяем установленную версию
    if version is not None:
        log(f"Текущая версия: {version}")
    else:
        error("Ошибка: версия программы не задана!")

```