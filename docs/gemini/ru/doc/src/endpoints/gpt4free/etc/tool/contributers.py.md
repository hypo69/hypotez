# Модуль `contributers.py`

## Обзор

Этот модуль предназначен для вывода списка участников проекта `gpt4free` на GitHub. 

## Подробнее

Модуль использует API GitHub для получения списка участников проекта. 
Он формирует HTML-код с ссылками на профили участников на GitHub, а также отображает аватарки участников. 

## Код

```python
                import requests

url = "https://api.github.com/repos/xtekky/gpt4free/contributors?per_page=100"

for user in requests.get(url).json():
    print(f'<a href="https://github.com/{user["login"]}" target="_blank"><img src="{user["avatar_url"]}&s=45" width="45" title="{user["login"]}"></a>')
                ```
                
## Как работает код:

1. **Импорт `requests`:**
    - Импортируется библиотека `requests` для отправки HTTP-запросов.

2. **Запрос к API GitHub:**
    - Определяется URL API GitHub для получения списка участников репозитория `gpt4free`.
    - Используется метод `requests.get` для отправки GET-запроса к API.
    - Полученный ответ в JSON-формате преобразуется в Python-список `users`.

3. **Итерация по участникам:**
    - Цикл `for` перебирает всех пользователей из списка `users`.
    - Для каждого пользователя `user`:
        - Формируется HTML-код с ссылкой на профиль пользователя на GitHub,  используя информацию из словаря `user`.
        - В HTML-код добавляется  аватарка пользователя.
        - Результат выводится на консоль.

## Примеры

**Пример вывода HTML-кода:**

```html
<a href="https://github.com/xtekky" target="_blank"><img src="https://avatars.githubusercontent.com/u/12345678?s=45" width="45" title="xtekky"></a>
```

**Пример вывода списка участников:**

```
<a href="https://github.com/user1" target="_blank"><img src="https://avatars.githubusercontent.com/u/12345678?s=45" width="45" title="user1"></a>
<a href="https://github.com/user2" target="_blank"><img src="https://avatars.githubusercontent.com/u/98765432?s=45" width="45" title="user2"></a>
<a href="https://github.com/user3" target="_blank"><img src="https://avatars.githubusercontent.com/u/34567890?s=45" width="45" title="user3"></a>
...