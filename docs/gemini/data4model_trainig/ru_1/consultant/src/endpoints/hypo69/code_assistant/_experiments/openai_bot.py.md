### **Анализ кода модуля `openai_bot.py`**

## \file /src/endpoints/hypo69/code_assistant/_experiments/openai_bot.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура, разделение на функции.
    - Использование `logger` для логирования.
    - Применение `Pathlib` для работы с путями.
    - Использование генератора `yield_files_content` для обработки файлов.
- **Минусы**:
    - Не все переменные аннотированы типами.
    - Жестко заданная роль и другие параметры в коде (не через аргументы командной строки или конфиг).
    - Отсутствует обработка ошибок при чтении файлов.
    - Смешанный стиль комментариев (русский/английский).
    - `time.sleep(20)` без объяснения необходимости.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:

    - Добавить аннотации типов для всех переменных, где это возможно.

2.  **Использовать аргументы командной строки или конфигурационные файлы**:

    - Перенести определение `role`, `openai_model_name`, `openai_assistant_id` в аргументы командной строки или конфигурационные файлы для большей гибкости.

3.  **Обработка ошибок при чтении файлов**:

    - Добавить обработку исключений при чтении файлов в функции `yield_files_content`.

4.  **Унифицировать стиль комментариев**:

    - Перевести все комментарии и docstring на русский язык.

5.  **Удалить неиспользуемые импорты**:

    - Проверить и удалить неиспользуемые импорты, чтобы уменьшить размер кода.

6.  **Улучшить обработку исключений**:

    - В `main()` конкретизировать исключения и добавить более информативные сообщения в `logger.error()`.

7.  **Заменить `time.sleep()` на более гибкое решение**:
    -  Использовать более подходящие механизмы контроля скорости выполнения, например, `asyncio.sleep()` для асинхронного кода или `RateLimiter` из библиотеки `limits`.
 
8. **Использовать `j_loads` или `j_loads_ns` для чтения файлов конфигурации**:
   - Заменить `read_text_file` + `json.load` на `j_loads` или `j_loads_ns` для чтения JSON или конфигурационных файлов.
   

**Оптимизированный код:**

```python
## \file /src/endpoints/hypo69/code_assistant/_experiments/openai_bot.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для экспериментов с моделью AI OpenAI
=================================================

Модуль обрабатывает исходный код или документацию, отправляет его в модель для анализа и получения ответов.

Процесс работы:
----------------

1. Модуль использует роль выполнения, установленную внутри кода, для взаимодействия с моделью.
2. Для роли `doc_writer` используется модель **OpenAI GPT-4** для генерации документации или других текстов.
3. Входные данные для модели включают комментарии и код/документацию, которые передаются в модель для обработки.
4. Ответ модели сохраняется в файл с расширением `.md` в зависимости от роли.

Используемая модель:
--------------------

- **OpenAI GPT-4**: Используется для создания документации и других текстовых материалов.

Ссылки на документацию модели:
------------------------------

- OpenAI: https://platform.openai.com/docs
"""

import re
import time
from pathlib import Path
from typing import Iterator, List, Tuple

from src import gs
from src.ai.openai import OpenAIModel
from src.utils.file import read_text_file
from src.logger.logger import logger

# Глобальная переменная для роли
role: str = 'doc_writer'  # Устанавливаем роль напрямую внутри кода

openai_model_name: str = 'gpt-4o-mini'
openai_assistant_id: str = gs.credentials.openai.assistant_id.code_assistant
openai_model: OpenAIModel


def main() -> None:
    """
    Главная функция для обработки файлов и взаимодействия с моделью.

    Эта функция считывает файл с комментарием, перебирает указанные файлы в исходном каталоге
    и отправляет содержимое файла в модель для анализа. Затем она обрабатывает ответ модели.
    """
    global role

    role = role if role else 'doc_writer'

    if role == 'doc_writer':
        comment_for_model_about_piece_of_code: str = 'doc_writer.md'
        system_instruction: str = 'create_documentation.md'

    # Считываем комментарий для модели из файла markdown
    comment_for_model_about_piece_of_code = read_text_file(
        gs.path.src / 'endpoints' / 'hypo69' / 'onela_bot' / 'instructions' / comment_for_model_about_piece_of_code
    )
    system_instruction = read_text_file(gs.path.src / "ai" / "prompts" / "developer" / system_instruction)

    openai_model = OpenAIModel(
        system_instruction=system_instruction,
        model_name=openai_model_name,
        assistant_id=openai_assistant_id
    )

    # Обрабатываем каждый файл на основе указанных паттернов
    for file_path, content in yield_files_content(
        gs.path.src, ['*.py', 'README.MD']
    ):
        # Формируем входной контент для модели
        content = (
            f"{comment_for_model_about_piece_of_code}\n"
            f"Расположение файла в проекте: `{file_path}`.\n"
            f"Роль выполнения: `{role}`.\n"
            "Код:\n\n"
            f"```{content}```\n"
        )
        try:
            # Получаем ответ от модели
            openai_response = openai_model.ask(content)

            # Сохраняем ответ модели, меняя суффикс файла на `.md`
            save_response(file_path=file_path, response=openai_response, from_model='openai')
        except Exception as ex:
            logger.error('Ошибка при взаимодействии с OpenAI', ex, exc_info=True)
            # Optional: handle error more gracefully
        # Optional sleep to prevent API rate limits or throttling
        time.sleep(20)


def save_response(file_path: Path, response: str, from_model: str) -> None:
    """
    Сохраняет ответ модели в markdown-файл с обновленным путем на основе роли.

    Args:
        file_path (Path): Исходный путь к обрабатываемому файлу.
        response (str): Ответ от модели для сохранения.
        from_model (str): От какой модели получен ответ.
    """
    global role

    # Словарь, ассоциирующий роли с директориями
    role_directories: dict[str, str] = {
        'doc_writer': f'docs/{from_model}/raw_rst_from_ai',
    }

    # Проверка наличия роли в словаре
    if role not in role_directories:
        logger.error(f"Неизвестная роль: {role}. Файл не будет сохранен.")
        return

    # Получаем директорию, соответствующую роли
    role_directory: str = role_directories[role]

    # Формируем новый путь с учетом роли
    export_file_path: tuple = file_path.parts
    new_parts: list = []

    for part in export_file_path:
        if part == 'src':
            new_parts.append(role_directory)
        else:
            new_parts.append(part)

    # Сформировать новый путь с замененной частью
    export_file_path = Path(*new_parts)

    # Изменить суффикс файла на .md
    export_file_path = export_file_path.with_suffix(".md")

    # Убедиться, что директория существует
    export_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохранить ответ в новый файл
    export_file_path.write_text(response, encoding="utf-8")
    print(f"Response saved to: {export_file_path}")


def yield_files_content(
    src_path: Path, patterns: list[str]
) -> Iterator[Tuple[Path, str]]:
    """
    Извлекает содержимое файлов на основе паттернов из исходного каталога, исключая определенные паттерны и каталоги.

    Args:
        src_path (Path): Базовый каталог для поиска файлов.
        patterns (list[str]): Список паттернов файлов для включения (например, ['*.py', '*.txt']).

    Yields:
        Iterator[tuple[Path, str]]: Кортеж из пути к файлу и его содержимого в виде строки.
    """

    # Регулярные выражения для исключаемых файлов и директорий
    exclude_file_patterns: list[re.Pattern] = [
        re.compile(r'.*\\(.*\\).*\'),  # Файлы и директории, содержащие круглые скобки
        re.compile(r'___+.*\'),      # Файлы или директории, начинающиеся с трех и более подчеркиваний
    ]

    # Список служебных директорий, которые необходимо исключить
    exclude_dirs: set[str] = {'.ipynb_checkpoints', '_experiments', '__pycache__', '.git', '.venv'}

    for pattern in patterns:
        for file_path in src_path.rglob(pattern):
            # Пропустить файлы, которые находятся в исключаемых директориях
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue

            # Пропустить файлы, соответствующие исключаемым паттернам
            if any(exclude.match(str(file_path)) for exclude in exclude_file_patterns):
                continue

            try:
                # Чтение содержимого файла
                content: str = file_path.read_text(encoding="utf-8")
                yield file_path, content
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла {file_path}', ex, exc_info=True)


if __name__ == "__main__":
    print("Starting training ...")
    main()