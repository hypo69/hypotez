# Модуль UserAgent
## Обзор

Модуль `useragent.py` предоставляет функцию для генерации случайного UserAgent. 

## Детали

Этот модуль используется для эмуляции различных браузеров при отправке запросов к веб-сайтам.  Это необходимо для предотвращения блокировки ботов и повышения анонимности при работе с API. 

## Функции

### `get_useragent()`

**Описание**: Функция для возврата случайного UserAgent из списка.

**Параметры**: 
-  -

**Возвращает**: 
-  `str`: Случайный UserAgent.

**Пример**:

```python
>>> get_useragent()
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
```

## Переменные

### `_useragent_list`

**Описание**: Список доступных UserAgent.

**Значение**:  
Список строк, каждая из которых представляет UserAgent определенного браузера.

```python
_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]
```