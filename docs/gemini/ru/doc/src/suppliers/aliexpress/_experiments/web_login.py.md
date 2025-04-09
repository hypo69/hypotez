# Модуль `web_login.py`

## Обзор

Модуль `web_login.py` предназначен для автоматизации процесса логина на сайт Aliexpress и сохранения cookies. Это экспериментальный скрипт, используемый для проверки и отладки процесса авторизации и получения cookies для дальнейшей работы с сайтом.

## Подробней

Этот файл содержит код для автоматического входа на сайт Aliexpress с использованием веб-драйвера. Он использует класс `Supplier` из модуля `src.suppliers` и веб-драйвер, чтобы открыть страницу логина, выполнить вход и сохранить cookies для последующего использования.

## Импортированные модули

- `header`: Импортирует модуль `header`.
- `pathlib.Path`: Используется для работы с путями к файлам и директориям.
- `pickle`: Используется для сериализации и десериализации объектов Python (в данном случае, для сохранения и загрузки cookies).
- `requests`: Используется для выполнения HTTP-запросов.
- `src.gs`: Импортирует модуль `gs` из пакета `src`.
- `src.suppliers.Supplier`: Импортирует класс `Supplier` из модуля `src.suppliers`.
- `src.utils.printer.pprint`: Импортирует функцию `pprint` из модуля `src.utils.printer` для удобной печати.

## Переменные

- `a`: Экземпляр класса `Supplier` с именем `'aliexpress'`. Используется для взаимодействия с Aliexpress.
- `d`: Драйвер, полученный из экземпляра класса `Supplier`. Используется для управления браузером.

## Классы

В данном коде классы отсутствуют.

## Функции

В данном коде функции отсутствуют.

## Пример использования

```python
import header
from pathlib import Path
import pickle
import requests

from src import gs
from src.suppliers import Supplier
from src.utils.printer import pprint

a = Supplier('aliexpress') # Создание экземпляра класса Supplier для Aliexpress
d = a.driver # Получение драйвера из экземпляра Supplier
d.get_url('https://aliexpress.com') # Открытие страницы Aliexpress в браузере