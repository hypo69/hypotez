### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код показывает базовое использование Apps Script API. Он вызывает Apps Script API для создания нового скриптового проекта, загружает файл в проект и выводит URL скрипта для пользователя.

Шаги выполнения
-------------------------
1. **Аутентификация и авторизация**:
   - Код пытается загрузить учетные данные пользователя из файла `token.json`.
   - Если файл не существует или учетные данные недействительны, выполняется процесс авторизации через `InstalledAppFlow`.
   - Полученные учетные данные сохраняются в файл `token.json` для последующего использования.

2. **Создание сервиса Apps Script API**:
   - После получения учетных данных создается экземпляр сервиса Apps Script API с использованием `build('script', 'v1', credentials=creds)`.

3. **Создание нового проекта**:
   - Выполняется запрос к API для создания нового скриптового проекта с названием "My Script".
   - Полученный ответ содержит `scriptId` нового проекта.

4. **Загрузка файлов в проект**:
   - Создается запрос для загрузки двух файлов в проект: `hello.js` с кодом `SAMPLE_CODE` и `appsscript.json` с манифестом `SAMPLE_MANIFEST`.
   - Выполняется запрос к API для обновления содержимого проекта с использованием `scriptId`.

5. **Вывод URL скрипта**:
   - Выводится URL созданного скрипта, который можно использовать для редактирования скрипта в Google Apps Script.

6. **Обработка ошибок**:
   - Если во время выполнения API возникают ошибки, они перехватываются и выводятся в консоль.

Пример использования
-------------------------

```python
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

import header
from src import gs

# If modifying these scopes, delete the file token.json.
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
    """Calls the Apps Script API."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = gs.path.secrets / 'e-cat-346312-137284f4419e.json'
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with Path('token.json').open('w') as token:
            token.write(creds.to_json())

    try:
        service = build('script', 'v1', credentials=creds)

        # Call the Apps Script API
        # Create a new project
        request = {'title': 'My Script'}
        response = service.projects().create(body=request).execute()

        # Upload two files to the project
        request = {
            'files': [{
                'name': 'hello',
                'type': 'SERVER_JS',
                'source': SAMPLE_CODE
            }, {
                'name': 'appsscript',
                'type': 'JSON',
                'source': SAMPLE_MANIFEST
            }]
        }
        response = service.projects().updateContent(
            body=request,
            scriptId=response['scriptId']).execute()
        print('https://script.google.com/d/' + response['scriptId'] + '/edit')
    except errors.HttpError as error:
        # The API encountered a problem.
        print(error.content)


if __name__ == '__main__':
    main()