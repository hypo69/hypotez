## \file /src/endpoints/wordpress_assistant/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.endpoints.wordpress_assistant
    :platform: Windows, Unix
    :synopsis: WordPress translation assistant using Gemini LLM.
"""

import asyncio
from pathlib import Path
from dataclasses import dataclass
from typing import List

from header import __root__
from src import gs
from src.llm.gemini import GoogleGenerativeAi
from src.utils.file import recursively_yield_file_path
from src.logger import logger
from src.utils.printer import pprint


def gemini_getinstance(api_key: str, system_instruction: str) -> GoogleGenerativeAi:
    """! Create and return an instance of GoogleGenerativeAi with the provided API key and system instruction.

    Args:
        api_key (str): Gemini API key.
        system_instruction (str): System instruction prompt.

    Returns:
        GoogleGenerativeAi: Configured Gemini model instance.
    """
    return GoogleGenerativeAi(api_key=api_key, system_instruction=system_instruction)


Languages: list = [
    "en",
    "fr",
    "es",
    "he",
    "ua",
    "pl",
    "de",
    "it",
]


@dataclass
class WordpressAssistant:
    """! Dataclass version of the WordPress Assistant configuration."""

    async def translate(
        self, model_instance: GoogleGenerativeAi, text: str, target_language: str
    ) -> str:
        """! Translate text to the specified target language using Gemini API.

        Args:
            model_instance (GoogleGenerativeAi): Gemini model instance.
            text (str): Source text to translate.
            target_language (str): Language code (e.g., 'en', 'fr').

        Returns:
            str: Translated text in HTML format.
        """
        prompt: str = (
            f"Translate the following text to {target_language} and return HTML:\n\n{text}"
        )
        response: str = model_instance.ask(prompt)
        return response

    async def generate_wordpress(
        self, model_instance: GoogleGenerativeAi, text: str
    ) -> str:
        """! Generate a WordPress-ready post from given text using Gemini API.

        Args:
            model_instance (GoogleGenerativeAi): Gemini model instance.
            text (str): Text content to format as WordPress post.

        Returns:
            str: HTML post formatted for WordPress.
        """
        prompt: str = (
            f"Format the following content as a clean WordPress HTML post:\n\n{text}"
        )
        response: str = model_instance.ask(prompt)
        return response

    async def run(self, model_instance: GoogleGenerativeAi, process_dir: Path) -> None:
        """! Run translation workflow for all `.md` and `.txt` files in directory.

        Args:
            model_instance (GoogleGenerativeAi): Gemini model instance.
            process_dir (Path): Directory path with source text files.

        Returns:
            None
        """


        def clean_before_heading(text: str) -> str:
            """
            Remove everything before the first <!-- wp:heading --> marker.

            Args:
                text (str): Input string that may contain WordPress HTML blocks.

            Returns:
                str: String starting from <!-- wp:heading -->. 
                     If marker not found — return the original text.
            """
            marker = "<!-- wp:heading -->"
            if marker in text:
                return text.split(marker, 1)[1].strip()
            return text



        filenames: List[Path] = list(
            recursively_yield_file_path(process_dir, patterns=["*.md", "*.txt"])
        )

        if not filenames:
            logger.error(f"No files found in {process_dir}")
            return

        for file_name in filenames:
            text: str = file_name.read_text(encoding="UTF-8")
            if not text:
                logger.error(f"Empty file skipped: {file_name}")
                continue

            data: str = ""
            for lang in Languages:
                translated: str = await self.translate(model_instance, text, lang)
                translated = clean_before_heading(translated)
                if not translated:
                    logger.error(
                        f"Translation failed for {file_name} → {lang}",
                        exc_info=True,
                    )
                    continue
                data += f"[:{lang}]{translated}"
            data += "[:]"

            output_file: Path = file_name.with_suffix(".html")
            output_file.write_text(data, encoding="UTF-8")
            pprint(f"✅ Saved: {output_file}")


if __name__ == "__main__":
    base_path_for_source_dirs: Path = Path(
        r"C:\Users\user\Documents\repos\public_repositories"
    )
    dirs = ["gemini-cli-articles", "Философия PowerShell", "1001-python"]

    system_instructions_dir: Path = (
        __root__ / "src" / "endpoints" / "wordpress_assistant" / ".gemini"
    )

    system_instruction: str = f"""{(system_instructions_dir / 'GEMINI.md').read_text(encoding='utf-8')}
    Пример md:
{(system_instructions_dir / 'ORIGINAL.md').read_text(encoding='utf-8')}
ответ worpress HTML в формате wordpress ответа:
{(system_instructions_dir / 'WP_POST_TEMPLATE.md').read_text(encoding='utf-8')}
НЕ ДОБАВБЛЯЙ НИЧЕГО ВНЕШНЕГО, ТОЛЬКО ЧИСТЫЙ HTML ДЛЯ WORDPRESS
"""

    kazarinov_api: str = gs.credentials.gemini.kazarinov.api_key
    onela_api: str = gs.credentials.gemini.onela.api_key

    gemini: GoogleGenerativeAi = gemini_getinstance(
        api_key=kazarinov_api, system_instruction=system_instruction
    )
    assistant = WordpressAssistant()
    asyncio.run(
        assistant.run(gemini, base_path_for_source_dirs / "Философия PowerShell" / "ru")
    )
