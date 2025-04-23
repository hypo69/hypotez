Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный модуль предназначен для экспериментов с AI моделью OpenAI. Он позволяет обрабатывать исходный код или документацию, отправлять его в модель для анализа и получения ответов. В основном используется для автоматической генерации документации с использованием модели GPT-4.

Шаги выполнения
-------------------------
1. **Установка роли**: Определяется роль выполнения, например `doc_writer`, для указания цели использования модели.
2. **Чтение инструкций**: Из файлов с инструкциями считываются необходимые комментарии и системные инструкции для модели.
3. **Инициализация модели OpenAI**: Создается экземпляр класса `OpenAIModel` с указанием системных инструкций, имени модели и ID ассистента.
4. **Обработка файлов**: Выполняется итерация по файлам, соответствующим заданным шаблонам (например, `*.py`, `README.MD`), из указанной директории (`gs.path.src`).
5. **Формирование контента для модели**: Для каждого файла формируется входной контент, включающий комментарии, расположение файла в проекте, роль выполнения и сам код файла.
6. **Отправка запроса в модель**: Сформированный контент отправляется в модель OpenAI для анализа.
7. **Сохранение ответа**: Ответ модели сохраняется в файл с расширением `.md` в соответствующую директорию, зависящую от роли выполнения (например, `docs/openai/raw_rst_from_ai`).
8. **Обработка ошибок**: В случае возникновения ошибки в процессе обработки файла, она логируется.
9. **Задержка**: После обработки каждого файла выполняется задержка (`time.sleep(20)`) для предотвращения превышения лимитов API или троттлинга.

Пример использования
-------------------------

```python
import re
from pathlib import Path
import time
from typing import Iterator

from src import gs
from src.ai.openai import OpenAIModel
from src.utils.file import yield_files_content, read_text_file
from src.logger.logger import logger

# Устанавливаем роль напрямую внутри кода
role: str = 'doc_writer'

openai_model_name: str = 'gpt-4o-mini'
openai_assistant_id: str = gs.credentials.openai.assistant_id.code_assistant
openai_model: OpenAIModel

def main() -> None:
    """
    Главная функция для обработки файлов и взаимодействия с моделью.

    Эта функция считывает файл комментариев, перебирает указанные файлы в исходном каталоге
    и отправляет содержимое файла в модель для анализа. Затем она обрабатывает ответ модели.
    """
    global role

    role = role if role else 'doc_writer'

    if role == 'doc_writer':
        comment_for_model_about_piece_of_code = 'doc_writer.md'
        system_instruction: str = 'create_documentation.md'

    # Считываем комментарий для ввода модели из файла markdown
    comment_for_model_about_piece_of_code = read_text_file(
        gs.path.src / 'endpoints' / 'hypo69' / 'onela_bot' / 'instructions' / comment_for_model_about_piece_of_code
    )
    system_instruction = read_text_file(gs.path.src / "ai" / "prompts" / "developer" / system_instruction)

    openai_model = OpenAIModel(
        system_instruction=system_instruction,
        model_name=openai_model_name,
        assistant_id=openai_assistant_id
    )

    # Обрабатываем каждый файл на основе указанных шаблонов
    for file_path, content in yield_files_content(
        gs.path.src, ['*.py', 'README.MD']
    ):
        # Создаем входной контент для модели
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

            # Сохраняем ответ модели, изменяя суффикс файла на `.md`
            save_response(file_path=file_path, response=openai_response, from_model='openai')
        except Exception as ex:
            logger.error(ex)
            # Опционально: обработать ошибку более изящно
        # Опционально: спим, чтобы предотвратить превышение лимитов API или троттлинг
        time.sleep(20)

def save_response(file_path: Path, response: str, from_model: str) -> None:
    """
    Сохраняем ответ модели в файл markdown с обновленным путем на основе роли.

    Args:
        file_path (Path): Исходный путь к обрабатываемому файлу.
        response (str): Ответ от модели для сохранения.
    """
    global role

    # Словарь, ассоциирующий роли с директориями
    role_directories = {
        'doc_writer': f'docs/{from_model}/raw_rst_from_ai',
    }

    # Проверка наличия роли в словаре
    if role not in role_directories:
        logger.error(f"Неизвестная роль: {role}. Файл не будет сохранен.")
        return

    # Получаем директорию, соответствующую роли
    role_directory = role_directories[role]

    # Формируем новый путь с учетом роли
    export_file_path = file_path.parts
    new_parts = []

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
) -> Iterator[tuple[Path, str]]:
    """
    Извлекает содержимое файла на основе шаблонов из исходного каталога, исключая определенные шаблоны и каталоги.

    Args:
        src_path (Path): Базовый каталог для поиска файлов.
        patterns (list[str]): Список шаблонов файлов для включения (например, ['*.py', '*.txt']).

    Yields:
        Iterator[tuple[Path, str]]: Кортеж из пути к файлу и его содержимого в виде строки.
    """

    # Регулярные выражения для исключаемых файлов и директорий
    exclude_file_patterns = [
        re.compile(r'.*\\(.*\\).*'),  # Файлы и директории, содержащие круглые скобки
        re.compile(r'___+.*'),      # Файлы или директории, начинающиеся с трех и более подчеркиваний
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
            content = file_path.read_text(encoding="utf-8")
            yield file_path, content

if __name__ == "__main__":
    print("Starting training ...")
    main()