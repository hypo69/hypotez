# # \file /src/utils/string/html_simplification.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for cleaning HTML tags from the text and simplifying the HTML code.
==============================================================================
The module minimizes the HTML code, removes tags and attributes, and also processes
Special cases, such as scripts, styles and comments.
The main attention is paid to the contents of the tag <body>.
Allows you to remove "insignificant" tags containers, leaving only tags,
containing the text or which are permitted by empty tags (for example, <br>).
Uses Beautifulsoup for reliable Parsing HTML and Config class
To control the simplification parameters.

Dependencies:
    - Beautifulsoup4 (Pip Install Beautifulsoup4)
    - LXML (optionally, for faster parsing: PIP Install LXML)

 .. Module :: src.utils.string.html_simplification"""

import re
import html
from pathlib import Path
from typing import Optional, Set, Dict, List, Union
from dataclasses import dataclass, field
from bs4 import BeautifulSoup, Comment, NavigableString, Tag


# We leave imports from your project if they are needed
import header
from header import __root__
from src import gs
from src.logger import logger

@dataclass
class Config:
    """Configuration for the Simplify_html function.

    Attributes:
        allowed_tags (set [str]): a lot of tags in the lower register that needs to be left.
            If `set ()` (empty set), all tags (except for remote options) remain.
            Tags will not be expanded in this set (unw parap) if `keep_only_significant` = false,
            or potentially removed/deployed if `Keep_only_significant` = True.
            Example: `{'P', 'A', 'Br', 'Strong', 'Em'}`
        allowed_attributes (dict [str, set [str]]): a dictionary where the keys are the names of tags (in the lower register),
            And the values are many permitted attributes (in the lower register) for this tag.
            If `{}` (empty dictionary), all attributes are removed.
            If the attribute is allowed for the `'*'` tag, it is allowed for all tags.
            Example: `{'a': 'href', 'title'}, 'img': {'src', 'alt'}, '*': {'style'}}}
        unw parap_tags (set [str]): a lot of tags (in the lower register) that you need to "expand"
            (remove the tag, leaving the contents) at the final stage, regardless of other rules.
            Example: `{'span', 'div'}`
        VOID_TAGS (set [str]): many tags considered "empty" (VOID elements),
            Used for `keep_only_significant = true`.
        Remove_comments (Bool): Do HTML-Commentaries (`<!-...->`).
        Remove_scripts_styles (Bool): Do you remove the tags `<Script>` and `<Style>` along with their contents.
        Normalize_whitespace (Bool): replace multiple spaces with one and remove spaces at the beginning/end.
        Keep_only_significant (Bool): Do you remove tags that do not contain significant content.
        Parser (StR): Parser for Beautifulsoup ('Html.parser', 'LXML', 'HTML5Lib')."""
    # Setting the default value through Default_Factory for changed types
    allowed_tags: Set[str] = field(default_factory=lambda: {'p', 'b', 'a', 'br', 'img', 'h1', 'hr', 'div', 'span', 'table', 'tbody', 'tr', 'td', 'th', 'ul', 'ol', 'li', 'strong', 'em', 'i', 'u'}) # Expanded set by default
    # Changed: deleted 'class' and 'ID' from standardly permitted for '*'
    allowed_attributes: Dict[str, Set[str]] = field(default_factory=lambda: {'a': {'href', 'title'}, 'img': {'src', 'alt', 'title'}, '*': {'style'}})
    unwrap_tags: Set[str] = field(default_factory=set) # By default, we do not unfold anything forcibly
    VOID_TAGS: Set[str] = field(default_factory=lambda: {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    })
    remove_comments: bool = True
    remove_scripts_styles: bool = True # Delete scripts and default styles
    normalize_whitespace: bool = True
    keep_only_significant: bool = False # By default we do not delete "insignificant" tags
    parser: str = 'html.parser' # Default value for parser

# --- The main functions ---

def strip_tags(html_content: str | None, parser: Optional[str] = None) -> str:
    """Completely removes all HTML/XML tags from the line, leaving only the text.
    Also transforms HTML-lounges (type &) into the corresponding symbols.
    Focus on the contents of the <body> tag if it is present.

    Args:
        html_content (str | none): a string with a HTML code or None.
        Parser (Optional [Str]): Parser for Beautifulsoup ('Html.parser', 'LXML', 'HTML5Lib').
                                If None is used 'html.parser'.

    Returns:
        STR: Text without html tugs. Returns an empty line with an error, None or empty input.

    RAISES:
        Exception: Beautifulsoup can generate exceptions with serious Parsing problems,
                   which are logged in.

    Example:
        >>> html_input = '<html> <head> <title> t </ditle> </daad> <body> <p> hello <b> world </b> </p> <!-comment-> </body> </ html>'
        >>> strip_tags (html_input)
        'Hello World!'
        >>> strip_tags ('Text with <entities> & symbols')
        'Text with <entities> & symbols'
        >>> strip_tags (none)
        ''"""
    # Verification of input data
    if not html_content or not isinstance(html_content, str):
        # The logger may not be configured at the Warning level, the Debug or Info is used, if you need to see it often
        logger.debug("strip_tags: Входные данные некорректны или пустые.")
        return '' # Return empty line for incorrect input

    # The Parser from the argument or default value is used
    actual_parser = parser if parser is not None else 'html.parser'

    try:
        # Initialization of Beautifulsoup for the entire document
        original_soup = BeautifulSoup(html_content, actual_parser)

        # We are looking for Body tag
        body_tag = original_soup.body

        # If Body is not found, we process all the content as a body
        target_node = body_tag if body_tag else original_soup

        # Removal of non -actual elements (scripts, styles) inside the target node
        for element in target_node(['script', 'style']):
            element.decompose() # The function removes the tag and its contents made of wood

        # Extracting the text from the target node
        text: str = target_node.get_text(separator=' ', strip=True)

        # Transformation of HTML SUBLECTIONS (&, <, etc.) into symbols
        text = html.unescape(text)

        # Additional cleaning: replacing multiple spaces with one
        text = re.sub(r'\s+', ' ', text).strip()

        return text
    except Exception as ex:
        # Logger error logging
        logger.error(f"Ошибка при обработке HTML в strip_tags: {html_content[:100]}...", ex, exc_info=True)
        # Return empty line as an indicator of the problem
        ... # Added troot in front of Return in the Except block
        return ''

def simplify_html(
    html_content: str | None,
    config: Optional[Config] = None, # Allows you to convey a specific configuration
    parser: Optional[str] = None, # Allows you to reduce the Parser from the config
) -> str:
    """Simplifies the HTML code, focusing on the contents of the <body> tag and using parameters
    From the Config object (transferred or created by default).

    Removes everything outside <Body>, then applies the rules for simplification (removal of tags, attributes,
    comments, scripts, styles, etc.) to the content of <body> according to the settings
    In the object `config`. Can also remove tags containers inside <body>,
    not containing significant content if `config.keep_only_significant = true`.

    Args:
        html_content (str | none): a string with a HTML code or None.
        Config (Optional [config]): Object of configuration. If None, Config () is used
                                   With default settings.
        Parser (Optional [Str]): Parser for Beautifulsoup ('Html.parser', 'LXML', 'HTML5Lib').
                                If indicated, overrights `config.parser`.

    Returns:
        STR: Simplified HTML code of the contents <body>. Returns an empty line with an error,
             None/empty input or if the <body> tag was not found.

    RAISES:
        Exception: Beautifulsoup can generate exceptions with serious Parsing problems,
                   which are logged in.

    Example:
        >>> # Example of Class/ID removal by default
        >>> Default_cfg = config (Allowed_tags = {'Div', 'Span'})
        >>> sample_cls_id = '<body> <div class = "Main" id = "Cont"> <span style = "color: red"> text </span> </div> </body>' '
        >>> simplify_html (sample_cls_id, config = default_cfg)
        '<div> <span style = "color: red"> text </span> </div>'

        >>> # Example with obvious resolution of Class/ID
        >>> allow_cls_id_cfg = config (allowed_tags = {'div', 'span'}, allowed_attributes = {''*': {' class', 'id', 'style'}})
        >>> simplify_html (sample_cls_id, config = allow_cls_id_cfg)
        '<Div class = "Main" ID = "CONT"> <span style = "color: red"> text </span> </div>'"""
    # The transmitted config or the creation of a new by default is used
    effective_config = config if config is not None else Config()

    # Verification of input data
    if not html_content or not isinstance(html_content, str):
        logger.debug("simplify_html: Входные данные некорректны или пустые.")
        return ''

    # Parser selection: Priority in the argument of function, then config
    actual_parser: str = parser if parser is not None else effective_config.parser

    try:
        # --- Step 1: isolation of the contents <body> ---
        original_soup = BeautifulSoup(html_content, actual_parser)
        body_tag = original_soup.body

        if not body_tag:
            # If there is no Body, but there is content, let's try to process it as a fragment
            if original_soup.contents:
                 logger.debug(f"Тег <body> не найден, но есть контент. Обработка как фрагмента: {html_content[:100]}...")
                 body_content_str = html_content # All content is used
            else:
                 logger.warning(f"Тег <body> не найден и нет контента в HTML: {html_content[:100]}... Возвращается пустая строка.")
                 return ''
        else:
            # We get the contents of Body as a string for repeated parsing
            body_content_str = body_tag.decode_contents()


        # --- Step 2: Processing of isolated contents <body> (or fragment) ---
        # creation of new soup only from the contents of the Body or the entire fragment
        soup = BeautifulSoup(body_content_str, actual_parser)

        # 2.1 initial cleaning in the new soup: comments, scripts, styles
        if effective_config.remove_comments:
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            for comment in comments:
                comment.extract()
        if effective_config.remove_scripts_styles:
            # Remove Script/Style, which could be inside the Body or Fragment
            for element in soup(['script', 'style']):
                element.decompose()

        # 2.2 Removal of insignificant containers (if included)
        if effective_config.keep_only_significant:
            significant_void_tags: Set[str]
            current_allowed_tags = effective_config.allowed_tags
            significant_void_tags = effective_config.VOID_TAGS.intersection(current_allowed_tags)

            significant_elements_ids: Set[int] = set()
            all_tags: List[Tag] = soup.find_all(True)

            for tag in reversed(all_tags):
                if not tag.parent and tag.name != '[document]':
                     ... # Processing of the upper level elements (do not delete on the basis of ancestors)

                is_significant: bool = False
                tag_name_lower: str = tag.name.lower()

                if tag_name_lower in significant_void_tags:
                    is_significant = True
                else:
                    for child in tag.children:
                        if isinstance(child, NavigableString) and child.string.strip():
                            is_significant = True
                            break
                        elif isinstance(child, Tag) and id(child) in significant_elements_ids:
                             is_significant = True
                             break

                if is_significant:
                    significant_elements_ids.add(id(tag))
                elif tag.parent: # We do not remove the root elements of the contents of the Body in this way
                    should_unwrap: bool = effective_config.unwrap_tags is not None and tag_name_lower in effective_config.unwrap_tags
                    will_be_unwrapped_by_allowed: bool = tag_name_lower not in current_allowed_tags

                    if not should_unwrap and not will_be_unwrapped_by_allowed:
                         tag.decompose()


        # 2.3 final processing of tags and attributes
        tags_to_process_final: List[Tag] = soup.find_all(True)

        for tag in tags_to_process_final:
            if tag.name == '[document]':
                 continue
            if not tag.find_parent() and tag.name != '[document]':
                 ... # Top -level tag processing

            tag_name: str = tag.name.lower()

            # 3.1. Tagging tags from config.unwrap_tags
            if effective_config.unwrap_tags and tag_name in effective_config.unwrap_tags:
                 if tag.parent:
                      tag.unwrap()
                      continue
                 else:
                      logger.debug(f"Попытка unwrap тега '{tag_name}' без родителя (пропущено).")
                      ...

            # 3.2. Filtering on allowed tags (config.allowed_tags)
            if tag_name not in effective_config.allowed_tags:
                 if tag.parent:
                      tag.unwrap()
                      continue
                 else:
                      logger.debug(f"Тег '{tag_name}' без родителя не в allowed_tags (пропущено удаление).")
                      ...

            # 3.3. Filtering attributes
            if isinstance(tag, Tag) and tag.attrs:
                current_attrs = dict(tag.attrs)
                specific_allowed_attrs: Set[str] = set()

                if effective_config.allowed_attributes is not None:
                    specific_allowed_attrs.update(effective_config.allowed_attributes.get(tag_name, set()))
                    specific_allowed_attrs.update(effective_config.allowed_attributes.get('*', set()))

                # If the attributes dictionary is empty or for the tag there are no permitted ones - we delete everything
                if not effective_config.allowed_attributes or not specific_allowed_attrs:
                     tag.attrs = {}
                else:
                    # We are weered by a copy of the keys to safely remove from the original
                    for attr_name_case_sensitive in list(current_attrs.keys()):
                        attr_name_lower: str = attr_name_case_sensitive.lower()
                        if attr_name_lower not in specific_allowed_attrs:
                            # We delete the attribute if it is not in permitted
                            del tag.attrs[attr_name_case_sensitive]


        # --- Step 3: obtaining the final HTML and normalization of spaces ---
        # We extract the contents of the processed soup
        final_html: str = soup.decode_contents()

        # Normalization of spaces if the option is enabled
        if effective_config.normalize_whitespace and final_html:
            final_html = re.sub(r'\s+', ' ', final_html).strip()

        return final_html

    except Exception as ex:
        logger.error(f"Ошибка при обработке HTML в simplify_html: {html_content[:100]}...", ex, exc_info=True)
        ... # Added troot in front of Return in the Except block
        return '' # Return empty line with any error


# --- examples of use (for demonstration and debugging) ---

if __name__ == "__main__":
    # It is assumed that Logger is already configured somewhere at the start of the application
    # If not, you can add a basic setup for tests:
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    # logger = logging.getlogger (__ name__) # The standard logger is used if SRC.Logger is not configured

    logger.info("--- Примеры работы модуля html_simplification ---")

    # Determination of the Parser once
    parser_choice = 'lxml'
    try:
        import lxml
        logger.debug(f"(Используется парсер: {parser_choice})")
    except ImportError:
        parser_choice = 'html.parser'
        logger.debug(f"(Парсер lxml не найден, используется: {parser_choice})")


    sample_html_full: str = """<! Doctype html>
    <html>
    <head>
        <meta charset = "UTF-8">
        <Title> Test page </ Title>
        <Style> Body {font-Family: Sans-Serif; }/ * CSS Comment */</style>
        <script type = "Text/JavaScript"> alert ("Hello!"); // js Comment </SCRIPT>
    </ Head>
    <body>
        <div ID = "Main" class = "Container">
            <h1 style = "color: blue;"> an example html </ h1>
            <p style = "margin: 10px;" Class = "Main-Text First">
                This is <b> the first </b> paragraph with <a href = "http://example.com" target = "_ Blank" title = "visit"> link </a>.
                <! Is HTML Comment inside Body->
                Contains <span class = "Highlight"> unnecessary </span> & important text.
            </p>
            <div Class = "Empty-Container"> </ DIV>
            <div>
                Another text <br/> with the transfer of the line. <IMG SRC = " /Logo.png" Alt = "Logo" Title = "Company Logo" Width = "100" />
            </div>
            <p class = "Main-Text Second"> the second paragraph. </p>
        </div>
        <hr/>
        <footer> empty section </footer>
    </body>
    </ html>"""
    # The file reading is noted so that the examples work autonomously
    # try:
    # from Header Import __root__ # We assume that __root__ is defined
    # sample_html_full = Path(__root__,'SANDBOX','davidka','raw_data_products','raw-1802-27026.html').read_text(encoding='utf-8')
    # Logger.info ("Loaded HTML from the file")
    # except (ImportError, FileNotFoundError) as e:
    # Logger.warning (F "failed to download HTML from a file, a built -in example is used: {e}")

    logger.info("\n1. Исходный HTML (фрагмент):\n" + sample_html_full[150:650])

    logger.info("\n2. Текст после strip_tags():")
    stripped_text: str = strip_tags(sample_html_full, parser=parser_choice)
    logger.info(stripped_text)

    logger.info("\n3. simplify_html() с Config по умолчанию (class/id удалены):")
    # Config is used by default where Class/ID is not allowed for '*'
    default_cfg = Config()
    simplified_default: str = simplify_html(sample_html_full, config=default_cfg, parser=parser_choice)
    logger.info(simplified_default)
    # The expected result: the structure is saved, but the attributes of Class and ID are deleted. Style remains.
    # <div style = ""> <h1 style = "color: blue;"> example html </ h1> <p style = "margin: 10px;"> this <b> first </b> paragraph with <a href = "http://example.com" title = "visit"> link </a>. Contains <span> unnecessary </span> & important text. </p> <div Style = ""> </div> <div style = ""> another text <br/> with the transfer of the line. <img src = "/logo.png" alt = "logo" title = "Company Logo"/> </ Div> <p Style = "> The second paragraph. </p> </div> <hr/> An empty section

    logger.info("\n4. simplify_html() с Config, явно разрешающим class/id:")
    config_allow_cls_id = Config(
        allowed_tags=default_cfg.allowed_tags, # Tags from default
        allowed_attributes={'a': {'href', 'title'}, 'img': {'src', 'alt', 'title'}, '*': {'class', 'id', 'style'}}, # We allow class, id, style for everyone
        unwrap_tags=default_cfg.unwrap_tags,
        keep_only_significant=False,
    )
    simplified_cls_id: str = simplify_html(sample_html_full, config=config_allow_cls_id, parser=parser_choice)
    logger.info(simplified_cls_id)
    # The expected result: Class and ID remain, because Obviously allowed.
    # <div ID = "Main" class = "Container" style = ""> <h1 style = "color: blue;"> example html </ h1> <p style = "margin: 10px;" Class = "Main-Text First"> this <b> first </b> paragraph with <a href = "http://example.com" Title = "Visit"> link </a>. Contains <span class = "Highlight"> unnecessary </span> & important text. </p> <div Class = "Empty-Container" Style = ""> </ Div> <div Style = ""> also text <br/> with the transfer of the line. <img src = "/logo.png" alt = "logo" title = "Company Logo"/> </ Div> <p class = "Main- Text Second" Style = ""> The second paragraph.


    logger.info("\n5. simplify_html() с keep_significant=True (class/id удалены по умолчанию):")
    config_significant = Config(
        allowed_tags={'p', 'b', 'a', 'br', 'img', 'h1', 'hr', 'div'}, # Specific tags
        allowed_attributes={'a': {'href'}, 'img': {'src', 'alt'}, '*': {'style'}}, # All Style is allowed
        unwrap_tags={'span', 'footer'},
        keep_only_significant=True,
    )
    simplified_significant: str = simplify_html(sample_html_full, config=config_significant, parser=parser_choice)
    logger.info(simplified_significant)
    # Expected result: as in test 3, but without class/ID. Empty DIV is removed.
    # <div style = ""> <h1 style = "color: blue;" an example html </ h1> <p style = "margin: 10px;"> this <b> first </b> paragraph with <a href = "http://example.com"> link </a>. Contains an unnecessary & important text. </p> <div Style = ""> More text <br/> with the transfer of the line. <img src = "/logo.png" alt = "logo"/> </div> <p style = ""> the second paragraph. </p> </div> <hr /> The empty section


    logger.info("\n--- Тестирование крайних случаев ---")
    default_config_test = Config() # Config is used by default for tests
    config_keep_significant_default = Config(keep_only_significant=True)

    logger.info(f"strip_tags(None): -> '{strip_tags(None)}'")
    logger.info("\n------------------------------------")
    logger.info(f"strip_tags(''): -> '{strip_tags('')}'")
    logger.info("\n------------------------------------")
    logger.info(f"simplify_html(None, config=default_config_test): -> '{simplify_html(None, config=default_config_test)}'")
    logger.info("\n------------------------------------")
    logger.info(f"simplify_html('', config=default_config_test): -> '{simplify_html('', config=default_config_test)}'")
    logger.info("\n------------------------------------")
    # HTML without Body (will be treated as a fragment)
    html_no_body = '<h1 class="title">Title</h1><p id="intro">Text</p>'
    logger.info(f"simplify_html (no body, default config): -> '{simplify_html(html_no_body, config=default_config_test, parser=parser_choice)}'") # Class/ID will be removed
    logger.info("\n------------------------------------")
    # Html with blank body
    html_empty_body = "<html><head></head><body></body></html>"
    logger.info(f"simplify_html (empty body): -> '{simplify_html(html_empty_body, config=default_config_test, parser=parser_choice)}'")
    logger.info("\n------------------------------------")
    # Keep_significant with empty div in Body
    html_empty_div = '<body><div class="empty"> </div></body>'
    # We expect '', because DIV empty and keep_significant = True
    logger.info(f"simplify_html ('<div class=\"empty\"> </div>', config=config_keep_significant_default): -> '{simplify_html(html_empty_div, config=config_keep_significant_default, parser=parser_choice)}'")
    logger.info("\n------------------------------------")
    # Keep_significant with text in p
    html_p_text = '<body><p class="para">Text</p></body>'
    config_p_only_sig = Config(allowed_tags={'p'}, keep_only_significant=True) # Class will leave, because Not allowed in this config
    logger.info(f"simplify_html ('<p class=\"para\">Text</p>', config=config_p_only_sig): -> '{simplify_html(html_p_text, config=config_p_only_sig, parser=parser_choice)}'")
    logger.info("\n------------------------------------")
    # keep_significant с br
    html_br = "<body>Текст <br class='break'/> еще</body>"
    config_br_only_sig = Config(allowed_tags={'br'}, keep_only_significant=True) # Br will remain, class will retire
    logger.info(f"simplify_html ('Текст <br class=\'break\'/> еще', config=config_br_only_sig): -> '{simplify_html(html_br, config=config_br_only_sig, parser=parser_choice)}'")