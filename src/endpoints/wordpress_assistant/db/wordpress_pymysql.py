## \file src/database/wordpress_pymysql.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для подключения к базе данных WordPress с использованием PyMySQL.
====================================================================
Предоставляет простой и эффективный способ работы с базой данных WordPress
через PyMySQL драйвер.

```rst
.. module:: src.database.wordpress_pymysql
```
"""

import header
from header import __root__
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns, j_dumps
from src.utils.printer import pprint as print

from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import pymysql
from contextlib import contextmanager
from dataclasses import dataclass
import re


@dataclass
class WordPressConfig:
    """Конфигурация подключения к базе данных WordPress."""
    host: str = gs.credentials.wordpress.db.host
    port: int = gs.credentials.wordpress.db.port
    database: str = gs.credentials.wordpress.db.db_name
    username: str = gs.credentials.wordpress.db.db_user
    password: str = gs.credentials.wordpress.db.db_password
    charset: str = 'utf8mb4'
    table_prefix: str = 'wp_'


class WordPressDB:
    """Класс для работы с базой данных WordPress через PyMySQL."""
    
    def __init__(self, config: WordPressConfig):
        """
        Инициализация подключения к WordPress базе данных.
        
        Args:
            config (WordPressConfig): Конфигурация подключения к базе данных.
        """
        self.config: WordPressConfig = config
        self.connection = None
        self._connected: bool = False
    
    def connect(self) -> bool:
        """
        Установка соединения с базой данных WordPress.
        
        Returns:
            bool: True если подключение успешно, False в противном случае.
            
        Example:
            >>> config = WordPressConfig(host='localhost', database='wordpress')
            >>> wp_db = WordPressDB(config)
            >>> if wp_db.connect():
            ...     print('Подключение успешно')
            Подключение успешно
        """
        try:
            self.connection = pymysql.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                charset=self.config.charset,
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=10,
                read_timeout=10,
                write_timeout=10
            )
            
            self._connected = True
            logger.info(f'Успешное подключение к WordPress базе данных: {self.config.database}')
            return True
            
        except pymysql.Error as ex:
            logger.error(f'Ошибка подключения к базе данных WordPress: {ex}', ex)
            self._connected = False
            return False
    
    def is_connected(self) -> bool:
        """
        Проверка активности соединения с базой данных.
        
        Returns:
            bool: True если соединение активно, False в противном случае.
        """
        if not self.connection:
            return False
            
        try:
            self.connection.ping(reconnect=True)
            return True
        except pymysql.Error:
            self._connected = False
            return False
    
    def reconnect(self) -> bool:
        """
        Переподключение к базе данных.
        
        Returns:
            bool: True если переподключение успешно, False в противном случае.
        """
        self.close()
        return self.connect()
    
    @contextmanager
    def get_cursor(self):
        """
        Контекстный менеджер для получения курсора базы данных.
        
        Yields:
            cursor: Курсор для выполнения SQL-запросов.
            
        Example:
            >>> with wp_db.get_cursor() as cursor:
            ...     cursor.execute('SELECT COUNT(*) as count FROM wp_posts')
            ...     result = cursor.fetchone()
        """
        if not self.is_connected():
            if not self.reconnect():
                logger.error('Невозможно установить соединение с базой данных')
                yield None
                return
        
        cursor = None
        try:
            cursor = self.connection.cursor()
            yield cursor
            
        except pymysql.Error as ex:
            logger.error(f'Ошибка при работе с курсором: {ex}', ex)
            if self.connection:
                self.connection.rollback()
            yield None
        finally:
            if cursor:
                cursor.close()
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Выполнение SQL-запроса с возвращением результата.
        
        Args:
            query (str): SQL-запрос для выполнения.
            params (Optional[Tuple]): Параметры запроса.
            
        Returns:
            List[Dict[str, Any]]: Результат выполнения запроса.
            
        Example:
            >>> posts = wp_db.execute_query('SELECT * FROM wp_posts WHERE post_status = %s', ('publish',))
            >>> print(f'Найдено постов: {len(posts)}')
        """
        results: List[Dict[str, Any]] = []
        
        with self.get_cursor() as cursor:
            if not cursor:
                return results
            
            try:
                cursor.execute(query, params or ())
                results = cursor.fetchall() or []
                
            except pymysql.Error as ex:
                logger.error(f'Ошибка выполнения запроса: {query[:100]}...', ex)
                
        return results
    
    def execute_single_query(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Выполнение SQL-запроса с возвращением одного результата.
        
        Args:
            query (str): SQL-запрос для выполнения.
            params (Optional[Tuple]): Параметры запроса.
            
        Returns:
            Optional[Dict[str, Any]]: Единственный результат или None.
        """
        with self.get_cursor() as cursor:
            if not cursor:
                return None
            
            try:
                cursor.execute(query, params or ())
                return cursor.fetchone()
                
            except pymysql.Error as ex:
                logger.error(f'Ошибка выполнения запроса: {query[:100]}...', ex)
                return None
    
    def get_table_name(self, table: str) -> str:
        """
        Получение полного имени таблицы с префиксом.
        
        Args:
            table (str): Название таблицы без префикса.
            
        Returns:
            str: Полное название таблицы с префиксом.
        """
        return f'{self.config.table_prefix}{table}'
    
    # === WordPress специфичные методы ===
    
    def get_posts(self, limit: int = 10, post_type: str = 'post', post_status: str = 'publish') -> List[Dict[str, Any]]:
        """
        Получение постов WordPress.
        
        Args:
            limit (int): Максимальное количество постов.
            post_type (str): Тип поста (post, page, и т.д.).
            post_status (str): Статус поста (publish, draft, и т.д.).
            
        Returns:
            List[Dict[str, Any]]: Список постов.
        """
        query: str = f'''
            SELECT 
                ID, 
                post_title, 
                post_content, 
                post_excerpt,
                post_date, 
                post_status,
                post_type,
                post_author,
                comment_count
            FROM {self.get_table_name('posts')}
            WHERE post_status = %s 
            AND post_type = %s
            ORDER BY post_date DESC 
            LIMIT %s
        '''
        
        return self.execute_query(query, (post_status, post_type, limit))
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Получение поста по ID.
        
        Args:
            post_id (int): ID поста.
            
        Returns:
            Optional[Dict[str, Any]]: Данные поста или None.
        """
        query: str = f'''
            SELECT 
                ID, 
                post_title, 
                post_content, 
                post_excerpt,
                post_date, 
                post_status,
                post_type,
                post_author,
                comment_count
            FROM {self.get_table_name('posts')}
            WHERE ID = %s
        '''
        
        return self.execute_single_query(query, (post_id,))
    
    def get_post_meta(self, post_id: int, meta_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Получение метаданных поста.
        
        Args:
            post_id (int): ID поста.
            meta_key (Optional[str]): Конкретный ключ метаданных.
            
        Returns:
            Dict[str, Any]: Словарь метаданных поста.
        """
        if meta_key:
            query: str = f'''
                SELECT meta_key, meta_value 
                FROM {self.get_table_name('postmeta')}
                WHERE post_id = %s AND meta_key = %s
            '''
            params = (post_id, meta_key)
        else:
            query = f'''
                SELECT meta_key, meta_value 
                FROM {self.get_table_name('postmeta')}
                WHERE post_id = %s
            '''
            params = (post_id,)
        
        results = self.execute_query(query, params)
        meta_dict: Dict[str, Any] = {}
        
        for row in results:
            meta_dict[row['meta_key']] = row['meta_value']
            
        return meta_dict
    
    def get_posts_with_meta(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Получение постов с их метаданными.
        
        Args:
            limit (int): Максимальное количество постов.
            
        Returns:
            List[Dict[str, Any]]: Список постов с метаданными.
        """
        posts = self.get_posts(limit=limit)
        
        for post in posts:
            post['meta'] = self.get_post_meta(post['ID'])
            
        return posts
    
    def get_users(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Получение пользователей WordPress.
        
        Args:
            limit (int): Максимальное количество пользователей.
            
        Returns:
            List[Dict[str, Any]]: Список пользователей.
        """
        query: str = f'''
            SELECT 
                ID,
                user_login,
                user_nicename,
                user_email,
                user_registered,
                display_name
            FROM {self.get_table_name('users')}
            ORDER BY user_registered DESC
            LIMIT %s
        '''
        
        return self.execute_query(query, (limit,))
    
    def get_comments(self, post_id: Optional[int] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Получение комментариев WordPress.
        
        Args:
            post_id (Optional[int]): ID поста для фильтрации комментариев.
            limit (int): Максимальное количество комментариев.
            
        Returns:
            List[Dict[str, Any]]: Список комментариев.
        """
        if post_id:
            query: str = f'''
                SELECT 
                    comment_ID,
                    comment_post_ID,
                    comment_author,
                    comment_author_email,
                    comment_content,
                    comment_date,
                    comment_approved
                FROM {self.get_table_name('comments')}
                WHERE comment_post_ID = %s AND comment_approved = '1'
                ORDER BY comment_date DESC
                LIMIT %s
            '''
            params = (post_id, limit)
        else:
            query = f'''
                SELECT 
                    comment_ID,
                    comment_post_ID,
                    comment_author,
                    comment_author_email,
                    comment_content,
                    comment_date,
                    comment_approved
                FROM {self.get_table_name('comments')}
                WHERE comment_approved = '1'
                ORDER BY comment_date DESC
                LIMIT %s
            '''
            params = (limit,)
        
        return self.execute_query(query, params)
    
    def get_options(self) -> Dict[str, Any]:
        """
        Получение настроек WordPress.
        
        Returns:
            Dict[str, Any]: Словарь настроек WordPress.
        """
        query: str = f'''
            SELECT option_name, option_value 
            FROM {self.get_table_name('options')}
        '''
        
        results = self.execute_query(query)
        options_dict: Dict[str, Any] = {}
        
        for row in results:
            options_dict[row['option_name']] = row['option_value']
            
        return options_dict
    
    def get_option(self, option_name: str) -> Optional[str]:
        """
        Получение конкретной настройки WordPress.
        
        Args:
            option_name (str): Название настройки.
            
        Returns:
            Optional[str]: Значение настройки или None.
        """
        query: str = f'''
            SELECT option_value 
            FROM {self.get_table_name('options')}
            WHERE option_name = %s
        '''
        
        result = self.execute_single_query(query, (option_name,))
        return result['option_value'] if result else None
    
    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        if self.connection:
            try:
                self.connection.close()
                self._connected = False
                logger.info('Соединение с базой данных WordPress закрыто')
            except Exception as ex:
                logger.error(f'Ошибка при закрытии соединения: {ex}', ex)


def load_config_from_wp_config(wp_config_path: str | Path) -> Optional[WordPressConfig]:
    """
    Загрузка конфигурации из файла wp-config.php.
    
    Args:
        wp_config_path (str | Path): Путь к файлу wp-config.php.
        
    Returns:
        Optional[WordPressConfig]: Конфигурация или None при ошибке.
    """
    config_path: Path = Path(wp_config_path)
    
    if not config_path.exists():
        logger.error(f'Файл wp-config.php не найден: {config_path}')
        return None
    
    try:
        content: str = config_path.read_text(encoding='utf-8')
        
        # Извлечение параметров базы данных
        db_name_match = re.search(r"define\(\s*['\"]DB_NAME['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\);", content)
        db_user_match = re.search(r"define\(\s*['\"]DB_USER['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\);", content)
        db_password_match = re.search(r"define\(\s*['\"]DB_PASSWORD['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\);", content)
        db_host_match = re.search(r"define\(\s*['\"]DB_HOST['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\);", content)
        table_prefix_match = re.search(r"\$table_prefix\s*=\s*['\"]([^'\"]+)['\"];", content)
        
        if not all([db_name_match, db_user_match, db_host_match]):
            logger.error('Не удалось найти необходимые параметры базы данных в wp-config.php')
            return None
        
        # Парсинг хоста и порта
        host_port: str = db_host_match.group(1)
        host: str = host_port
        port: int = 3306
        
        if ':' in host_port:
            host, port_str = host_port.split(':', 1)
            try:
                port = int(port_str)
            except ValueError:
                logger.warning(f'Невалидный порт в wp-config.php: {port_str}, использую порт по умолчанию 3306')
                port = 3306
        
        return WordPressConfig(
            host=host,
            port=port,
            database=db_name_match.group(1),
            username=db_user_match.group(1),
            password=db_password_match.group(1) if db_password_match else '',
            table_prefix=table_prefix_match.group(1) if table_prefix_match else 'wp_'
        )
        
    except Exception as ex:
        logger.error(f'Ошибка при парсинге wp-config.php: {ex}', ex)
        return None


def create_wp_config(config: WordPressConfig, config_path: str | Path = None) -> bool:
    """
    Сохранение конфигурации WordPress в JSON файл.
    
    Args:
        config (WordPressConfig): Конфигурация для сохранения.
        config_path (str | Path): Путь для сохранения конфигурации.
        
    Returns:
        bool: True если сохранение успешно, False в противном случае.
    """
    if not config_path:
        config_path = __root__ / 'config' / 'wordpress_db.json'
    
    config_data = {
        'host': config.host,
        'port': config.port,
        'database': config.database,
        'username': config.username,
        'password': config.password,
        'charset': config.charset,
        'table_prefix': config.table_prefix
    }
    
    return j_dumps(config_data, config_path)


def load_wp_config(config_path: str | Path = None) -> Optional[WordPressConfig]:
    """
    Загрузка конфигурации WordPress из JSON файла.
    
    Args:
        config_path (str | Path): Путь к файлу конфигурации.
        
    Returns:
        Optional[WordPressConfig]: Загруженная конфигурация или None.
    """
    if not config_path:
        config_path = __root__ / 'config' / 'wordpress_db.json'
    
    config_data = j_loads_ns(config_path)
    
    if not config_data:
        logger.error(f'Не удалось загрузить конфигурацию из {config_path}')
        return None
    
    return WordPressConfig(
        host=getattr(config_data, 'host', 'localhost'),
        port=getattr(config_data, 'port', 3306),
        database=getattr(config_data, 'database', 'wordpress'),
        username=getattr(config_data, 'username', 'wp_user'),
        password=getattr(config_data, 'password', ''),
        charset=getattr(config_data, 'charset', 'utf8mb4'),
        table_prefix=getattr(config_data, 'table_prefix', 'wp_')
    )


# === Примеры использования ===

def example_basic_usage():
    """Базовый пример использования WordPress базы данных."""
    
    # Создание конфигурации
    config = WordPressConfig(
        host='localhost',
        database='wordpress',
        username='wp_user',
        password='your_password'
    )
    
    # Подключение к базе данных
    wp_db = WordPressDB(config)
    
    if not wp_db.connect():
        print('Не удалось подключиться к базе данных')
        return
    
    # Получение последних постов
    posts = wp_db.get_posts(limit=5)
    print(f'Найдено постов: {len(posts)}')
    
    for post in posts:
        print(f"ID: {post['ID']}, Заголовок: {post['post_title']}")
        print(f"Дата: {post['post_date']}")
        print('-' * 50)
    
    # Получение информации о сайте
    site_title = wp_db.get_option('blogname')
    site_url = wp_db.get_option('siteurl')
    
    print(f'Название сайта: {site_title}')
    print(f'URL сайта: {site_url}')
    
    # Закрытие соединения
    wp_db.close()


def example_load_from_wp_config():
    """Пример загрузки конфигурации из wp-config.php."""
    
    # Загрузка конфигурации из wp-config.php
    config = load_config_from_wp_config('/path/to/wordpress/wp-config.php')
    
    if not config:
        print('Не удалось загрузить конфигурацию из wp-config.php')
        return
    
    wp_db = WordPressDB(config)
    
    if wp_db.connect():
        # Работа с базой данных
        users = wp_db.get_users(limit=3)
        print(f'Пользователи: {len(users)}')
        
        for user in users:
            print(f"Логин: {user['user_login']}, Email: {user['user_email']}")
        
        wp_db.close()


def main():
    """Главная функция для демонстрации."""
    print('=== Пример работы с WordPress базой данных через PyMySQL ===')
    
    # Запуск примеров
    example_basic_usage()
    print('\n' + '='*60 + '\n')
    # example_load_from_wp_config()  # Раскомментируйте для использования


if __name__ == '__main__':
    main()