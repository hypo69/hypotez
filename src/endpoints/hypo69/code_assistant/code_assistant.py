
## \file /src/endpoints/hypo69/code_assistant/code_assistant.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль обучения модели машинного обучения кодовой базе, составления документации к проекту, примеров кода и тестов
=========================================================================================

:class:`CodeAssistant`, читает файлы кода, отдает код в модели, модель обрабатывет код и возвращает его в класс, класс сохраняет результат
в директории `docs/gemini` В зависимости от роли файлы сохраняются в 

Пример использования
--------------------

Пример использования класса `CodeAssistant`:
# задайте роль исполнителя, язык 
```python

    assistant = CodeAssistant(role='code_checker', lang='ru', model=['gemini'])
    assistant.process_files()
```

.. header.py:
    ```mermaid
    flowchart TD
        Start --> Header[<code>header.py</code><br> Determine Project Root]
    
        Header --> import[Import Global Settings: <br><code>from src import gs</code>] 
    ```

[Документация](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/endpoints/hypo69/code_assistant/code_assistant.py.md)
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from typing import Iterator, List, Optional
from types import SimpleNamespace
import signal
import time
import re
import fnmatch

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads, j_loads_ns
from src.llm.gemini import GoogleGenerativeAi
from src.llm.openai import OpenAIModel
from src.utils.printer import pprint as print
from src.utils.path import get_relative_path
from src.logger.logger import logger
from src import USE_ENV

# -------------------------- file config.py ----------------------------------

class Config:
    ...
    ENDPOINT: Path = __root__ / 'src' / 'endpoints' / 'hypo69' / 'code_assistant'   
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'code_assistant.json')
    roles_list:list = config.roles
    languages_list:list = config.languages
    role: str = 'doc_writer_md'
    lang: str = 'ru'
    process_dirs:list[Path] = config.process_dirs
    exclude_dirs:list[Path] = config.exclude_dirs
    exclude_files_patterns:list[Path] = config.exclude_files_patterns
    include_files_patterns:list[Path] = config.include_files_patterns
    exclude_files:list[Path] = config.exclude_files
    exclude_dirs:list[Path] = config.exclude_dirs
    response_mime_type:str = config.response_mime_type 
    output_dir: str | Path = ''
    output_directory_patterns:list = config.output_dirs
    remove_prefixes:str = config.remove_prefixes
    model_name:str = config.model_name

    @classmethod
    @property
    def code_instruction(self):
        """code_instruction - Инструкция для кода.
        При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету"
        """
        try:
            return Path( Config.ENDPOINT / 'instructions'/ f'instruction_{Config.role}_{Config.lang}.md'
                ).read_text(encoding='UTF-8')

        except Exception as ex:
            return ''

    @classmethod
    @property
    def system_instruction(self):
        """Инструкция для модели.
        При каждом вызове читает файл с инструкцией, что позволяет обновлять инструкции "на лету
        """
        try:
            return Path(Config.ENDPOINT / 'instructions' / f'CODE_RULES.{Config.lang}.MD'
                                ).read_text(encoding='UTF-8')
        except Exception as ex:
            return ''


    gemini: SimpleNamespace = SimpleNamespace(**{
        'model_name': os.getenv('GEMINI_MODEL') if USE_ENV else config.model_name or None, 
        'api_key': os.getenv('GEMINI_API_KEY') if USE_ENV else gs.credentials.gemini.onela.api_key or None, 
        'response_mime_type': 'text/plain',
    })

# -------------------------- end config.py---------------------------------------------------



class CodeAssistant:
    """Класс для работы ассистента программиста с моделями ИИ"""

    role: str = ''
    lang: str = ''
    system_instruction:str = ''
    code_instruction:str = ''
    gemini: 'GoogleGenerativeAi'
    openai: 'OpenAIModel'

    def __init__(
        self,
        role: Optional[str] = 'doc_writer_md',
        lang: Optional[str] = 'en',
        model_name:Optional[str] = '',
        system_instruction: Optional[str | Path] = None,
        **kwargs,
    ) -> None:
        """
        Инициализация ассистента с заданными параметрами.

        Args:
            role (str): Роль для выполнения задачи.
            lang (str): Язык выполнения.
            models_list (list[str]): Список моделей для инициализации.
            system_instruction (str|Path): Общая инструкция для модели. 
            **kwargs: Дополнительные аргументы для инициализации моделей.
        """
        self.role = role or Config.role
        self.lang = lang or Config.lang
        self.system_instruction = system_instruction or Config.system_instruction

        filtered_kwargs = {
                    k: v
                    for k, v in kwargs.items()
                    if k not in ('model_name', 'api_key', 'generation_config', 'system_instruction') # <- оставляю только то, что нужно модели
                }
        self.gemini = GoogleGenerativeAi(     
                model_name = model_name or Config.gemini.model_name,
                api_key=kwargs.get('api_key', Config.gemini.api_key),# Значение из kwargs имеет приоритет,
                system_instruction= system_instruction or Config.system_instruction,
                generation_config = {'response_mime_type': kwargs.get( 'response_mime_type',  Config.response_mime_type)},
                **filtered_kwargs,
            )
        ...


  

    def send_file(self, file_path: Path) -> Optional[str | None]:
        """
        Отправка файла в модель.

        Args:
            file_path (Path): Абсолютный путь к файлу, который нужно отправить.
            file_name (Optional[str]): Имя файла для отправки. Если не указано и 'src' отсутствует, используется имя файла без изменений.

        Returns:
            Optional[str | None]: URL файла, если успешно отправлен, иначе None.
        """
        try:
            # Отправка файла в модель
            response:str = self.gemini.upload_file(file_path)

            if response:
                if hasattr(response, 'url'):
                    return response.url

                ...
                return ''
        except Exception as ex:
            logger.error('Ошибка при отправке файла: ', ex)
            ...
            return ''
      
    # --- вспомогательные функции ---

    def _yield_files_content(
        self,
        process_directory: str | Path,
    ) -> Iterator[tuple[Path, str]]:
        """
        Генерирует пути файлов и их содержимое по указанным шаблонам.

        Args:
            process_directory (Path | str): Абсолютный путь к стартовой директории

        Returns:
            bool: Iterator
        """

        process_directory: Path = process_directory if isinstance(process_directory, Path) else Path(process_directory)

        # Компиляция паттернов исключаемых файлов
        try:
            exclude_files_patterns = [
                re.compile(pattern) for pattern in Config.exclude_files_patterns
            ]

        except Exception as ex:
            logger.error(
                f'Не удалось скомпилировать регулярки из списка:/n{Config.exclude_files_patterns=}\n ', ex
            )
            ...

        # Итерация по всем файлам в директории
        for file_path in process_directory.rglob('*'):
            # Проверка на соответствие шаблонам включения
            if not any(
                fnmatch.fnmatch(file_path.name, pattern) for pattern in Config.include_files_patterns
            ):
                continue

            # Прверка исключенных директорий
            if any(exclude_dir in file_path.parts for exclude_dir in Config.exclude_dirs):
                continue

            # Проверка исключенных файлов по паттерну
            if any(exclude.match(str(file_path.name)) for exclude in exclude_files_patterns):
                continue

            # Проверка конкретных исключенных файлов
            if str(file_path.name) in Config.exclude_files:
                continue

            # Чтение содержимого файла
            try:
                content = file_path.read_text(encoding='utf-8')
                yield file_path, content
                # make_summary( docs_dir = start_dir.parent / 'docs' )  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG  (create `summary.md`)
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла {file_path}', ex)
                ...
                yield None, None

            ...


    def _create_request(self, file_path: str, content: str, ) -> str:
        """Создание запроса с учетом роли и языка."""
        
        try:
            content_request: dict = {
                'role': self.role,
                'output_language': self.lang,
                f'file_location_in_project_hypotez': get_relative_path(file_path, 'hypotez'),
                'instruction': self.code_instruction or '',
                'input_code': f"""```python
                {content}
                ```""",
            } 
            return str(content_request)

        except Exception as ex:
            logger.error(f'Ошибка в составлении запроса ', ex, False)
            ...
            return str(content)


    def _remove_outer_quotes(self, response: str) -> str:
            """
            Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.

            Args:
                response (str): Ответ модели, который необходимо обработать.

            Returns:
                str: Очищенный контент как строка.

            Example:
                >>> _remove_outer_quotes('```md some content ```')
                'some content'
                >>> _remove_outer_quotes('some content')
                'some content'
                >>> _remove_outer_quotes('```python def hello(): print("Hello") ```')
                '```python def hello(): print("Hello") ```'
            """
            try:
                response = response.strip()
            except Exception as ex:
                logger.error('Exception in `_remove_outer_quotes()`', ex, False)
                return ''

            # Если строка начинается с '```python' или '```mermaid', возвращаем её без изменений. Это годный код
            if response.startswith(('```python', '```mermaid')):
                return response


            for prefix in Config.remove_prefixes:
                # Сравнение с префиксом без учёта регистра
                if response.lower().startswith(prefix.lower()):
                    # Удаляем префикс и суффикс "```", если он есть
                    cleaned_response = response[len(prefix) :].strip()
                    if cleaned_response.endswith('```'):
                        cleaned_response = cleaned_response[: -len('```')].strip()
                    return cleaned_response

            # Возврат строки без изменений, если условия не выполнены
            return response

    async def _save_response(self, file_path: str|Path, output_dir: str|Path,  relative_to: str, response: str, model_name: str = 'gemini', ) -> bool:
        """
        Сохранение ответа модели в файл с добавлением суффикса.

        Метод сохраняет ответ модели в файл, добавляя к текущему расширению файла
        дополнительный суффикс, определяемый ролью.

        Args:
            file_path (Path): Исходный путь к файлу, в который будет записан ответ.
            response (str): Ответ модели, который необходимо сохранить.
            model_name (str): Имя модели, использованной для генерации ответа.

        Raises:
            OSError: Если не удаётся создать директорию или записать в файл.
        """
        export_path:Path = None
        relative_path:Path = None
        try:
            # Получение директории  в зависимости от роли
            _pattern:str = getattr(Config.output_directory_patterns, Config.role, '')

            for i, part in enumerate(file_path.parts):
                if part == relative_to:
                    relative_path = Path(*file_path.parts[i+1:])
                    break

            # Формирование целевой директории с учётом подстановки параметров <model> и <lang>
            target_dir: str = (
                f'docs/{_pattern}'
                .replace('<lang>', self.lang)
                .replace('<module>', str(relative_path))
                )



            # суффикс в зависимости от роли
            suffix_map = {
                'traslator':'',
                'code_checker': '.md',
                'doc_writer_md': '.md',
                'doc_writer_rst': '.rst',
                'doc_writer_html': '.html',
                'code_explainer_md': '.md',
                'code_explainer_html': '.html',
                'pytest': '.md',
            }
            suffix = suffix_map.get(self.role, '')

            #export_path:Path = Path(output_dir / f'{target_dir}{suffix}')  # Полный путь к конеччому файлу документации
            export_path:Path = Path(output_dir / relative_path) # <- без создания дополнительных поддиректорий 
            export_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                export_path.write_text(response, encoding='utf-8')
                logger.success(f'Файл сохранён В:\n{export_path}')
                return True
            except Exception as e:
                logger.error(f'Файл не сохранился по адресу:\n{export_path}\nОшибка: {e}')
                return False


        except Exception as ex:
            logger.critical(f'Ошибка сохранения файла:\n{file_path=}', ex, False)
            ...
            return False

    # --------

    async def process_files(
        self, 
        process_dirs: Optional[str | Path | list[str | Path]], 
        output_dir: Optional[str | Path | list[str | Path]],
        relative_to:str
    ) -> bool:
        """компиляция, отправка запроса и сохранение результата.
        Args:
            process_dirs(str|Path|list[str|Path]): путь к исходным файлам. Путь должен вести к директории/ям, не к файлу
            output_dir(str): путь конечной директории
            relative_to(str): имя директории, откуда будет достраиваться путь к файлу в `output_dir`

        """
        process_dirs = process_dirs if isinstance(process_dirs, list) else [process_dirs]
        for process_directory in process_dirs:

            process_directory:Path = Path(process_directory)

            if not process_directory.exists():
                logger.error(f"Директория не существует: {process_directory}")
                continue  # Переход к следующей директории, если текущая не существует

            if not process_directory.is_dir():
                logger.error(f"Это не директория: {process_directory}", None, False)
                continue  # Переход к следующей директории, если текущая не является директорией

            logger.info(f'Start {process_directory=}')

            for i, (file_path, content) in enumerate( self._yield_files_content(process_directory) ):
                if not any((file_path, content)):  # <- ошибка чтения файла
                    logger.error(f'Ошибка чтения содержимого файла {file_path}\nContent {content} ')
                    continue

                if file_path and content:
                    logger.debug(f'Чтение файла номер: {i+1}\n{file_path}', None, False)
                    #в случае переводчика дополнительные параметры к запросу не нужны
                    content_request:str = content if self.role == 'translator' else self._create_request(file_path, content)
                    response:str = await self.gemini.ask_async(content_request) 
                    #response:str = await self.gemini.chat(content_request,'coder') # <- чат (не проверен)

                    if response:
                        response: str = self._remove_outer_quotes(response)
                        if Config.role == 'trainer': # трениривка модели, Результат не сохараням
                            print(response, text_color = 'yellow')
                        elif not await self._save_response(file_path, output_dir, relative_to, response, ):
                                    logger.error(f'Файл {file_path} \n НЕ сохранился')
                                    ...
                                    continue
                    else:
                        logger.error('Ошибка ответа модели', None, False)
                        ...
                        continue

                await asyncio.sleep(20)  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG (change timeout)


  
    def run(self, start_from_file: int = 1) -> None:
        """Запуск процесса обработки файлов."""
        signal.signal(signal.SIGINT, self._signal_handler)  # Обработка прерывания (Ctrl+C)
        asyncio.run(self.process_files(start_from_file))

    def _signal_handler(self, signal, frame) -> None:
        """Обработка прерывания выполнения."""
        logger.debug('Процесс был прерван', text_color='red')
        sys.exit(0)


def parse_args() -> dict:
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Ассистент для программистов')
    parser.add_argument(
        '--role',
        type=str,
        default='code_checker',
        help='Роль для выполнения задачи',
    )
    parser.add_argument('--lang', type=str, default='ru', help='Язык выполнения')
    parser.add_argument(
        '--model',
        nargs='+',
        type=str,
        default=['gemini'],
        help='Список моделей для инициализации',
    )
    parser.add_argument(
        '--start-dirs',
        nargs='+',
        type=str,
        default=[],
        help='Список директорий для обработки',
    )
    parser.add_argument(
        '--start-file-number',
        type=int,
        default=1,
        help='С какого файла делать обработку. Полезно при сбоях',
    )
    return vars(parser.parse_args())


def main() -> None:
    """
    Функция запускает бесконечный цикл, в котором выполняется обработка файлов с учетом ролей и языков, указанных в конфигурации.
    Конфигурация обновляется в каждом цикле, что позволяет динамически изменять настройки в файле `code_assistant.json` во время работы программы.
    Для каждой комбинации языка и роли создается экземпляр класса :class:`CodeAssistant`, который обрабатывает файлы, используя заданную модель ИИ.
    """


    # --- настройки для переводчика
    Config.roles_list = ['translator']
    Config.languages_list = ['he']
    Config.model_name = 'gemini-2.5-flash-preview-04-17'
    Config.process_dirs = [r'C:\Users\user\Documents\repos\public_repositories\1001-python-ru']
    Config.output_dir = r'C:\Users\user\Documents\repos\public_repositories\1001-python-he'
    relative_to:str = '1001-python-ru'
    Config.system_instruction = (Config.ENDPOINT / 'instructions' / f'DOCUMENT_TRANSLATOR.{Config.languages_list[0]}.MD').read_text(encoding='UTF-8')
    # -----------------------------

    while True:
       
        # Обработка файлов для каждой комбинации языков и ролей
        for lang in Config.languages_list:
            
            for role in Config.roles_list:
                logger.debug(f'Start role: {role}, lang: {lang}', None, False)
                assistant_direct = CodeAssistant(
                    role=role,
                    lang=lang,
                    model_name = Config.model_name,
                    system_instruction = Config.system_instruction,
                )
                asyncio.run(
                    assistant_direct.process_files(Config.process_dirs, Config.output_dir, relative_to)
                    )


if __name__ == '__main__':
    main()