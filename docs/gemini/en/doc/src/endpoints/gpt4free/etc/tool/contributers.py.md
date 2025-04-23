# Документация для `contributers.py`

## Обзор

Этот скрипт предназначен для получения списка контрибьюторов репозитория `xtekky/gpt4free` с использованием API GitHub и отображения их аватарок со ссылками на профили GitHub.

## Более подробно

Скрипт запрашивает информацию о контрибьюторах репозитория `xtekky/gpt4free` с помощью API GitHub. Для каждого контрибьютора извлекается логин и URL аватарки, после чего формируется HTML-код для отображения аватарки со ссылкой на профиль GitHub. Этот код выводится в консоль.

## Функции

### Запрос и вывод контрибьюторов

```python
import requests

url = "https://api.github.com/repos/xtekky/gpt4free/contributors?per_page=100"

for user in requests.get(url).json():
    print(f'<a href="https://github.com/{user["login"]}" target="_blank"><img src="{user["avatar_url"]}&s=45" width="45" title="{user["login"]}"></a>')
```

**Назначение**:
Получает список контрибьюторов репозитория `xtekky/gpt4free` и выводит HTML-код для отображения их аватарок со ссылками на профили GitHub.

**Как работает функция**:
1. Импортируется библиотека `requests` для выполнения HTTP-запросов.
2. Определяется URL для запроса списка контрибьюторов из API GitHub.
3. Выполняется GET-запрос к API GitHub и получается JSON-ответ.
4. Для каждого пользователя в JSON-ответе извлекается логин (`user["login"]`) и URL аватарки (`user["avatar_url"]`).
5. Формируется HTML-код для отображения аватарки пользователя со ссылкой на его профиль GitHub.
6. HTML-код выводится в консоль.

**Пример**:

```python
import requests

url = "https://api.github.com/repos/xtekky/gpt4free/contributors?per_page=100"

for user in requests.get(url).json():
    print(f'<a href="https://github.com/{user["login"]}" target="_blank"><img src="{user["avatar_url"]}&s=45" width="45" title="{user["login"]}"></a>')
```

В результате выполнения этого кода в консоль будет выведен HTML-код для отображения аватарок контрибьюторов репозитория `xtekky/gpt4free`.