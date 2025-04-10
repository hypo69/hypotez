### **Анализ кода модуля `openai_bot.py`**

## \file /src/endpoints/hypo69/code_assistant/_experiments/openai_bot.py

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование аннотаций типов.
    - Четкое разделение на функции.
    - Использование `logger` для логирования.
- **Минусы**:
    - Отсутствие docstring у некоторых функций и переменных.
    - Использование глобальных переменных.
    - Жестко заданные пути к файлам.
    - Смешанный стиль кавычек (использованы как одинарные, так и двойные).
    - Использование неявных путей к файлам внутри кода (вместо использования os.path или pathlib).
    - Docstring'и есть, но они на английском языке. Необходимо перевести на русский и привести в соответствие со стандартом оформления.

**Рекомендации по улучшению:**

1.  **Документация**:
    - Добавить docstring для всех функций, переменных и классов, включая описание параметров, возвращаемых значений и возможных исключений.
    - Перевести существующие docstring на русский язык и привести их в соответствие со стандартом оформления.

2.  **Глобальные переменные**:
    - Избегать использования глобальных переменных, таких как `role`. Вместо этого передавать их как аргументы в функции.
    - Сделать `openai_model` локальной переменной в `main` или передавать как аргумент.

3.  **Пути к файлам**:
    - Использовать `os.path` или `pathlib` для построения путей к файлам, чтобы обеспечить кроссплатформенность.
    - Вынести пути к файлам в переменные окружения или параметры конфигурации.

4.  **Обработка исключений**:
    - Указывать конкретные типы исключений вместо `Exception`.
    - Добавить обработку исключений для чтения файлов и сетевых запросов.
    - Логировать исключения с использованием `logger.error` и передавать `ex` в качестве аргумента.

5.  **Форматирование**:
    - Привести все кавычки к одному стилю (одинарные).
    - Добавить пробелы вокруг операторов присваивания.

6. **Комментарии**:
    - Добавить комментарии к сложным участкам кода.
    - Уточнить существующие комментарии, избегая расплывчатых формулировок.
7. **Сохранение ответа**
    - Пересмотреть логику формирования путей, чтобы сделать её более гибкой и понятной.
    - Использовать `os.path.join` или `pathlib` для создания путей.
8. **Прочее**
    - Для `exclude_file_patterns` добавить описание, что это за паттерны и для чего они нужны.
    - Убрать неиспользуемые импорты.
    - Переименовать переменную `comment_for_model_about_piece_of_code` на более короткое и понятное имя.

**Оптимизированный код:**

```python
## \file /src/endpoints/hypo69/code_assistant/_experiments/openai_bot.py
# -*- coding: utf-8 -*-

"""
Модуль для экспериментов с моделью AI OpenAI
=================================================

Модуль предназначен для обработки исходного кода или документации, отправки его в модель OpenAI для анализа и получения ответов.

Процесс работы:
1.  Модуль использует роль выполнения, установленную для взаимодействия с моделью.
2.  Для роли `doc_writer` используется модель **OpenAI GPT-4** для генерации документации или других текстов.
3.  Входные данные для модели включают комментарии и код/документацию.
4.  Ответ модели сохраняется в файл с расширением `.md` в зависимости от роли.

Используемая модель:
-   **OpenAI GPT-4**: Используется для создания документации и других текстовых материалов.

Ссылки на документацию модели:
-   OpenAI: https://platform.openai.com/docs

Пример использования
----------------------

>>> from src.endpoints.hypo69.code_assistant._experiments.openai_bot import main
>>> main()
"""

import re
import time
from pathlib import Path
from typing import Iterator, List, Tuple

from src import gs
from src.ai.openai import OpenAIModel
from src.utils.file import yield_files_content
from src.utils.file import read_text_file
from src.logger.logger import logger

# Устанавливаем роль по умолчанию
DEFAULT_ROLE: str = 'doc_writer'

# Имя модели OpenAI по умолчанию
DEFAULT_OPENAI_MODEL_NAME: str = 'gpt-4o-mini'


def main(role: str = DEFAULT_ROLE) -> None:
    """
    Основная функция для обработки файлов и взаимодействия с моделью.

    Считывает файл с комментариями, перебирает указанные файлы в исходном каталоге
    и отправляет содержимое файла в модель для анализа. Затем обрабатывает ответ модели.

    Args:
        role (str, optional): Роль для обработки файлов. По умолчанию 'doc_writer'.
    """
    try:
        # Определяем переменные в зависимости от роли
        if role == 'doc_writer':
            comment_file_name: str = 'doc_writer.md'
            system_instruction_file: str = 'create_documentation.md'
        else:
            logger.error(f'Неизвестная роль: {role}')
            return

        # Читаем комментарий для модели из markdown файла
        comment_for_model: str | None = read_text_file(
            gs.path.src / 'endpoints' / 'hypo69' / 'onela_bot' / 'instructions' / comment_file_name
        )

        # Читаем системные инструкции для модели из markdown файла
        system_instruction: str | None = read_text_file(
            gs.path.src / 'ai' / 'prompts' / 'developer' / system_instruction_file
        )

        if not comment_for_model or not system_instruction:
            logger.error('Не удалось прочитать файлы с комментариями или системными инструкциями')
            return

        # Инициализируем модель OpenAI
        openai_model: OpenAIModel = OpenAIModel(
            system_instruction=system_instruction,
            model_name=DEFAULT_OPENAI_MODEL_NAME,
            assistant_id=gs.credentials.openai.assistant_id.code_assistant
        )

        # Обрабатываем каждый файл на основе указанных паттернов
        for file_path, content in yield_files_content(
            gs.path.src, ['*.py', 'README.MD']
        ):
            # Формируем входные данные для модели
            content: str = (
                f'{comment_for_model}\n'
                f'Расположение файла в проекте: `{file_path}`.\n'
                f'Роль выполнения: `{role}`.\n'
                'Код:\n\n'
                f'```{content}```\n'
            )

            try:
                # Получаем ответ от модели
                openai_response: str = openai_model.ask(content)

                # Сохраняем ответ модели, изменяя суффикс файла на `.md`
                save_response(
                    file_path=file_path, response=openai_response, from_model='openai', role=role
                )

            except Exception as ex:
                logger.error('Ошибка при обработке файла', ex, exc_info=True)

            # Необязательная задержка для предотвращения ограничений API
            time.sleep(20)

    except Exception as ex:
        logger.error('Общая ошибка в main', ex, exc_info=True)


def save_response(file_path: Path, response: str, from_model: str, role: str) -> None:
    """
    Сохраняет ответ модели в markdown файл с обновленным путем на основе роли.

    Args:
        file_path (Path): Исходный путь к обрабатываемому файлу.
        response (str): Ответ от модели, который нужно сохранить.
        from_model (str): Имя модели, от которой получен ответ.
        role (str): Роль, определяющая директорию сохранения.
    """
    # Словарь, связывающий роли с директориями
    role_directories: dict[str, str] = {
        'doc_writer': f'docs/{from_model}/raw_rst_from_ai',
    }

    # Проверяем наличие роли в словаре
    if role not in role_directories:
        logger.error(f'Неизвестная роль: {role}. Файл не будет сохранен.')
        return

    # Получаем директорию, соответствующую роли
    role_directory: str = role_directories[role]

    # Формируем новый путь с учетом роли
    export_file_path_parts: Tuple[str, ...] = file_path.parts
    new_parts: List[str] = []

    for part in export_file_path_parts:
        if part == 'src':
            new_parts.append(role_directory)
        else:
            new_parts.append(part)

    # Формируем новый путь с замененной частью
    export_file_path: Path = Path(*new_parts)

    # Изменяем суффикс файла на .md
    export_file_path: Path = export_file_path.with_suffix('.md')

    # Убеждаемся, что директория существует
    export_file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Сохраняем ответ в новый файл
        export_file_path.write_text(response, encoding='utf-8')
        print(f'Response saved to: {export_file_path}')
    except Exception as ex:
        logger.error(f'Ошибка при записи в файл {export_file_path}', ex, exc_info=True)


def yield_files_content(
    src_path: Path, patterns: list[str]
) -> Iterator[tuple[Path, str]]:
    """
    Перебирает содержимое файлов на основе паттернов из исходного каталога, исключая определенные паттерны и директории.

    Args:
        src_path (Path): Базовый каталог для поиска файлов.
        patterns (list[str]): Список файловых паттернов для включения (например, ['*.py', '*.txt']).

    Yields:
        Iterator[tuple[Path, str]]: Кортеж из пути к файлу и его содержимого в виде строки.
    """

    # Регулярные выражения для исключаемых файлов и директорий
    exclude_file_patterns: list[re.Pattern[str]] = [
        re.compile(r'.*\\(.*\\).*'),  # Файлы и директории, содержащие круглые скобки
        re.compile(r'___+.*'),  # Файлы или директории, начинающиеся с трех и более подчеркиваний
    ]

    # Список служебных директорий, которые необходимо исключить
    exclude_dirs: set[str] = {'.ipynb_checkpoints', '_experiments', '__pycache__', '.git', '.venv'}

    for pattern in patterns:
        for file_path in src_path.rglob(pattern):
            # Пропускаем файлы, которые находятся в исключаемых директориях
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue

            # Пропускаем файлы, соответствующие исключаемым паттернам
            if any(exclude.match(str(file_path)) for exclude in exclude_file_patterns):
                continue

            try:
                # Читаем содержимое файла
                content: str = file_path.read_text(encoding='utf-8')
                yield file_path, content
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла {file_path}', ex, exc_info=True)


if __name__ == '__main__':
    print('Starting training ...')
    main()