### **Анализ кода модуля `utils.py`**

#### **Качество кода**:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет полезную функцию - извлекает куки из различных браузеров.
    - Использование `browser_cookie3` упрощает получение куки.
- **Минусы**:
    - Отсутствует документация модуля и функций.
    - Обработка исключений `Exception as e` слишком общая, что затрудняет отладку.
    - Не используется логирование ошибок.
    - Не указаны типы для переменных.
    - Не используется `logger` из модуля `src.logger`.
    - Не обрабатывается исключение `KeyError` при поиске куки по имени.

#### **Рекомендации по улучшению**:

1.  **Добавить документацию модуля**:
    - Описать назначение модуля и предоставить примеры использования.
2.  **Добавить документацию для класса `Utils`**:
    - Описать назначение класса и его атрибуты.
3.  **Добавить документацию для функции `get_cookies`**:
    - Описать параметры, возвращаемые значения и возможные исключения.
4.  **Указывать более конкретные типы исключений**:
    - Вместо `Exception as e` использовать конкретные типы исключений, такие как `browser_cookie3.BrowserError` или `KeyError`.
5.  **Использовать логирование**:
    - Замените `print` на `logger.error` для регистрации ошибок.
6.  **Обрабатывать `KeyError`**:
    - Вместо выхода из программы при отсутствии куки, можно возвращать `None` или пустой словарь.
7.  **Добавить аннотации типов**:
    - Укажите типы для всех переменных и параметров функций.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с куками браузеров
========================================

Модуль содержит класс :class:`Utils`, который используется для извлечения куки из различных браузеров.

Пример использования
----------------------

>>> utils = Utils()
>>> cookies = utils.get_cookies(domain='example.com')
>>> print(cookies)
{'cookie_name': 'cookie_value'}
"""
import browser_cookie3
from typing import Dict, Optional, List
from src.logger import logger


class Utils:
    """
    Класс для работы с куками браузеров.
    Содержит методы для извлечения куки из различных браузеров.
    """

    browsers = [
        browser_cookie3.chrome,  # 62.74% market share
        browser_cookie3.safari,  # 24.12% market share
        browser_cookie3.firefox,  # 4.56% market share
        browser_cookie3.edge,  # 2.85% market share
        browser_cookie3.opera,  # 1.69% market share
        browser_cookie3.brave,  # 0.96% market share
        browser_cookie3.opera_gx,  # 0.64% market share
        browser_cookie3.vivaldi,  # 0.32% market share
    ]

    def get_cookies(self, domain: str, setName: Optional[str] = None, setBrowser: Optional[str] = None) -> Dict[str, str]:
        """
        Извлекает куки из указанного домена из различных браузеров.

        Args:
            domain (str): Домен, для которого нужно извлечь куки.
            setName (Optional[str], optional): Имя конкретной куки, которую нужно извлечь. По умолчанию `None`.
            setBrowser (Optional[str], optional): Имя браузера, из которого нужно извлечь куки. По умолчанию `None`.

        Returns:
            Dict[str, str]: Словарь с куками, где ключ - имя куки, значение - значение куки.
                           Возвращает пустой словарь, если куки не найдены.

        Raises:
            browser_cookie3.BrowserError: Если возникает ошибка при доступе к кукам браузера.
            KeyError: Если не найдена кука с указанным именем.

        Example:
            >>> utils = Utils()
            >>> cookies = utils.get_cookies(domain='example.com')
            >>> print(cookies)
            {'cookie_name': 'cookie_value'}
        """
        cookies: Dict[str, str] = {}

        if setBrowser:
            for browser in Utils.browsers:
                if browser.__name__ == setBrowser:
                    try:
                        for c in browser(domain_name=domain):
                            if c.name not in cookies:
                                cookies[c.name] = c.value

                    except browser_cookie3.BrowserError as ex:
                        logger.error(f'Error while getting cookies from {browser.__name__}', ex, exc_info=True)

        else:
            for browser in Utils.browsers:
                try:
                    for c in browser(domain_name=domain):
                        if c.name not in cookies:
                            cookies[c.name] = c.value

                except browser_cookie3.BrowserError as ex:
                    logger.error(f'Error while getting cookies from {browser.__name__}', ex, exc_info=True)

        if setName:
            try:
                return {setName: cookies[setName]}

            except KeyError as ex:
                logger.error(f'Error: could not find {setName} cookie in any browser.', ex, exc_info=True)
                return {}

        else:
            return cookies