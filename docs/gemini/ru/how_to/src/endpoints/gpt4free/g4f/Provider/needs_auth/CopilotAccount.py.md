## Как использовать CopilotAccount
=========================================================================================

Описание
-------------------------
`CopilotAccount`  -  класс, реализующий аутентификацию пользователя для использования модели Copilot.  

Шаги выполнения
-------------------------
1. **Инициализация класса**:  `CopilotAccount`  является наследником `AsyncAuthedProvider` и `Copilot`. Он  использует  `Copilot`  для работы с моделью Copilot. 
2. **Авторизация**: Метод  `on_auth_async`  отвечает за авторизацию пользователя. Он пытается получить токены доступа и куки из файла HAR,  созданного ранее. 
3. **Обработка ошибок**:  Если файл HAR не найден или недействителен,  `on_auth_async`  проверяет,  доступен ли `nodriver`. Если доступен, то  пользователю будет предложен  вход в  систему.  В противном случае будет выброшено исключение `NoValidHarFileError`.
4. **Получение токенов**: Если  `nodriver`  доступен, то  `on_auth_async`  использует  `get_access_token_and_cookies`  для получения токенов доступа и куки с помощью браузера.
5. **Создание объекта**: Метод  `create_authed`  создает аутентифицированный объект Copilot и начинает процесс обработки запроса. 
6. **Сохранение данных**:  `create_authed`  сохраняет  токены доступа и куки, полученные при аутентификации.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.CopilotAccount import CopilotAccount

# Инициализация объекта CopilotAccount
account = CopilotAccount()

# Авторизация пользователя
async for result in account.on_auth_async():
    if isinstance(result, RequestLogin):
        # Предложите пользователю войти в систему
        print("Пожалуйста, войдите в систему:")
        # Ожидайте ввода данных авторизации от пользователя
        # ...
    elif isinstance(result, AuthResult):
        # Авторизация успешна, получите токены доступа и куки
        access_token = result.api_key
        cookies = result.cookies

# Используйте полученные токены для работы с моделью Copilot
async for chunk in account.create_authed(model="Copilot", messages=["Привет!"]):
    print(chunk)

```