# Модуль FTP

## Обзор

Модуль `src.utils.ftp` предоставляет набор функций для взаимодействия с FTP-серверами. Он позволяет отправлять, получать и удалять файлы с FTP-сервера.

## Подробности

Этот модуль реализует базовые операции FTP, такие как отправка файлов, получение файлов и удаление файлов с FTP-сервера. Он использует библиотеку `ftplib` для работы с протоколом FTP. 

## Классы
### Нет классов

## Функции

### `write`

**Назначение**: Эта функция отправляет файл на FTP-сервер.

**Параметры**:

- `source_file_path` (str): Путь к файлу, который нужно отправить.
- `dest_dir` (str): Целевой каталог на FTP-сервере.
- `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

- `bool`: `True`, если файл успешно отправлен, иначе `False`.

**Исключения**:

- `Exception`: Возникает ошибка, если не удается подключиться к FTP-серверу или отправить файл.

**Пример**:

```python
>>> success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')
>>> print(success)
True
```

**Как работает функция**:

1. Устанавливает соединение с FTP-сервером, используя заданные настройки подключения.
2. Переходит к целевому каталогу на FTP-сервере.
3. Открывает файл и отправляет его на FTP-сервер с использованием команды `STOR`.
4. Закрывает соединение с FTP-сервером.

**Дополнительные сведения**:

- Конфигурация соединения хранится в переменной `_connection`, которая должна быть определена в другом месте.
- Логгирование ошибок осуществляется с использованием модуля `logger` из `src.logger.logger`.


### `read`

**Назначение**: Эта функция получает файл с FTP-сервера.

**Параметры**:

- `source_file_path` (str): Путь, по которому файл будет сохранен локально.
- `dest_dir` (str): Каталог на FTP-сервере, где находится файл.
- `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

- `Union[str, bytes, None]`: Содержимое файла, если оно успешно получено, иначе `None`.

**Исключения**:

- `Exception`: Возникает ошибка, если не удается подключиться к FTP-серверу или получить файл.

**Пример**:

```python
>>> content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')
>>> print(content)
b'Some file content'
```

**Как работает функция**:

1. Устанавливает соединение с FTP-сервером, используя заданные настройки подключения.
2. Переходит к целевому каталогу на FTP-сервере.
3. Получает файл с FTP-сервера с использованием команды `RETR`.
4. Сохраняет файл локально.
5. Возвращает содержимое файла.
6. Закрывает соединение с FTP-сервером.

**Дополнительные сведения**:

- Логгирование ошибок осуществляется с использованием модуля `logger` из `src.logger.logger`.

### `delete`

**Назначение**: Эта функция удаляет файл с FTP-сервера.

**Параметры**:

- `source_file_path` (str): Путь, по которому файл находится локально (не используется).
- `dest_dir` (str): Каталог на FTP-сервере, где находится файл.
- `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

- `bool`: `True`, если файл успешно удален, иначе `False`.

**Исключения**:

- `Exception`: Возникает ошибка, если не удается подключиться к FTP-серверу или удалить файл.

**Пример**:

```python
>>> success = delete('local_path/to/file.txt', '/remote/directory', 'file.txt')
>>> print(success)
True
```

**Как работает функция**:

1. Устанавливает соединение с FTP-сервером, используя заданные настройки подключения.
2. Переходит к целевому каталогу на FTP-сервере.
3. Удаляет файл с FTP-сервера с использованием команды `DELETE`.
4. Закрывает соединение с FTP-сервером.

**Дополнительные сведения**:

- Логгирование ошибок осуществляется с использованием модуля `logger` из `src.logger.logger`.

## Параметры
### `_connection`

- `_connection` (dict): Хранит настройки подключения к FTP-серверу.
    - `server` (str):  Адрес FTP-сервера.
    - `port` (int): Порт для подключения к FTP-серверу (по умолчанию 21).
    - `user` (str): Имя пользователя для доступа к FTP-серверу.
    - `password` (str): Пароль для доступа к FTP-серверу. 
    - Этот словарь должен быть определен в другом месте.
    
## Примеры
### Пример: отправка файла

```python
from src.utils.ftp import write

# Предполагается, что настройки подключения уже определены
# в переменной '_connection'

# Отправка файла 'local_path/to/file.txt' в каталог '/remote/directory'
# на FTP-сервере под именем 'file.txt'
success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')

if success:
    print('Файл успешно отправлен на FTP-сервер.')
else:
    print('Ошибка отправки файла на FTP-сервер.')
```

### Пример: получение файла

```python
from src.utils.ftp import read

# Предполагается, что настройки подключения уже определены
# в переменной '_connection'

# Получение файла 'file.txt' из каталога '/remote/directory'
# на FTP-сервере и сохранение его в файл 'local_path/to/file.txt'
content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')

if content:
    print('Файл успешно получен с FTP-сервера.')
else:
    print('Ошибка получения файла с FTP-сервера.')
```

### Пример: удаление файла

```python
from src.utils.ftp import delete

# Предполагается, что настройки подключения уже определены
# в переменной '_connection'

# Удаление файла 'file.txt' из каталога '/remote/directory'
# на FTP-сервере
success = delete('local_path/to/file.txt', '/remote/directory', 'file.txt')

if success:
    print('Файл успешно удален с FTP-сервера.')
else:
    print('Ошибка удаления файла с FTP-сервера.')
```