## \file src/database/wordpress_models.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль с моделями WordPress и CRUD операциями.
=============================================
Содержит классы для работы с постами, пользователями и другими сущностями WordPress
с полной поддержкой создания, обновления и удаления.

```rst
.. module:: src.database.wordpress_models
```
"""

import header
from header import __root__
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns, j_dumps
from src.utils.printer import pprint as print

from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
from datetime import datetime
import pymysql
from .wordpress_pymysql import WordPressDB


@dataclass
class Post:
    """Модель поста WordPress с полной поддержкой CRUD операций."""
    
    ID: Optional[int] = None
    post_author: int = 1
    post_date: Optional[datetime] = None
    post_date_gmt: Optional[datetime] = None
    post_content: str = ''
    post_title: str = ''
    post_excerpt: str = ''
    post_status: str = 'draft'  # publish, draft, private, pending
    comment_status: str = 'open'  # open, closed
    ping_status: str = 'open'  # open, closed
    post_password: str = ''
    post_name: str = ''  # slug
    to_ping: str = ''
    pinged: str = ''
    post_modified: Optional[datetime] = None
    post_modified_gmt: Optional[datetime] = None
    post_content_filtered: str = ''
    post_parent: int = 0
    guid: str = ''
    menu_order: int = 0
    post_type: str = 'post'  # post, page, attachment, custom
    post_mime_type: str = ''
    comment_count: int = 0
    
    # Дополнительные поля
    meta: Dict[str, Any] = field(default_factory=dict)
    categories: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Инициализация после создания объекта."""
        current_time = gs.now
        
        if not self.post_date:
            self.post_date = current_time
        if not self.post_date_gmt:
            self.post_date_gmt = current_time
        if not self.post_modified:
            self.post_modified = current_time
        if not self.post_modified_gmt:
            self.post_modified_gmt = current_time
            
        # Генерация slug из заголовка если не указан
        if not self.post_name and self.post_title:
            self.post_name = self._generate_slug(self.post_title)
    
    def _generate_slug(self, title: str) -> str:
        """
        Генерация slug из заголовка поста.
        
        Args:
            title (str): Заголовок поста.
            
        Returns:
            str: Сгенерированный slug.
        """
        import re
        
        # Преобразование в нижний регистр и замена пробелов на дефисы
        slug = title.lower()
        # Удаление специальных символов
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Замена пробелов и множественных дефисов на один дефис
        slug = re.sub(r'[\s_-]+', '-', slug)
        # Удаление дефисов в начале и конце
        slug = slug.strip('-')
        
        return slug[:200]  # Ограничение длины
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта в словарь для сохранения в базу данных.
        
        Returns:
            Dict[str, Any]: Словарь с данными поста.
        """
        data = {
            'post_author': self.post_author,
            'post_date': self.post_date.strftime('%Y-%m-%d %H:%M:%S') if self.post_date else None,
            'post_date_gmt': self.post_date_gmt.strftime('%Y-%m-%d %H:%M:%S') if self.post_date_gmt else None,
            'post_content': self.post_content,
            'post_title': self.post_title,
            'post_excerpt': self.post_excerpt,
            'post_status': self.post_status,
            'comment_status': self.comment_status,
            'ping_status': self.ping_status,
            'post_password': self.post_password,
            'post_name': self.post_name,
            'to_ping': self.to_ping,
            'pinged': self.pinged,
            'post_modified': self.post_modified.strftime('%Y-%m-%d %H:%M:%S') if self.post_modified else None,
            'post_modified_gmt': self.post_modified_gmt.strftime('%Y-%m-%d %H:%M:%S') if self.post_modified_gmt else None,
            'post_content_filtered': self.post_content_filtered,
            'post_parent': self.post_parent,
            'guid': self.guid,
            'menu_order': self.menu_order,
            'post_type': self.post_type,
            'post_mime_type': self.post_mime_type,
            'comment_count': self.comment_count
        }
        
        # Добавление ID только если он существует (для обновления)
        if self.ID:
            data['ID'] = self.ID
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        """
        Создание объекта Post из словаря.
        
        Args:
            data (Dict[str, Any]): Данные поста из базы данных.
            
        Returns:
            Post: Объект поста.
        """
        # Преобразование строк даты в datetime объекты
        for date_field in ['post_date', 'post_date_gmt', 'post_modified', 'post_modified_gmt']:
            if data.get(date_field) and isinstance(data[date_field], str):
                try:
                    data[date_field] = datetime.strptime(data[date_field], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    data[date_field] = None
        
        return cls(**data)
    
    def add(self, wp_db: WordPressDB) -> bool:
        """
        Добавление нового поста в базу данных.
        
        Args:
            wp_db (WordPressDB): Объект подключения к базе данных.
            
        Returns:
            bool: True если пост успешно добавлен, False в противном случае.
            
        Example:
            >>> post = Post(post_title='Новый пост', post_content='Содержимое поста')
            >>> if post.add(wp_db):
            ...     print(f'Пост добавлен с ID: {post.ID}')
        """
        if not wp_db.is_connected():
            logger.error('Нет подключения к базе данных')
            return False
        
        data = self.to_dict()
        
        # Удаление ID для вставки нового поста
        if 'ID' in data:
            del data['ID']
        
        # Подготовка запроса INSERT
        columns = list(data.keys())
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        query = f'''
            INSERT INTO {wp_db.get_table_name('posts')} 
            ({columns_str}) 
            VALUES ({placeholders})
        '''
        
        try:
            with wp_db.get_cursor() as cursor:
                if not cursor:
                    return False
                
                cursor.execute(query, list(data.values()))
                
                # Получение ID нового поста
                self.ID = cursor.lastrowid
                
                # Обновление GUID если не указан
                if not self.guid and self.ID:
                    site_url = wp_db.get_option('siteurl') or 'http://localhost'
                    self.guid = f'{site_url}/?p={self.ID}'
                    
                    update_guid_query = f'''
                        UPDATE {wp_db.get_table_name('posts')} 
                        SET guid = %s 
                        WHERE ID = %s
                    '''
                    cursor.execute(update_guid_query, (self.guid, self.ID))
                
                # Добавление метаданных
                if self.meta:
                    self._save_meta(wp_db)
                
                logger.info(f'Пост успешно добавлен с ID: {self.ID}')
                return True
                
        except pymysql.Error as ex:
            logger.error(f'Ошибка при добавлении поста: {ex}', ex)
            return False
    
    def update(self, wp_db: WordPressDB) -> bool:
        """
        Обновление существующего поста в базе данных.
        
        Args:
            wp_db (WordPressDB): Объект подключения к базе данных.
            
        Returns:
            bool: True если пост успешно обновлен, False в противном случае.
            
        Example:
            >>> post.post_title = 'Обновленный заголовок'
            >>> if post.update(wp_db):
            ...     print('Пост обновлен')
        """
        if not self.ID:
            logger.error('Нельзя обновить пост без ID')
            return False
            
        if not wp_db.is_connected():
            logger.error('Нет подключения к базе данных')
            return False
        
        # Обновление времени модификации
        self.post_modified = gs.now
        self.post_modified_gmt = gs.now
        
        data = self.to_dict()
        
        # Удаление ID из данных для обновления
        post_id = data.pop('ID')
        
        # Подготовка запроса UPDATE
        set_clauses = [f'{column} = %s' for column in data.keys()]
        set_clause = ', '.join(set_clauses)
        
        query = f'''
            UPDATE {wp_db.get_table_name('posts')} 
            SET {set_clause}
            WHERE ID = %s
        '''
        
        try:
            with wp_db.get_cursor() as cursor:
                if not cursor:
                    return False
                
                values = list(data.values()) + [post_id]
                cursor.execute(query, values)
                
                # Обновление метаданных
                if self.meta:
                    self._save_meta(wp_db)
                
                logger.info(f'Пост с ID {self.ID} успешно обновлен')
                return True
                
        except pymysql.Error as ex:
            logger.error(f'Ошибка при обновлении поста с ID {self.ID}: {ex}', ex)
            return False
    
    def delete(self, wp_db: WordPressDB, force_delete: bool = False) -> bool:
        """
        Удаление поста из базы данных.
        
        Args:
            wp_db (WordPressDB): Объект подключения к базе данных.
            force_delete (bool): Если True, пост будет удален навсегда, 
                               иначе перемещен в корзину.
            
        Returns:
            bool: True если пост успешно удален, False в противном случае.
            
        Example:
            >>> if post.delete(wp_db, force_delete=True):
            ...     print('Пост удален')
        """
        if not self.ID:
            logger.error('Нельзя удалить пост без ID')
            return False
            
        if not wp_db.is_connected():
            logger.error('Нет подключения к базе данных')
            return False
        
        try:
            if force_delete:
                # Полное удаление поста
                with wp_db.get_cursor() as cursor:
                    if not cursor:
                        return False
                    
                    # Удаление метаданных
                    cursor.execute(
                        f'DELETE FROM {wp_db.get_table_name("postmeta")} WHERE post_id = %s',
                        (self.ID,)
                    )
                    
                    # Удаление связей с терминами (категории, теги)
                    cursor.execute(
                        f'DELETE FROM {wp_db.get_table_name("term_relationships")} WHERE object_id = %s',
                        (self.ID,)
                    )
                    
                    # Удаление самого поста
                    cursor.execute(
                        f'DELETE FROM {wp_db.get_table_name("posts")} WHERE ID = %s',
                        (self.ID,)
                    )
                    
                    logger.info(f'Пост с ID {self.ID} полностью удален')
            else:
                # Перемещение в корзину
                self.post_status = 'trash'
                self.post_modified = gs.now
                self.post_modified_gmt = gs.now
                
                if not self.update(wp_db):
                    return False
                    
                logger.info(f'Пост с ID {self.ID} перемещен в корзину')
            
            return True
            
        except pymysql.Error as ex:
            logger.error(f'Ошибка при удалении поста с ID {self.ID}: {ex}', ex)
            return False
    
    def _save_meta(self, wp_db: WordPressDB) -> bool:
        """
        Сохранение метаданных поста.
        
        Args:
            wp_db (WordPressDB): Объект подключения к базе данных.
            
        Returns:
            bool: True если метаданные успешно сохранены, False в противном случае.
        """
        if not self.ID or not self.meta:
            return True
        
        try:
            with wp_db.get_cursor() as cursor:
                if not cursor:
                    return False
                
                for meta_key, meta_value in self.meta.items():
                    # Проверка существования метаданных
                    cursor.execute(
                        f'SELECT meta_id FROM {wp_db.get_table_name("postmeta")} WHERE post_id = %s AND meta_key = %s',
                        (self.ID, meta_key)
                    )
                    
                    existing_meta = cursor.fetchone()
                    
                    # Преобразование сложных типов в строку
                    if isinstance(meta_value, (dict, list)):
                        import json
                        meta_value = json.dumps(meta_value, ensure_ascii=False)
                    
                    if existing_meta:
                        # Обновление существующих метаданных
                        cursor.execute(
                            f'UPDATE {wp_db.get_table_name("postmeta")} SET meta_value = %s WHERE meta_id = %s',
                            (str(meta_value), existing_meta['meta_id'])
                        )
                    else:
                        # Добавление новых метаданных
                        cursor.execute(
                            f'INSERT INTO {wp_db.get_table_name("postmeta")} (post_id, meta_key, meta_value) VALUES (%s, %s, %s)',
                            (self.ID, meta_key, str(meta_value))
                        )
                
                return True
                
        except pymysql.Error as ex:
            logger.error(f'Ошибка при сохранении метаданных поста с ID {self.ID}: {ex}', ex)
            return False


@dataclass
class User:
    """Модель пользователя WordPress."""
    
    ID: Optional[int] = None
    user_login: str = ''
    user_pass: str = ''
    user_nicename: str = ''
    user_email: str = ''
    user_url: str = ''
    user_registered: Optional[datetime] = None
    user_activation_key: str = ''
    user_status: int = 0
    display_name: str = ''
    
    # Дополнительные поля
    meta: Dict[str, Any] = field(default_factory=dict)
    roles: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Инициализация после создания объекта."""
        if not self.user_registered:
            self.user_registered = gs.now
            
        if not self.user_nicename and self.user_login:
            self.user_nicename = self.user_login.lower()
            
        if not self.display_name:
            self.display_name = self.user_login
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта в словарь."""
        data = {
            'user_login': self.user_login,
            'user_pass': self.user_pass,
            'user_nicename': self.user_nicename,
            'user_email': self.user_email,
            'user_url': self.user_url,
            'user_registered': self.user_registered.strftime('%Y-%m-%d %H:%M:%S') if self.user_registered else None,
            'user_activation_key': self.user_activation_key,
            'user_status': self.user_status,
            'display_name': self.display_name
        }
        
        if self.ID:
            data['ID'] = self.ID
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Создание объекта User из словаря."""
        if data.get('user_registered') and isinstance(data['user_registered'], str):
            try:
                data['user_registered'] = datetime.strptime(data['user_registered'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                data['user_registered'] = None
        
        return cls(**data)
    
    def add(self, wp_db: WordPressDB) -> bool:
        """Добавление нового пользователя."""
        if not wp_db.is_connected():
            logger.error('Нет подключения к базе данных')
            return False
        
        data = self.to_dict()
        if 'ID' in data:
            del data['ID']
        
        columns = list(data.keys())
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        query = f'''
            INSERT INTO {wp_db.get_table_name('users')} 
            ({columns_str}) 
            VALUES ({placeholders})
        '''
        
        try:
            with wp_db.get_cursor() as cursor:
                if not cursor:
                    return False
                
                cursor.execute(query, list(data.values()))
                self.ID = cursor.lastrowid
                
                logger.info(f'Пользователь успешно добавлен с ID: {self.ID}')
                return True
                
        except pymysql.Error as ex:
            logger.error(f'Ошибка при добавлении пользователя: {ex}', ex)
            return False
    
    def update(self, wp_db: WordPressDB) -> bool:
        """Обновление существующего пользователя."""
        if not self.ID:
            logger.error('Нельзя обновить пользователя без ID')
            return False
            
        if not wp_db.is_connected():
            logger.error('Нет подключения к базе данных')
            return False
        
        data = self.to_dict()
        user_id = data.pop('ID')
        
        set_clauses = [f'{column} = %s' for column in data.keys()]
        set_clause = ', '.join(set_clauses)
        
        query = f'''
            UPDATE {wp_db.get_table_name('users')} 
            SET {set_clause}
            WHERE ID = %s
        '''
        
        try:
            with wp_db.get_cursor() as cursor:
                if not cursor:
                    return False
                
                values = list(data.values()) + [user_id]
                cursor.execute(query, values)
                
                logger.info(f'Пользователь с ID {self.ID} успешно обновлен')
                return True
                
        except pymysql.Error as ex:
            logger.error(f'Ошибка при обновлении пользователя с ID {self.ID}: {ex}', ex)
            return False
    
    def delete(self, wp_db: WordPressDB) -> bool:
        """Удаление пользователя."""
        if not self.ID:
            logger.error('Нельзя удалить пользователя без ID')
            return False
            
        if not wp_db.is_connected():
            logger.error('Нет подключения к базе данных')
            return False
        
        try:
            with wp_db.get_cursor() as cursor:
                if not cursor:
                    return False
                
                # Удаление метаданных пользователя
                cursor.execute(
                    f'DELETE FROM {wp_db.get_table_name("usermeta")} WHERE user_id = %s',
                    (self.ID,)
                )
                
                # Удаление самого пользователя
                cursor.execute(
                    f'DELETE FROM {wp_db.get_table_name("users")} WHERE ID = %s',
                    (self.ID,)
                )
                
                logger.info(f'Пользователь с ID {self.ID} успешно удален')
                return True
                
        except pymysql.Error as ex:
            logger.error(f'Ошибка при удалении пользователя с ID {self.ID}: {ex}', ex)
            return False


# === Функции для работы с постами ===

def add_new_post(wp_db: WordPressDB, post: Post) -> Optional[int]:
    """
    Добавление нового поста в WordPress.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post (Post): Объект поста для добавления.
        
    Returns:
        Optional[int]: ID нового поста или None при ошибке.
        
    Example:
        >>> new_post = Post(
        ...     post_title='Новый пост',
        ...     post_content='Содержимое поста',
        ...     post_status='publish'
        ... )
        >>> post_id = add_new_post(wp_db, new_post)
        >>> if post_id:
        ...     print(f'Пост создан с ID: {post_id}')
    """
    if not isinstance(post, Post):
        logger.error('Параметр post должен быть экземпляром класса Post')
        return None
    
    if post.add(wp_db):
        return post.ID
    
    return None


def update_post(wp_db: WordPressDB, post: Post) -> bool:
    """
    Обновление существующего поста в WordPress.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post (Post): Объект поста для обновления.
        
    Returns:
        bool: True если пост успешно обновлен, False в противном случае.
        
    Example:
        >>> post = get_post_by_id(wp_db, 123)
        >>> if post:
        ...     post.post_title = 'Обновленный заголовок'
        ...     if update_post(wp_db, post):
        ...         print('Пост обновлен')
    """
    if not isinstance(post, Post):
        logger.error('Параметр post должен быть экземпляром класса Post')
        return False
    
    return post.update(wp_db)


def get_post_by_id(wp_db: WordPressDB, post_id: int, include_meta: bool = True) -> Optional[Post]:
    """
    Получение поста по ID.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post_id (int): ID поста.
        include_meta (bool): Включать ли метаданные поста.
        
    Returns:
        Optional[Post]: Объект поста или None.
    """
    post_data = wp_db.get_post_by_id(post_id)
    
    if not post_data:
        return None
    
    post = Post.from_dict(post_data)
    
    if include_meta:
        post.meta = wp_db.get_post_meta(post_id)
    
    return post


def delete_post(wp_db: WordPressDB, post_id: int, force_delete: bool = False) -> bool:
    """
    Удаление поста по ID.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post_id (int): ID поста для удаления.
        force_delete (bool): Полное удаление или перемещение в корзину.
        
    Returns:
        bool: True если пост успешно удален, False в противном случае.
    """
    post = get_post_by_id(wp_db, post_id, include_meta=False)
    
    if not post:
        logger.error(f'Пост с ID {post_id} не найден')
        return False
    
    return post.delete(wp_db, force_delete=force_delete)


def get_posts_by_criteria(
    wp_db: WordPressDB, 
    post_type: str = 'post', 
    post_status: str = 'publish',
    limit: int = 10,
    author_id: Optional[int] = None,
    category: Optional[str] = None
) -> List[Post]:
    """
    Получение постов по заданным критериям.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post_type (str): Тип поста.
        post_status (str): Статус поста.
        limit (int): Максимальное количество постов.
        author_id (Optional[int]): ID автора для фильтрации.
        category (Optional[str]): Название категории для фильтрации.
        
    Returns:
        List[Post]: Список объектов постов.
    """
    # Базовый запрос
    query_parts = [f'''
        SELECT 
            p.ID, p.post_author, p.post_date, p.post_date_gmt,
            p.post_content, p.post_title, p.post_excerpt, p.post_status,
            p.comment_status, p.ping_status, p.post_password, p.post_name,
            p.to_ping, p.pinged, p.post_modified, p.post_modified_gmt,
            p.post_content_filtered, p.post_parent, p.guid, p.menu_order,
            p.post_type, p.post_mime_type, p.comment_count
        FROM {wp_db.get_table_name('posts')} p
    ''']
    
    conditions = ['p.post_type = %s', 'p.post_status = %s']
    params = [post_type, post_status]
    
    # Добавление фильтра по автору
    if author_id:
        conditions.append('p.post_author = %s')
        params.append(author_id)
    
    # Добавление фильтра по категории
    if category:
        query_parts.append(f'''
            JOIN {wp_db.get_table_name('term_relationships')} tr ON p.ID = tr.object_id
            JOIN {wp_db.get_table_name('term_taxonomy')} tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
            JOIN {wp_db.get_table_name('terms')} t ON tt.term_id = t.term_id
        ''')
        conditions.extend(['tt.taxonomy = %s', 't.name = %s'])
        params.extend(['category', category])
    
    # Сборка финального запроса
    query = ' '.join(query_parts)
    query += ' WHERE ' + ' AND '.join(conditions)
    query += ' ORDER BY p.post_date DESC LIMIT %s'
    params.append(limit)
    
    results = wp_db.execute_query(query, tuple(params))
    posts = []
    
    for row in results:
        post = Post.from_dict(row)
        posts.append(post)
    
    return posts


# === Примеры использования ===

def example_post_operations():
    """Пример операций с постами."""
    from .wordpress_pymysql import WordPressConfig, WordPressDB
    
    # Настройка подключения
    config = WordPressConfig(
        host='localhost',
        database='wordpress',
        username='wp_user',
        password='password'
    )
    
    wp_db = WordPressDB(config)
    
    if not wp_db.connect():
        print('Не удалось подключиться к базе данных')
        return
    
    # Создание нового поста
    new_post = Post(
        post_title='Тестовый пост из Python',
        post_content='<p>Это содержимое поста, созданного из Python!</p>',
        post_excerpt='Краткое описание поста',
        post_status='publish',
        post_author=1,
        meta={
            '_custom_field': 'Пользовательское значение',
            '_seo_title': 'SEO заголовок поста'
        }
    )
    
    # Добавление поста
    post_id = add_new_post(wp_db, new_post)
    
    if post_id:
        print(f'✅ Пост успешно создан с ID: {post_id}')
        
        # Получение созданного поста
        created_post = get_post_by_id(wp_db, post_id)
        if created_post:
            print(f'📄 Заголовок: {created_post.post_title}')
            print(f'📅 Дата создания: {created_post.post_date}')
            print(f'🔗 Slug: {created_post.post_name}')
            print(f'📊 Метаданные: {len(created_post.meta)} элементов')
            
            # Обновление поста
            created_post.post_title = 'Обновленный заголовок поста'
            created_post.post_content += '\n<p>Дополнительный контент после обновления.</p>'
            created_post.meta['_updated_from_python'] = 'true'
            
            if update_post(wp_db, created_post):
                print('✅ Пост успешно обновлен')
            else:
                print('❌ Ошибка при обновлении поста')
            
            # Демонстрация удаления (перемещение в корзину)
            # if delete_post(wp_db, post_id, force_delete=False):
            #     print('🗑️ Пост перемещен в корзину')
    else:
        print('❌ Ошибка при создании поста')
    
    # Получение постов по критериям
    recent_posts = get_posts_by_criteria(
        wp_db,
        post_type='post',
        post_status='publish',
        limit=5
    )
    
    print(f'\n📝 Найдено {len(recent_posts)} опубликованных постов:')
    for post in recent_posts:
        print(f'  • {post.post_title} (ID: {post.ID})')
    
    wp_db.close()


def example_user_operations():
    """Пример операций с пользователями."""
    from .wordpress_pymysql import WordPressConfig, WordPressDB
    
    config = WordPressConfig(
        host='localhost',
        database='wordpress',
        username='wp_user',
        password='password'
    )
    
    wp_db = WordPressDB(config)
    
    if not wp_db.connect():
        print('Не удалось подключиться к базе данных')
        return
    
    # Создание нового пользователя
    new_user = User(
        user_login='python_user',
        user_email='python@example.com',
        user_pass='hashed_password',  # В реальности должен быть хешированный пароль
        display_name='Python User',
        user_url='https://python.org'
    )
    
    if new_user.add(wp_db):
        print(f'✅ Пользователь создан с ID: {new_user.ID}')
        
        # Обновление пользователя
        new_user.display_name = 'Обновленное имя'
        if new_user.update(wp_db):
            print('✅ Пользователь обновлен')
    
    wp_db.close()


def bulk_import_posts(wp_db: WordPressDB, posts_data: List[Dict[str, Any]]) -> List[int]:
    """
    Массовый импорт постов в WordPress.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        posts_data (List[Dict[str, Any]]): Список данных постов для импорта.
        
    Returns:
        List[int]: Список ID созданных постов.
        
    Example:
        >>> posts_to_import = [
        ...     {'post_title': 'Пост 1', 'post_content': 'Содержимое 1'},
        ...     {'post_title': 'Пост 2', 'post_content': 'Содержимое 2'}
        ... ]
        >>> imported_ids = bulk_import_posts(wp_db, posts_to_import)
        >>> print(f'Импортировано {len(imported_ids)} постов')
    """
    imported_ids: List[int] = []
    
    for post_data in posts_data:
        try:
            post = Post(**post_data)
            post_id = add_new_post(wp_db, post)
            
            if post_id:
                imported_ids.append(post_id)
                logger.info(f'Пост "{post.post_title}" импортирован с ID: {post_id}')
            else:
                logger.error(f'Не удалось импортировать пост: {post_data.get("post_title", "Без заголовка")}')
                
        except Exception as ex:
            logger.error(f'Ошибка при создании поста из данных: {post_data}', ex)
    
    logger.info(f'Массовый импорт завершен. Импортировано {len(imported_ids)} из {len(posts_data)} постов')
    return imported_ids


def export_posts_to_json(wp_db: WordPressDB, output_file: str | Path, **criteria) -> bool:
    """
    Экспорт постов в JSON файл.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        output_file (str | Path): Путь к файлу для сохранения.
        **criteria: Критерии для фильтрации постов.
        
    Returns:
        bool: True если экспорт успешен, False в противном случае.
    """
    try:
        posts = get_posts_by_criteria(wp_db, **criteria)
        
        export_data = []
        for post in posts:
            post_dict = post.to_dict()
            # Преобразование datetime в строку для JSON
            for key, value in post_dict.items():
                if isinstance(value, datetime):
                    post_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            
            # Добавление метаданных
            post_dict['meta'] = post.meta
            export_data.append(post_dict)
        
        success = j_dumps(export_data, output_file)
        
        if success:
            logger.info(f'Экспортировано {len(posts)} постов в файл: {output_file}')
        
        return success
        
    except Exception as ex:
        logger.error(f'Ошибка при экспорте постов в файл {output_file}', ex)
        return False


def import_posts_from_json(wp_db: WordPressDB, input_file: str | Path) -> List[int]:
    """
    Импорт постов из JSON файла.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        input_file (str | Path): Путь к файлу с данными.
        
    Returns:
        List[int]: Список ID импортированных постов.
    """
    import_data = j_loads_ns(input_file)
    
    if not import_data:
        logger.error(f'Не удалось загрузить данные из файла: {input_file}')
        return []
    
    # Преобразование SimpleNamespace в dict если необходимо
    if hasattr(import_data, '__dict__'):
        import_data = vars(import_data)
    
    posts_data = import_data if isinstance(import_data, list) else [import_data]
    
    return bulk_import_posts(wp_db, posts_data)


# === Вспомогательные функции ===

def get_post_categories(wp_db: WordPressDB, post_id: int) -> List[str]:
    """
    Получение категорий поста.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post_id (int): ID поста.
        
    Returns:
        List[str]: Список названий категорий.
    """
    query = f'''
        SELECT t.name
        FROM {wp_db.get_table_name('terms')} t
        JOIN {wp_db.get_table_name('term_taxonomy')} tt ON t.term_id = tt.term_id
        JOIN {wp_db.get_table_name('term_relationships')} tr ON tt.term_taxonomy_id = tr.term_taxonomy_id
        WHERE tr.object_id = %s AND tt.taxonomy = 'category'
    '''
    
    results = wp_db.execute_query(query, (post_id,))
    return [row['name'] for row in results]


def get_post_tags(wp_db: WordPressDB, post_id: int) -> List[str]:
    """
    Получение тегов поста.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post_id (int): ID поста.
        
    Returns:
        List[str]: Список названий тегов.
    """
    query = f'''
        SELECT t.name
        FROM {wp_db.get_table_name('terms')} t
        JOIN {wp_db.get_table_name('term_taxonomy')} tt ON t.term_id = tt.term_id
        JOIN {wp_db.get_table_name('term_relationships')} tr ON tt.term_taxonomy_id = tr.term_taxonomy_id
        WHERE tr.object_id = %s AND tt.taxonomy = 'post_tag'
    '''
    
    results = wp_db.execute_query(query, (post_id,))
    return [row['name'] for row in results]


def set_post_categories(wp_db: WordPressDB, post_id: int, categories: List[str]) -> bool:
    """
    Установка категорий для поста.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        post_id (int): ID поста.
        categories (List[str]): Список названий категорий.
        
    Returns:
        bool: True если категории успешно установлены, False в противном случае.
    """
    try:
        with wp_db.get_cursor() as cursor:
            if not cursor:
                return False
            
            # Удаление существующих связей с категориями
            cursor.execute(f'''
                DELETE tr FROM {wp_db.get_table_name('term_relationships')} tr
                JOIN {wp_db.get_table_name('term_taxonomy')} tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
                WHERE tr.object_id = %s AND tt.taxonomy = 'category'
            ''', (post_id,))
            
            # Добавление новых категорий
            for category_name in categories:
                # Поиск существующей категории
                cursor.execute(f'''
                    SELECT tt.term_taxonomy_id 
                    FROM {wp_db.get_table_name('terms')} t
                    JOIN {wp_db.get_table_name('term_taxonomy')} tt ON t.term_id = tt.term_id
                    WHERE t.name = %s AND tt.taxonomy = 'category'
                ''', (category_name,))
                
                result = cursor.fetchone()
                
                if result:
                    term_taxonomy_id = result['term_taxonomy_id']
                else:
                    # Создание новой категории если не существует
                    cursor.execute(f'''
                        INSERT INTO {wp_db.get_table_name('terms')} (name, slug)
                        VALUES (%s, %s)
                    ''', (category_name, category_name.lower().replace(' ', '-')))
                    
                    term_id = cursor.lastrowid
                    
                    cursor.execute(f'''
                        INSERT INTO {wp_db.get_table_name('term_taxonomy')} (term_id, taxonomy)
                        VALUES (%s, 'category')
                    ''', (term_id,))
                    
                    term_taxonomy_id = cursor.lastrowid
                
                # Связывание поста с категорией
                cursor.execute(f'''
                    INSERT INTO {wp_db.get_table_name('term_relationships')} (object_id, term_taxonomy_id)
                    VALUES (%s, %s)
                ''', (post_id, term_taxonomy_id))
            
            logger.info(f'Категории поста {post_id} успешно обновлены')
            return True
            
    except pymysql.Error as ex:
        logger.error(f'Ошибка при установке категорий для поста {post_id}', ex)
        return False


def search_posts(wp_db: WordPressDB, search_term: str, limit: int = 20) -> List[Post]:
    """
    Поиск постов по ключевым словам.
    
    Args:
        wp_db (WordPressDB): Объект подключения к базе данных.
        search_term (str): Поисковый запрос.
        limit (int): Максимальное количество результатов.
        
    Returns:
        List[Post]: Список найденных постов.
    """
    search_pattern = f'%{search_term}%'
    
    query = f'''
        SELECT 
            ID, post_author, post_date, post_date_gmt,
            post_content, post_title, post_excerpt, post_status,
            comment_status, ping_status, post_password, post_name,
            to_ping, pinged, post_modified, post_modified_gmt,
            post_content_filtered, post_parent, guid, menu_order,
            post_type, post_mime_type, comment_count
        FROM {wp_db.get_table_name('posts')}
        WHERE post_status = 'publish' 
        AND post_type = 'post'
        AND (post_title LIKE %s OR post_content LIKE %s)
        ORDER BY post_date DESC
        LIMIT %s
    '''
    
    results = wp_db.execute_query(query, (search_pattern, search_pattern, limit))
    posts = []
    
    for row in results:
        post = Post.from_dict(row)
        posts.append(post)
    
    return posts


def main():
    """Главная функция для демонстрации всех возможностей."""
    print('=== Демонстрация работы с моделями WordPress ===')
    
    # Запуск примеров
    print('\n🔹 Операции с постами:')
    example_post_operations()
    
    print('\n🔹 Операции с пользователями:')
    example_user_operations()


if __name__ == '__main__':
    main()