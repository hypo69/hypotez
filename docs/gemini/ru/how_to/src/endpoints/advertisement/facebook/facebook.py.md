## Как использовать класс `Facebook`
=========================================================================================

### Описание
-------------------------
Класс `Facebook` предоставляет интерфейс для взаимодействия с Facebook через веб-драйвер. 
Он позволяет выполнять различные действия, такие как вход в аккаунт, отправка сообщений, загрузка медиафайлов, продвижение постов и событий.

### Шаги выполнения
-------------------------
1. **Инициализация объекта `Facebook`**: 
    - Создайте экземпляр класса `Facebook`, передав в конструктор веб-драйвер `driver`, имя промоутера `promoter` и список путей к файлам `group_file_paths`.
2. **Вход в аккаунт**: 
    - Вызовите метод `login()`, чтобы войти в аккаунт Facebook. Метод возвращает `True` в случае успешного входа, иначе `False`.
3. **Продвижение постов**:
    - Вызовите метод `promote_post(item)`, чтобы продвинуть пост. Передайте в метод объект `item` с данными о посте.
4. **Продвижение событий**: 
    - Вызовите метод `promote_event(event)`, чтобы продвинуть событие. Передайте в метод объект `event` с данными о событии.
    - Вместо этого вы можете использовать другие методы, которые предоставляются классом `Facebook`, например, `upload_media`, `post_title` и т.д.

### Пример использования
-------------------------

```python
from src.endpoints.advertisement.facebook.facebook import Facebook
from src.webdirver import Chrome

# Инициализируем объект Facebook
driver = Chrome()
facebook = Facebook(driver, "promoter_name", ["path/to/group_file1.json", "path/to/group_file2.json"])

# Входим в аккаунт
if facebook.login():
    print("Успешный вход в аккаунт Facebook")

# Продвигаем пост
item = {"title": "Post title", "message": "Post message"}
if facebook.promote_post(item):
    print("Пост успешно продвинут")

# Продвигаем событие
event = {"title": "Event title", "description": "Event description"}
facebook.promote_event(event)

# Закрываем драйвер
driver.close()

```