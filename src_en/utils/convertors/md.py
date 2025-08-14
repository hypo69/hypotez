# # \file /src/utils/convertors/md2dict.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.utils.convertors.md2dict 
	: Platform: Windows, Unix
	: synopsis: Module for converting the Markdown line into a structured dictionary, including the extraction of JSON of the contents, if present."""

import re
from typing import Dict, List, Any
from markdown2 import markdown
from src.logger.logger import logger



def md2html(md_string: str, extras: List[str] = None) -> str:
     """Converts the Markdown line in HTML.

     Args:
         MD_String (str): Markdown string for conversion.
         Extras (List, Optional): List of extensions Markdown2. Defaults to None.

     Returns:
         STR: HTML. Markdown."""
     try:
         if extras is None:
            return markdown(md_string)
         return markdown(md_string, extras=extras)
     except Exception as ex:
        logger.error("Ошибка при преобразовании Markdown в HTML.", exc_info=True)
        return ""


def md2dict(md_string: str, extras: List[str] = None) -> Dict[str, list[str]]:
    """Converts the Markdown line into a structured dictionary.

    Args:
        MD_String (str): Markdown string for conversion.
        Extras (List, Optional): List of Markdown2 extensions for MD2HTML. Defaults to None.

    Returns:
         Dict [str, list [str]]: structured view of the markdown contents."""
    try:

        html = md2html(md_string, extras)
        sections: Dict[str, list[str]] = {}
        current_section: str | None = None

        for line in html.splitlines():
            if line.startswith('<h'):
                heading_level_match = re.search(r'h(\d)', line)
                if heading_level_match:
                    heading_level = int(heading_level_match.group(1))
                    section_title = re.sub(r'<.*?>', '', line).strip()
                    if heading_level == 1:
                        current_section = section_title
                        sections[current_section] = []
                    elif current_section:
                        sections[current_section].append(section_title)

            elif line.strip() and current_section:
                clean_text = re.sub(r'<.*?>', '', line).strip()
                sections[current_section].append(clean_text)

        return sections

    except Exception as ex:
        logger.error("Ошибка при парсинге Markdown в структурированный словарь.", exc_info=True)
        return {}