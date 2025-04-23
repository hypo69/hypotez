### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет интерфейс для взаимодействия с FTP-серверами, позволяя отправлять, получать и удалять файлы.

Шаги выполнения
-------------------------
1. **Установка соединения с FTP-сервером**:
   - Функция `ftplib.FTP()` устанавливает соединение с FTP-сервером, используя параметры сервера, пользователя и пароля из словаря `_connection`.
   - Функция `session.cwd(dest_dir)` переходит в указанный каталог на FTP-сервере.
2. **Отправка файла на FTP-сервер (write)**:
   - Функция `write(source_file_path, dest_dir, dest_file_name)` отправляет файл с локального пути `source_file_path` в каталог `dest_dir` на FTP-сервере под именем `dest_file_name`.
   - Файл открывается в бинарном режиме для чтения (`'rb'`).
   - Функция `session.storbinary()` отправляет файл на сервер.
3. **Получение файла с FTP-сервера (read)**:
   - Функция `read(source_file_path, dest_dir, dest_file_name)` получает файл из каталога `dest_dir` на FTP-сервере с именем `dest_file_name` и сохраняет его локально по пути `source_file_path`.
   - Файл создается и открывается в бинарном режиме для записи (`'wb'`).
   - Функция `session.retrbinary()` получает файл с сервера и записывает его в локальный файл.
   - Функция `f.read()` возвращает содержимое файла.
4. **Удаление файла с FTP-сервера (delete)**:
   - Функция `delete(source_file_path, dest_dir, dest_file_name)` удаляет файл с именем `dest_file_name` из каталога `dest_dir` на FTP-сервере.
   - Функция `session.delete()` удаляет файл с сервера.
5. **Закрытие соединения с FTP-сервером**:
   - Функция `session.quit()` закрывает соединение с FTP-сервером.
6. **Обработка исключений**:
   - Блоки `try...except` используются для обработки возможных ошибок при подключении к серверу, передаче, получении или удалении файлов, а также при закрытии соединения.
   - В случае ошибки, информация об ошибке логируется с использованием `logger.error()`.

Пример использования
-------------------------

```python
from src.utils.ftp import write, read, delete

# Пример отправки файла
source_file = 'local_path/to/example.txt'
destination_directory = '/remote/directory'
destination_file = 'example.txt'
success = write(source_file, destination_directory, destination_file)
if success:
    print('Файл успешно отправлен на FTP-сервер.')
else:
    print('Не удалось отправить файл на FTP-сервер.')

# Пример получения файла
local_file = 'local_path/to/downloaded.txt'
content = read(local_file, destination_directory, destination_file)
if content:
    print('Файл успешно получен с FTP-сервера.')
    #  print(f'Содержимое файла: {content.decode("utf-8")}')  # Раскомментируйте для просмотра содержимого
else:
    print('Не удалось получить файл с FTP-сервера.')

# Пример удаления файла
success = delete(source_file, destination_directory, destination_file)
if success:
    print('Файл успешно удален с FTP-сервера.')
else:
    print('Не удалось удалить файл с FTP-сервера.')