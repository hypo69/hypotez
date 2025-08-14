# # \file /src/utils/html.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for normalizing and cleaning the HTML string.
========================================================================

Provides functions for removing unwanted tags (scripts, styles),
Comments and normalization of testable characters in the HTML code.
 ** Function `clean_html_string`: **
    * Accepts HTML and optionally the name of Parser (`html.parser`,` html5lib`, `lxml`).
    * Added check for empty or non -stroke input.
    * The `try ... Except` unit is turned on for processing parsing errors and logging them using` logger.error`.
    * The list of `tags_to_remove` expanded by typical navigation containers, forms, functions, etc.
    * Normalization of spaces now uses the Flag `Re.unicode` for the correct work with different test -sized Unicode symbols.
    * Removing tags `<body>` is made more reliable using `re.sub` and flags` re.ignorecase` (register -dependence) and `re.dotall` (so that` [^>]* `corresponded to the strings inside the Body tag). `Count = 1` guarantees the removal of only the first entry of` <body> `.
    * The function returns the empty line of `" "` in case of error or universal input.
`` `RST
.. Module :: src.utils.html
`` `"""

import re
from bs4 import BeautifulSoup, Comment
import logging # Add logistics for errors

# Setting up basic logistics (you can configure more in more detail in the main application)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_html_string(html_content: str, parser: str = 'html.parser') -> str:
    """Cleans the line HTML: deleys scripts, styles, comments
    And normalizes testable characters.

    Args:
        html_content (str): input line with html.
        Parser (StR): Parser for Beautifulsoup ('Html.parser', 'Html5Lib', 'LXML').
                      'html.parser' - built -in, fast, less reliable.
                      'HTML5LIB' - reliable, slower, requires installation.
                      'LXML' - fast, reliable, requires the installation of C -Bibliotek.

    Returns:
        STR: The purified HTML line or an empty line in case of an error."""
    if not html_content or not isinstance(html_content, str):
        logger.debug("Получено пустое или нестроковое содержимое для очистки.")
        return ""

    try:
        # 1. Parsing using Beautifulsoup
        soup = BeautifulSoup(html_content, parser)

        # 2. Removing unnecessary tags
        tags_to_remove = ['script', 'style', 'head', 'meta', 'link', 'noscript', 'iframe', 'button', 'input', 'textarea', 'select', 'option', 'form', 'nav', 'footer', 'header', 'aside']
        for tag in soup.find_all(tags_to_remove):
            tag.decompose()

        # 3. Removing comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # 4. We get the "main" contents (usually inside Body, but if it is not, we take everything)
        target_node = soup.body if soup.body else soup
        if not target_node:
            logger.debug("Не удалось найти корневой узел (body или soup) после парсинга.")
            return ""

        # 5. We get a string of processed wood
        intermediate_string = str(target_node)

        # 6. Normalization of spaces using regular expressions
        # We replace all the sequences of protected characters (\ n, \ t, gap, etc.) for one gap
        cleaned_string = re.sub(r'\s+', ' ', intermediate_string, flags=re.UNICODE).strip()

        # We remove the gaps between tags (for example, "> <" on "> <") - optionally
        cleaned_string = re.sub(r'>\s+<', '><', cleaned_string, flags=re.UNICODE)

        # Remove tags <body> and </body> if they remained around the edges
        # Register -dependent search is used and we take into account possible attributes
        cleaned_string = re.sub(r'^<body[^>]*>', '', cleaned_string, count=1, flags=re.IGNORECASE | re.DOTALL).lstrip()
        cleaned_string = re.sub(r'</body\s*>$', '', cleaned_string, count=1, flags=re.IGNORECASE).rstrip()


        return cleaned_string

    except Exception as e:
        logger.error(f"Ошибка при очистке HTML: {e}", exc_info=True) # Logging error with traceback
        # In case of error, you can return the original line or empty
        return "" # Return empty line with an error


# --- Block for demonstration and testing ---
if __name__ == "__main__":
    # Example HTML for testing
    html_string_example = """<! Doctype html>
    <html>
    <head>
        <Title> Test Page </ Title>
        <meta charset = "UTF-8">
        <Script> Alert ('Remove me'); </ Script>
        <style> .hide {display: none; } </ Style>
        <Link Rel = "Stylesheet" href = "style.css">
    </ Head>
    <Body Class = "Page">
        <!-This is a comment->
        <dader> <h1> Logo </ h1> <nav> menu </nav> </ header>
        <div>
            <p> This is the first paragraph.
            Contains \ t Tabs and \ n transfers. </p>
            <p> The second paragraph. </p>
            <noscript> Turn on JavaScript! </ Noscript>
        </div>
        <Form Action = "# "> <Button> button </Button> </form>
        <footer> Contacts </footer>
        <script SRC = "Extra.js"> </ Script>
    </body>
    </ html>"""

    print("--- Исходный HTML ---")
    print(html_string_example)

    print("\n--- Очищенный HTML (html.parser) ---")
    cleaned_html_parser = clean_html_string(html_string_example, parser='html.parser')
    print(cleaned_html_parser)

    # An example of use with HTML5LIB (requires PIP Install HTML5LIB)
    try:
        print("\n--- Очищенный HTML (html5lib) ---")
        # Import attempt to check the availability
        import html5lib
        cleaned_html_html5lib = clean_html_string(html_string_example, parser='html5lib')
        print(cleaned_html_html5lib)
    except ImportError:
        print("Библиотека html5lib не установлена. Пропустите этот тест.")
    except Exception as e:
         print(f"Ошибка при использовании html5lib: {e}")

    # An example with empty input
    print("\n--- Пустой ввод ---")
    print(f"Результат: '{clean_html_string('')}'")

    # Example with unylidery html
    invalid_html = "<div><p>Не закрыт</div>"
    print("\n--- Невалидный HTML ---")
    print(f"Результат: '{clean_html_string(invalid_html)}'")
