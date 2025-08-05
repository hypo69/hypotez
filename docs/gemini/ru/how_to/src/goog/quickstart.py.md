## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой пример использования API Apps Script для создания нового проекта скрипта, загрузки файла в проект и записи URL-адреса скрипта для пользователя. 

Шаги выполнения
-------------------------
1. **Аутентификация:**
    - Проверяет наличие токена доступа в файле `token.json`.
    - Если токена нет, запускает диалог аутентификации для получения разрешений от пользователя.
    - Сохраняет полученный токен в файл `token.json`.
2. **Создание проекта:**
    - Создает новый проект Apps Script с заголовком "My Script".
3. **Загрузка файлов:**
    - Загружает два файла в проект:
        - `hello.js` с кодом функции `helloWorld()`.
        - `appsscript.json` с манифестом проекта.
4. **Печать URL-адреса:**
    - Выводит URL-адрес созданного проекта в консоль.

Пример использования
-------------------------

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Если изменять область действия, удалите файл token.json.
SCOPES = ['https://www.googleapis.com/auth/script.projects']

SAMPLE_CODE = '''
function helloWorld() {
  console.log("Hello, world!");
}
'''.strip()

SAMPLE_MANIFEST = '''
{
  "timeZone": "America/New_York",
  "exceptionLogging": "CLOUD"
}
'''.strip()

def main():
    """Вызывает API Apps Script."""
    creds = None
    # Файл token.json хранит токены доступа и обновления пользователя, и 
    # создается автоматически, когда поток авторизации завершается в первый раз.
    token_path = 'token.json'
    if Path(token_path).exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # Если доступных (действительных) учетных данных нет, разрешите пользователю войти в систему.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохраните учетные данные для следующего запуска
        with Path('token.json').open('w') as token:
            token.write(creds.to_json())

    try:
        service = build('script', 'v1', credentials=creds)

        # Вызов API Apps Script
        # Создание нового проекта
        request = {'title': 'My Script'}
        response = service.projects().create(body=request).execute()

        # Загрузка двух файлов в проект
        request = {
            'files': [
                {
                    'name': 'hello',
                    'type': 'SERVER_JS',
                    'source': SAMPLE_CODE
                },
                {
                    'name': 'appsscript',
                    'type': 'JSON',
                    'source': SAMPLE_MANIFEST
                }
            ]
        }
        response = service.projects().updateContent(
            body=request,
            scriptId=response['scriptId']).execute()
        print('https://script.google.com/d/' + response['scriptId'] + '/edit')
    except HttpError as error:
        # Произошла ошибка в API.
        print(error.content)

if __name__ == '__main__':
    main()
```

**Объяснение кода**:
-  Этот код использует API Google Apps Script для создания нового проекта скрипта, загрузки файла в проект и вывода URL-адреса скрипта для пользователя. 
-  Сначала код проверяет наличие токена доступа в файле `token.json`, если его нет, он запускает процесс аутентификации для получения разрешений от пользователя.
-  Затем код создает новый проект Apps Script с заголовком "My Script" и загружает в него два файла: `hello.js` с кодом функции `helloWorld()` и `appsscript.json` с манифестом проекта.
-  Наконец, код выводит URL-адрес созданного проекта в консоль.