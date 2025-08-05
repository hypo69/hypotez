## Как использовать класс `GoogleDriveHandler`
=========================================================================================

### Описание
-------------------------
Класс `GoogleDriveHandler` обеспечивает взаимодействие с Google Drive. Он позволяет загружать файлы в определенную папку на Google Drive.

### Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создайте экземпляр класса `GoogleDriveHandler`, передав имя целевой папки в качестве аргумента.
    - Класс инициализирует аутентификацию с Google Drive, используя `google_auth_oauthlib` и `googleapiclient.discovery` для получения учетных данных и создания сервисного объекта.
2. **Загрузка файла**:
    - Вызовите метод `upload_file` с путем к файлу в качестве аргумента.
    - Метод `upload_file` (который пока не реализован) должен реализовать логику загрузки файла в указанную папку на Google Drive, используя сервисный объект Google Drive API.

### Пример использования
-------------------------

```python
    from pathlib import Path
    
    file_path = Path('/mnt/data/google_extracted/sample_file.txt')  # Замените на ваш фактический путь к файлу
    folder_name = 'My Drive Folder'  # Замените на имя целевой папки в Google Drive

    google_drive_handler = GoogleDriveHandler(
        folder_name=folder_name,
    )
    google_drive_handler.upload_file(file_path)
```

### Дополнительная информация
-------------------------
- Пример кода в документации демонстрирует основные шаги по использованию класса.
- Метод `upload_file` пока не реализован, вам нужно добавить логику загрузки файла в указанную папку на Google Drive.
- Класс `GoogleDriveHandler` использует `pickle` для сохранения и извлечения учетных данных в файл `token.pickle`.
- Для работы с Google Drive API требуется ключ API, который необходимо получить на [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
- Проект `hypotez` должен иметь необходимые права доступа для работы с Google Drive API.