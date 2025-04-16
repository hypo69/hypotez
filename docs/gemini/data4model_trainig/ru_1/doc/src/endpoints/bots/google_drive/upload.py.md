# Модуль для загрузки файлов в Google Drive
=================================================

Модуль предоставляет функциональность для загрузки файлов в Google Drive с использованием библиотеки `pydrive`.
Он включает в себя функции для аутентификации пользователя, создания папок (если они не существуют) и загрузки файлов в указанную папку.
Модуль поддерживает загрузку как в личный Google Drive, так и в Team Drive (если настроены соответствующие параметры).

## Обзор

Этот модуль предназначен для автоматизации процесса загрузки файлов в Google Drive. 
Он использует библиотеку `pydrive` для взаимодействия с Google Drive API. 
Модуль позволяет загружать файлы, создавать папки, если они не существуют, и устанавливать разрешения на файлы для общего доступа.

## Подробней

Модуль `upload.py` предоставляет функцию `upload`, которая загружает указанный файл в Google Drive. 
Перед загрузкой функция аутентифицирует пользователя, используя сохраненные учетные данные или запрашивая новые. 
Если указана родительская папка, функция проверяет, существует ли она в Google Drive, и создает ее, если она не существует.
Модуль поддерживает загрузку файлов как в личный Google Drive, так и в Team Drive, в зависимости от конфигурации.

## Функции

### `upload`

```python
def upload(filename: str, update, context, parent_folder: str = None) -> None:
    """Загружает файл в Google Drive.

    Args:
        filename (str): Полный путь к файлу, который нужно загрузить.
        update: Объект `update` от Telegram API, содержащий информацию о пользователе, отправившем запрос на загрузку.
        context: Контекст выполнения (используется для передачи дополнительных данных).
        parent_folder (str, optional): Название папки в Google Drive, в которую нужно загрузить файл. По умолчанию `None` (загрузка в корневую папку).

    Returns:
        str: `file_to_upload['webContentLink']` - Ссылка для скачивания файла из Google Drive.

    Raises:
        Exception: Если происходит ошибка при загрузке файла.

    **Как работает функция**:
    - Функция принимает имя файла, информацию об обновлении и контекст в качестве аргументов.
    - Инициализирует Google Drive API и аутентифицирует пользователя, используя сохраненные учетные данные.
    - Если учетные данные отсутствуют или устарели, функция обновляет их.
    - Если указана родительская папка, функция проверяет ее наличие в Google Drive и создает, если она не существует.
    - Загружает файл в Google Drive в указанную папку или в корневую папку, если родительская папка не указана.
    - Если загрузка происходит в личный Google Drive, функция устанавливает разрешение на чтение для всех пользователей, у которых есть ссылка.
    - Возвращает ссылку на загруженный файл.
    """

    FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
    drive: GoogleDrive
    http = None
    initial_folder = None
    gauth: drive.GoogleAuth = GoogleAuth()

    ID = update.message.from_user.id
    ID = str(ID)
    gauth.LoadCredentialsFile(
        path.join(path.dirname(path.abspath(__file__)), ID))

    if gauth.credentials is None:
        print("not Auth Users")
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
        gauth.SaveCredentialsFile(
            path.join(path.dirname(path.abspath(__file__)), ID))
    else:
        # Initialize the saved creds
        gauth.Authorize()
    drive = GoogleDrive(gauth)
    http = drive.auth.Get_Http_Object()
    if not path.exists(filename):
        print(f"Specified filename {filename} does not exist!")
        return

    if not Creds.TEAMDRIVE_FOLDER_ID:

        if parent_folder:

                # Check the files and folers in the root foled
                file_list = drive.ListFile(
                    {'q': "'root' in parents and trashed=false"}).GetList()
                for file_folder in file_list:
                    if file_folder['title'] == parent_folder:
                        # Get the matching folder id
                        folderid = file_folder['id']
                        print("Folder Already Exist  !!  Trying To Upload")
                        # We need to leave this if it's done
                        break
                else:
                    # Create folder
                    folder_metadata = {'title': parent_folder,
                                       'mimeType': 'application/vnd.google-apps.folder'}
                    folder = drive.CreateFile(folder_metadata)
                    folder.Upload()
                    folderid = folder['id']
                    # Get folder info and print to screen
                    foldertitle = folder['title']
                    # folderid = folder['id']
                    print('title: %s, id: %s' % (foldertitle, folderid))

    file_params = {'title': filename.split('/')[-1]}

    if Creds.TEAMDRIVE_FOLDER_ID:
        file_params['parents'] = [{"kind": "drive#fileLink", "teamDriveId": Creds.TEAMDRIVE_ID, "id": Creds.TEAMDRIVE_FOLDER_ID}]

    else:
        if parent_folder:
            file_params['parents'] = [{"kind": "drive#fileLink", "id": folderid}]

    file_to_upload = drive.CreateFile(file_params)
    file_to_upload.SetContentFile(filename)
    try:
        file_to_upload.Upload(param={"supportsTeamDrives": True, "http": http})


    except Exception as ex:
        print("upload", ex)
    if not Creds.TEAMDRIVE_FOLDER_ID:
        file_to_upload.FetchMetadata()
        file_to_upload.InsertPermission({
        'type':  'anyone', 'value': 'anyone', 'role':  'reader', 'withLink': True
    })

    return file_to_upload['webContentLink']
```
**Примеры**:

```python
filename = 'path/to/your/file.txt'
update = MockUpdateObject()  # Замените на реальный объект update из Telegram API
context = {}
parent_folder = 'MyFolder'

# Вызов функции upload
file_link = upload(filename, update, context, parent_folder)
print(f"File uploaded. Link: {file_link}")
```

## Переменные

- `FOLDER_MIME_TYPE` (str): MIME-тип для папок в Google Drive (`application/vnd.google-apps.folder`).
- `drive` (GoogleDrive): Объект GoogleDrive для взаимодействия с Google Drive API.
- `http`: Объект HTTP для выполнения запросов к Google Drive API.
- `initial_folder`: Исходная папка для загрузки файлов.