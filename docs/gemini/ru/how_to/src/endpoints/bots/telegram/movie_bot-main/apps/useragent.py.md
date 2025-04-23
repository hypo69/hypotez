Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет функциональность для случайного выбора User-Agent из списка. User-Agent используется для идентификации браузера и операционной системы пользователя при отправке HTTP-запросов. Это полезно для имитации запросов от разных браузеров и операционных систем, что может быть необходимо для обхода ограничений или сбора данных с веб-сайтов.

Шаги выполнения
-------------------------
1. **Определение списка User-Agent**: В коде определен список `_useragent_list`, содержащий различные User-Agent строки.
2. **Функция выбора User-Agent**: Функция `get_useragent()` использует модуль `random` для случайного выбора одного User-Agent из списка `_useragent_list` и возвращает его.

Пример использования
-------------------------

```python
                import random

def get_useragent():
    return random.choice(_useragent_list)


_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]

# Пример использования
user_agent = get_useragent()
print(f"Случайный User-Agent: {user_agent}")
```
```output
Случайный User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36