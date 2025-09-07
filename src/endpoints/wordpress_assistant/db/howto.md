# PyMySQL для WordPress - Быстрый старт

## Установка

```bash
pip install PyMySQL
```

## Быстрый пример использования

```python
from src.database.wordpress_pymysql import WordPressDB, WordPressConfig

# Создание конфигурации
config = WordPressConfig(
    host='localhost',
    database='wordpress',
    username='wp_user',
    password='your_password'
)

# Подключение и работа
wp_db = WordPressDB(config)
if wp_db.connect():
    posts = wp_db.get_posts(limit=5)
    print(f'Найдено постов: {len(posts)}')
    wp_db.close()
```

## Основные методы класса WordPressDB

### Подключение
- `connect()` - подключение к базе данных
- `is_connected()` - проверка соединения
- `reconnect()` - переподключение
- `close()` - закрытие соединения

### Работа с постами
- `get_posts(limit=10, post_type='post', post_status='publish')` - получение постов
- `get_post_by_id(post_id)` - получение поста по ID
- `get_post_meta(post_id, meta_key=None)` - метаданные поста
- `get_posts_with_meta(limit=10)` - посты с метаданными

### Работа с пользователями
- `get_users(limit=10)` - получение пользователей

### Работа с комментариями  
- `get_comments(post_id=None, limit=10)` - получение комментариев

### Работа с настройками
- `get_options()` - все настройки WordPress
- `get_option(option_name)` - конкретная настройка

### Выполнение запросов
- `execute_query(query, params=None)` - выполнение произвольного запроса
- `execute_single_query(query, params=None)` - получение одного результата

## Загрузка конфигурации

### Из wp-config.php
```python
from src.database.wordpress_pymysql import load_config_from_wp_config

config = load_config_from_wp_config('/path/to/wordpress/wp-config.php')
```

### Сохранение/загрузка в JSON
```python
from src.database.wordpress_pymysql import create_wp_config, load_wp_config

# Сохранение
create_wp_config(config, 'config/wordpress.json')

# Загрузка
config = load_wp_config('config/wordpress.json')
```

## Примеры полезных запросов

### Получение постов с авторами
```python
query = '''
SELECT 
    p.ID,
    p.post_title,
    p.post_date,
    u.display_name as author_name
FROM wp_posts p
JOIN wp_users u ON p.post_author = u.ID
WHERE p.post_status = 'publish'
ORDER BY p.post_date DESC
LIMIT %s
'''

posts_with_authors = wp_db.execute_query(query, (10,))
```

### Поиск постов по ключевым словам
```python
query = '''
SELECT ID, post_title, post_content
FROM wp_posts 
WHERE post_status = 'publish' 
AND (post_title LIKE %s OR post_content LIKE %s)
LIMIT %s
'''

keyword = '%python%'
search_results = wp_db.execute_query(query, (keyword, keyword, 20))
```

### Статистика по постам
```python
query = '''
SELECT 
    post_status,
    COUNT(*) as count
FROM wp_posts 
WHERE post_type = 'post'
GROUP BY post_status
'''

stats = wp_db.execute_query(query)
```

## Обработка ошибок

Класс автоматически обрабатывает ошибки подключения и выполнения запросов:

- Логирует ошибки через ваш logger
- Автоматически переподключается при разрыве соединения
- Использует контекстные менеджеры для безопасной работы с курсорами
- Возвращает пустые списки/None при ошибках

## Настройки безопасности

### Создание пользователя для Python
```sql
-- Подключение к MySQL/MariaDB
CREATE USER 'wp_python'@'localhost' IDENTIFIED BY 'secure_password';

-- Права только на чтение (безопасно)
GRANT SELECT ON wordpress.* TO 'wp_python'@'localhost';

-- Или полные права (осторожно!)
GRANT ALL PRIVILEGES ON wordpress.* TO 'wp_python'@'localhost';

FLUSH PRIVILEGES;
```

### Переменные окружения
```python
import os

config = WordPressConfig(
    host=os.getenv('WP_DB_HOST', 'localhost'),
    database=os.getenv('WP_DB_NAME', 'wordpress'),
    username=os.getenv('WP_DB_USER'),
    password=os.getenv('WP_DB_PASSWORD')
)
```

## Преимущества PyMySQL

✅ **Простая установка** - чистый Python, без компиляции  
✅ **Легковесный** - минимальные зависимости  
✅ **Совместимость** - работает с MySQLdb API  
✅ **Unicode поддержка** - отличная работа с UTF-8  
✅ **Автореконнект** - встроенная поддержка переподключения  

## Лучшие практики

1. **Всегда закрывайте соединение** после работы
2. **Используйте параметризованные запросы** для безопасности
3. **Проверяйте результат подключения** перед выполнением запросов
4. **Логируйте операции** для отладки
5. **Используйте ограничения LIMIT** для больших таблиц