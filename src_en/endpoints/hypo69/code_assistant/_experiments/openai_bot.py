# # \file /src/endpoints/hypo69/code_assistant/_experiments/openai_bot.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.endpoints.hypo69.code_assistant._experiments 
	:platform: Windows, Unix
	:synopsis:"""


""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix"""
""":platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:"""
  
"""module: src.endpoints.hypo69.code_assistant._experiments"""



Модуль для экспериментов с моделью AI OpenAI. Он обрабатывает исходный код или документацию, отправляет его в модель для анализа и получения ответов.

Процесс работы:
1. Модуль использует роль выполнения, установленную внутри кода, для взаимодействия с моделью.
2. Для роли `doc_writer` используется модель **OpenAI GPT-4** для генерации документации или других текстов.
3. Входные данные для модели включают комментарии и код/документацию, которые передаются в модель для обработки.
4. Ответ модели сохраняется в файл с расширением `.md` в зависимости от роли.
   
Используетсяая модель:
- **OpenAI GPT-4**: Используется для создания документации и других текстовых материалов.

Ссылки на документацию модели:
- OpenAI: https://platform.openai.com/docs

"""Import Re
From Pathlib Import Path
Import Time
From Typs Import Iterator

FROM SRC Import GS
from src.ai.openai import Openaimodel
from src.utils.file import yield_files_content, read_text_file
from src.logger.logger Import Logger

# Global variable for the role
Role: str = 'doc_writer' # installation of the role directly inside the code

Openai_Model_name: str = 'gpt-4o-mini'
Openai_assistant_id: str = gs.credentials.openai.assistant_id.code_assistant
Opena_Model: Openaimodel

Def Main () -> None:""" Main function to process files and interact with the model.

    This function reads a comment file, iterates over specified files in the source directory,
    and sends the file content to a model for analysis. It then processes the model's response.
    """global role

    role = role if role else 'doc_writer'

    if role == 'doc_writer':
        comment_for_model_about_piece_of_code = 'doc_writer.md'
        system_instruction: str = 'create_documentation.md'
        

    # Read the comment for model input from a markdown file
    comment_for_model_about_piece_of_code = read_text_file(
        gs.path.src / 'endpoints' / 'hypo69' / 'onela_bot' / 'instructions' / comment_for_model_about_piece_of_code
    )
    system_instruction = read_text_file(gs.path.src / "ai" / "prompts" / "developer" / system_instruction)

    openai_model = OpenAIModel(
        system_instruction=system_instruction,
        model_name=openai_model_name,
        assistant_id=openai_assistant_id
    )

    # Process each file based on the specified patterns
    for file_path, content in yield_files_content(
        gs.path.src, ['*.py', 'README.MD']
    ):
        # Construct the input content for the model
        content = (
            f"{comment_for_model_about_piece_of_code}\n"
            f"Расположение файла в проекте: `{file_path}`.\n"
            f"Роль выполнения: `{role}`.\n"
            "Код:\n\n"
            f"```{content}```\n"
        )
        try:
            # Get the response from the model
            openai_response = openai_model.ask(content)

            # Save the model's response, changing the file suffix to `.md`
            save_response(file_path=file_path, response=openai_response, from_model='openai')
        except Exception as ex:
            logger.error(ex)
            # Optional: handle error more gracefully
        # Optional sleep to prevent API rate limits or throttling
        time.sleep(20)


def save_response(file_path: Path, response: str, from_model: str) -> None:""" Save the model's response to a markdown file with updated path based on role.

    Args:
        file_path (Path): The original file path being processed.
        response (str): The response from the model to be saved.
    """Global Role

    # Dictionary associating roles with directors
    Role_Directories = {
        'doc_writer': f'Docs/{from_model}/raw_rsst_from_ai ',
    }

    # Testing the presence of a role in the dictionary
    if role not in role_directories:
        Logger.error (F "Unknown Role: {Role}. The file will not be saved.")
        Return

    # We get a directory corresponding to the role
    ROLE_DIRECTORY = ROLE_DIRECTORES [ROLE]

    # We form a new path taking into account the role
    Export_file_path = file_path.parts
    New_parts = []

    for part in export_file_path:
        run part == 'src':
            New_parts.ppend (Role_Directory)
        Else:
            New_parts.ppend (Part)

    # Form a new path with a replaced part
    Export_file_path = Path (*New_parts)

    # Change the suffix file to .MD
    Export_file_path = Export_file_path.with_suffix (". MD")

    # Make sure that the directory exists
    Export_file_path.part.mkdir (Parents = True, Exist_ok = True)

    # Save the answer to the new file
    Export_file_path.write_text (Response, Encoding = "UTF-8")
    Print (F "Response Saved to: {Export_file_path}")


Def yield_files_content (
    SRC_PATH: Path, Patterns: List [str]
) -> iterator [tuple [path, str]]:""" Yield file content based on patterns from the source directory, excluding certain patterns and directories.

    Args:
        src_path (Path): The base directory to search for files.
        patterns (list[str]): List of file patterns to include (e.g., ['*.py', '*.txt']).

    Yields:
        Iterator[tuple[Path, str]]: A tuple of file path and its content as a string.
    """

    # Regular expressions for excluded files and directory
    exclude_file_patterns = [
        re.compile(r'.*\(.*\).*'),  # Files and directors containing round brackets
        re.compile(r'___+.*'),      # Files or directory starting with three or more emphasizations
    ]

    # List of service directors that need to be excluded
    exclude_dirs = {'.ipynb_checkpoints', '_experiments', '__pycache__', '.git', '.venv'}

    for pattern in patterns:
        for file_path in src_path.rglob(pattern):
            # Skip files that are in the excluded directors
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue

            # Skip files corresponding to the excluded patterns
            if any(exclude.match(str(file_path)) for exclude in exclude_file_patterns):
                continue

            # Reading the contents of the file
            content = file_path.read_text(encoding="utf-8")
            yield file_path, content


if __name__ == "__main__":
    print("Starting training ...")
    main()
