### Анализ кода модуля `openai_bot.py`

**Качество кода:**
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Присутствует основная структура модуля для взаимодействия с OpenAI.
    - Код разбит на функции, что улучшает читаемость.
    - Используется логирование.
- **Минусы**:
    - Не все функции и переменные аннотированы типами.
    - Отсутствует docstring для многих функций и классов.
    - Используется глобальная переменная `role`.
    - Смешаны стили кавычек (используются и двойные, и одинарные).
    - В блоках `except` используется `e` вместо `ex`.
    - В начале файла много пустых docstring.
    - Не хватает подробных комментариев.
    - Использование `print` вместо `logger.info` для логирования в `if __name__ == "__main__":`.

**Рекомендации по улучшению:**

1. **Документирование кода**:
   - Добавить docstring к каждой функции, классу и методу, следуя указанному формату.
   - Описать назначение каждой функции, входные параметры, возвращаемые значения и возможные исключения.
   - Добавить примеры использования.

2. **Аннотации типов**:
   - Указать типы для всех переменных и параметров функций.
   - Использовать `Optional` и `Union` (или `|`) для обозначения возможных типов.

3. **Использование `logger`**:
   - Заменить `print` на `logger.info` для всех информационных сообщений.
   - В блоках `except` использовать `logger.error` с передачей исключения `ex` и `exc_info=True`.

4. **Глобальные переменные**:
   - Избегать использования глобальных переменных. Если необходимо, рассмотреть использование классов или контекстных менеджеров.

5. **Форматирование кода**:
   - Использовать только одинарные кавычки.
   - Добавить пробелы вокруг операторов присваивания.
   - Следовать стандартам PEP8.

6. **Улучшение обработки исключений**:
   - В блоках `except` использовать `ex` вместо `e`.
   - Добавить более детальную обработку исключений, чтобы предотвратить падения программы.

7. **Рефакторинг структуры**:
   - Рассмотреть возможность использования классов для организации кода.
   - Улучшить читаемость кода, разбив сложные функции на более простые.

8. **Удаление лишнего**:
   - Убрать пустые docstring в начале файла.

**Оптимизированный код:**

```python
"""
Модуль для экспериментов с моделью AI OpenAI.
=================================================

Модуль предназначен для обработки исходного кода или документации,
отправки его в модель OpenAI для анализа и получения ответов.

Процесс работы:
1. Модуль использует роль выполнения, установленную внутри кода, для взаимодействия с моделью.
2. Для роли `doc_writer` используется модель **OpenAI GPT-4** для генерации документации или других текстов.
3. Входные данные для модели включают комментарии и код/документацию, которые передаются в модель для обработки.
4. Ответ модели сохраняется в файл с расширением `.md` в зависимости от роли.

Используемая модель:
- **OpenAI GPT-4**: Используется для создания документации и других текстовых материалов.

Ссылки на документацию модели:
- OpenAI: https://platform.openai.com/docs
"""

import re
import time
from pathlib import Path
from typing import Iterator, Tuple, List

from src import gs
from src.ai.openai import OpenAIModel
from src.utils.file import yield_files_content as _yield_files_content, read_text_file
from src.logger.logger import logger


# Устанавливаем роль по умолчанию
DEFAULT_ROLE: str = 'doc_writer'

openai_model_name: str = 'gpt-4o-mini'
openai_assistant_id: str = gs.credentials.openai.assistant_id.code_assistant
openai_model: OpenAIModel


def main(role: str = DEFAULT_ROLE) -> None:
    """
    Основная функция для обработки файлов и взаимодействия с моделью OpenAI.

    Args:
        role (str, optional): Роль, определяющая режим работы. По умолчанию 'doc_writer'.

    Raises:
        Exception: Если возникает ошибка в процессе обработки.
    """
    try:
        if role == 'doc_writer':
            comment_file: str = 'doc_writer.md'
            system_instruction_file: str = 'create_documentation.md'

        # Чтение комментариев для модели из markdown-файла
        comment_for_model: str | None = read_text_file(
            gs.path.src / 'endpoints' / 'hypo69' / 'onela_bot' / 'instructions' / comment_file
        )
        system_instruction: str | None = read_text_file(gs.path.src / "ai" / "prompts" / "developer" / system_instruction_file)

        if not comment_for_model or not system_instruction:
            logger.error('Не удалось прочитать файлы комментариев или системных инструкций.')
            return

        openai_model: OpenAIModel = OpenAIModel(
            system_instruction=system_instruction,
            model_name=openai_model_name,
            assistant_id=openai_assistant_id
        )

        # Обработка каждого файла на основе указанных шаблонов
        for file_path, content in yield_files_content(gs.path.src, ['*.py', 'README.MD']):
            # Формирование входных данных для модели
            content = (
                f"{comment_for_model}\n"
                f"Расположение файла в проекте: `{file_path}`.\n"
                f"Роль выполнения: `{role}`.\n"
                "Код:\n\n"
                f"```{content}```\n"
            )
            try:
                # Получение ответа от модели
                openai_response: str = openai_model.ask(content)

                # Сохранение ответа модели, изменяя суффикс файла на `.md`
                save_response(file_path=file_path, response=openai_response, from_model='openai', role=role)
            except Exception as ex:
                logger.error('Ошибка при взаимодействии с моделью OpenAI', ex, exc_info=True)

            # Небольшая задержка для предотвращения превышения лимитов API
            time.sleep(20)

    except Exception as ex:
        logger.error('Общая ошибка в main', ex, exc_info=True)


def save_response(file_path: Path, response: str, from_model: str, role: str) -> None:
    """
    Сохраняет ответ модели в markdown-файл с обновленным путем на основе роли.

    Args:
        file_path (Path): Исходный путь к обрабатываемому файлу.
        response (str): Ответ от модели, который необходимо сохранить.
        from_model (str): Название модели, от которой получен ответ.
        role (str): Роль, определяющая директорию сохранения.
    """
    # Словарь, связывающий роли с директориями
    role_directories: dict[str, str] = {
        'doc_writer': f'docs/{from_model}/raw_rst_from_ai',
    }

    # Проверка наличия роли в словаре
    if role not in role_directories:
        logger.error(f'Неизвестная роль: {role}. Файл не будет сохранен.')
        return

    # Получение директории, соответствующей роли
    role_directory: str = role_directories[role]

    # Формирование нового пути с учетом роли
    export_file_path_parts: Tuple[str, ...] = file_path.parts
    new_parts: List[str] = []

    for part in export_file_path_parts:
        if part == 'src':
            new_parts.append(role_directory)
        else:
            new_parts.append(part)

    # Сформировать новый путь с замененной частью
    export_file_path: Path = Path(*new_parts)

    # Изменить суффикс файла на .md
    export_file_path = export_file_path.with_suffix('.md')

    # Убедиться, что директория существует
    export_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохранить ответ в новый файл
    try:
        export_file_path.write_text(response, encoding='utf-8')
        logger.info(f'Response saved to: {export_file_path}')
    except Exception as ex:
        logger.error(f'Ошибка при записи файла {export_file_path}', ex, exc_info=True)


def yield_files_content(
    src_path: Path, patterns: List[str]
) -> Iterator[Tuple[Path, str]]:
    """
    Предоставляет содержимое файлов на основе шаблонов из исходной директории, исключая определенные шаблоны и директории.

    Args:
        src_path (Path): Базовая директория для поиска файлов.
        patterns (List[str]): Список шаблонов файлов для включения (например, ['*.py', '*.txt']).

    Yields:
        Iterator[Tuple[Path, str]]: Кортеж, содержащий путь к файлу и его содержимое в виде строки.
    """

    # Регулярные выражения для исключаемых файлов и директорий
    exclude_file_patterns = [
        re.compile(r'.*\\(.*\\).*\'),  # Файлы и директории, содержащие круглые скобки
        re.compile(r'___+.*\'),      # Файлы или директории, начинающиеся с трех и более подчеркиваний
    ]

    # Список служебных директорий, которые необходимо исключить
    exclude_dirs = {'.ipynb_checkpoints', '_experiments', '__pycache__', '.git', '.venv'}

    for pattern in patterns:
        for file_path in src_path.rglob(pattern):
            # Пропустить файлы, которые находятся в исключаемых директориях
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue

            # Пропустить файлы, соответствующие исключаемым паттернам
            if any(exclude.match(str(file_path)) for exclude in exclude_file_patterns):
                continue

            # Чтение содержимого файла
            try:
                content: str = file_path.read_text(encoding='utf-8')
                yield file_path, content
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла {file_path}', ex, exc_info=True)


if __name__ == "__main__":
    logger.info('Starting training ...')
    main()