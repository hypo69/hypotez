### **Анализ кода модуля `date_time.py`**

## \file /src/utils/date_time.py

Модуль содержит класс `TimeoutCheck`, который предоставляет функциональность для проверки, находится ли текущее время в заданном интервале, с возможностью установки таймаута.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код выполняет поставленную задачу.
  - Есть пример использования в `if __name__ == '__main__':`.
  - Класс хорошо структурирован, с чётким разделением ответственности между методами.
  - Обработка интервалов, пересекающих полночь.
- **Минусы**:
  - Отсутствует логирование.
  - Docstring не соответствует требованиям оформления.
  - Не все переменные аннотированы.
  - В коде используются смешанные стили кавычек (как двойные, так и одинарные).
  - Отсутствуют проверки типов для входных параметров.
  - Не используется модуль `logger` для логгирования.
  - Текст docstring на английском языке.

**Рекомендации по улучшению:**

1. **Документирование**:
   - Перевести все комментарии и docstring на русский язык, соблюдая формат, указанный в инструкции.
   - Добавить примеры использования в docstring.
   - Описать все параметры и возвращаемые значения в docstring.
2. **Обработка исключений**:
   - Добавить обработку исключений в методах `interval`, `interval_with_timeout` и `input_with_timeout`.
   - Использовать `logger.error` для логирования ошибок.
3. **Типизация**:
   - Добавить аннотации типов для всех переменных, где это необходимо.
4. **Логирование**:
   - Добавить логирование в начале и конце методов, а также при возникновении таймаутов и ошибок.
5. **Форматирование**:
   - Использовать только одинарные кавычки для строк.
   - Добавить пробелы вокруг операторов присваивания.
6. **Проверки типов**:
   - Добавить проверки типов для входных параметров методов `interval`, `interval_with_timeout` и `input_with_timeout`.

**Оптимизированный код:**

```python
## \file /src/utils/date_time.py
# -*- coding: utf-8 -*-

"""
Модуль для работы с датой и временем
======================================

Модуль содержит класс :class:`TimeoutCheck`, который предоставляет функциональность для проверки,
находится ли текущее время в заданном интервале, с возможностью установки таймаута.

Пример использования
----------------------

>>> timeout_check = TimeoutCheck()
>>> if timeout_check.interval_with_timeout(timeout=5):
...     print('Текущее время находится в интервале.')
... else:
...     print('Текущее время вне интервала или произошел тайм-аут.')
"""

from datetime import datetime, time
import threading
from typing import Optional

from src.logger import logger  # Добавлен импорт logger


class TimeoutCheck:
    """
    Класс для проверки, находится ли текущее время в заданном интервале с таймаутом.
    """

    def __init__(self):
        """
        Инициализация класса TimeoutCheck.
        """
        self.result: Optional[bool] = None
        self.user_input: Optional[str] = None

    def interval(self, start: time = time(23, 0), end: time = time(6, 0)) -> bool:
        """
        Проверяет, находится ли текущее время в указанном интервале.

        Args:
            start (time, optional): Время начала интервала. По умолчанию 23:00.
            end (time, optional): Время окончания интервала. По умолчанию 06:00.

        Returns:
            bool: True, если текущее время находится в интервале, иначе False.

        Raises:
            TypeError: Если `start` или `end` не являются объектами `datetime.time`.

        Example:
            >>> timeout_check = TimeoutCheck()
            >>> timeout_check.interval(start=time(22, 0), end=time(7, 0))
            True
        """
        try:
            if not isinstance(start, time) or not isinstance(end, time):
                raise TypeError('`start` и `end` должны быть объектами `datetime.time`.')

            current_time: time = datetime.now().time()

            if start < end:
                # Интервал в пределах одного дня (например, с 08:00 до 17:00)
                self.result = start <= current_time <= end
            else:
                # Интервал, охватывающий полночь (например, с 23:00 до 06:00)
                self.result = current_time >= start or current_time <= end

            logger.info(f'Результат проверки интервала: {self.result}')  # Логирование результата
            return self.result
        except TypeError as ex:
            logger.error('Ошибка при проверке интервала', ex, exc_info=True)  # Логирование ошибки
            return False
        except Exception as ex:
            logger.error('Непредвиденная ошибка при проверке интервала', ex, exc_info=True)
            return False

    def interval_with_timeout(self, timeout: int = 5, start: time = time(23, 0), end: time = time(6, 0)) -> bool:
        """
        Проверяет, находится ли текущее время в указанном интервале с таймаутом.

        Args:
            timeout (int, optional): Время ожидания в секундах. По умолчанию 5.
            start (time, optional): Время начала интервала. По умолчанию 23:00.
            end (time, optional): Время окончания интервала. По умолчанию 06:00.

        Returns:
            bool: True, если текущее время находится в интервале и получен ответ в течение таймаута,
                  False, если нет или произошел таймаут.

        Raises:
            TypeError: Если `timeout` не является целым числом, или `start` или `end` не являются объектами `datetime.time`.

        Example:
            >>> timeout_check = TimeoutCheck()
            >>> timeout_check.interval_with_timeout(timeout=3, start=time(22, 0), end=time(7, 0))
            True
        """
        if not isinstance(timeout, int):
            raise TypeError('`timeout` должно быть целым числом.')
        if not isinstance(start, time) or not isinstance(end, time):
            raise TypeError('`start` и `end` должны быть объектами `datetime.time`.')
        logger.info(f'Запуск проверки интервала с таймаутом {timeout} секунд.')  # Логирование начала выполнения

        thread = threading.Thread(target=self.interval, args=(start, end))
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            logger.warning(f'Таймаут {timeout} секунд истек, продолжение выполнения.')  # Логирование таймаута
            thread.join()  # Обеспечивает остановку потока после таймаута
            return False  # Произошел таймаут, возвращаем False

        logger.info(f'Результат проверки интервала с таймаутом: {self.result}')  # Логирование результата
        return self.result

    def get_input(self):
        """
        Запрашивает ввод от пользователя.
        """
        self.user_input = input('U:> ')

    def input_with_timeout(self, timeout: int = 5) -> str | None:
        """
        Ожидает ввод с тайм-аутом.

        Args:
            timeout (int, optional): Время ожидания ввода в секундах. По умолчанию 5.

        Returns:
            str | None: Введенные данные или None, если был тайм-аут.

        Raises:
            TypeError: Если `timeout` не является целым числом.

        Example:
            >>> timeout_check = TimeoutCheck()
            >>> user_input = timeout_check.input_with_timeout(timeout=10)
            >>> if user_input:
            ...     print(f'Введено: {user_input}')
            ... else:
            ...     print('Тайм-аут ввода.')
        """
        if not isinstance(timeout, int):
            raise TypeError('`timeout` должно быть целым числом.')

        logger.info(f'Ожидание ввода от пользователя с таймаутом {timeout} секунд.')  # Логирование начала ожидания ввода

        # Запускаем поток для получения ввода от пользователя
        thread = threading.Thread(target=self.get_input)
        thread.start()

        # Ожидаем завершения потока или тайм-аут
        thread.join(timeout)

        if thread.is_alive():
            logger.warning(f'Таймаут {timeout} секунд истек.')  # Логирование таймаута
            return None  # Возвращаем None, если тайм-аут произошел

        logger.info(f'Введенные данные: {self.user_input}')  # Логирование введенных данных
        return self.user_input


if __name__ == '__main__':
    # Пример использования
    timeout_check = TimeoutCheck()

    # Проверка интервала с таймаутом 5 секунд
    if timeout_check.interval_with_timeout(timeout=5):
        print('Текущее время находится в интервале.')
    else:
        print('Текущее время вне интервала или произошел таймаут.')