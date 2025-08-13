# # \file /src/goog/gtanslator/translator.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Translation module
==================================================================
`` `RST
.. Module :: src.goog.gtanslator.translator
`` `"""

from googletrans import Translator, LANGUAGES


import header
from header import __root__
from src import gs
from src.logger import logger
from src.utils.printer import pprint as print


# This list is used as Fallback if the Target_langs provided is incorrect
# Or if there were no default values for Target_langs.
# You can choose the 10 most popular, as in the initial request:
# FALLBACK_DEFAULT_LANG_CODES = [
# 'in', 'zh-cn', 'his', 'is', 'fr', 'ar', 'ru', 'pt', 'de', 'ja'
# None
# Or use a wider list:
FALLBACK_DEFAULT_LANG_CODES = [
'en', 'zh-cn', 'de', 'it', 'es', 'fr', 'ar', 'ru', 'pt', 'ko',
'tr', 'he', 'pl', 'uk', 'nl', 'cs', 'sv', 'da', 'ja'
]

def translate_to(text_to_translate: str,
                           src_lang: str = 'auto',
                           target_langs: list = ['en', 'ru']): # Default value according to your request
    """Translates the text into these languages.

    : PARAM TEXT_TO_TRANSLATE: Text for translation.
    : Param src_lang: The original text language (for example, 'en', 'ru', 'auto' for auto -determination).
    : Param target_langs: a list of tongues for translation (for example, ['en', 'es', 'fr']).
                         By default ['en', 'ru']. If an empty list is transmitted or
                         Incorrect value, the Fallback-list is used.
    : return: a dictionary where the key is the language code (from Target_langs), the meaning is the translated text or error message."""
    translator = Translator()
    translations = {}

    # The logic of determining the original language and its display
    determined_source_lang_code = src_lang
    if src_lang == 'auto':
        source_lang_name_display = "auto (ожидание определения)"
    else:
        source_lang_name_display = LANGUAGES.get(src_lang, src_lang)

    if src_lang == 'auto':
        try:
            detected = translator.detect(text_to_translate)
            determined_source_lang_code = detected.lang
            # We update the displayed name of the source language after a successful definition
            source_lang_name_display = f"{LANGUAGES.get(determined_source_lang_code, determined_source_lang_code)} (обнаружено)"
            # print (f" per
        except Exception as ex:
            logger.error(f"Не удалось определить исходный язык. Используется 'auto' для перевода.", ex)
            determined_source_lang_code = 'auto' # `Auto 'remains for comparison
            source_lang_name_display = "auto (определение не удалось)"

    # print(f"\nОригинал ({source_lang_name_display}): {text_to_translate}\n")

    # Definition of the final list of targeted languages for translation
    final_target_codes = []
    # Checking that target_langs is a non -postal list of lines
    if isinstance(target_langs, list) and len(target_langs) > 0 and all(isinstance(lang, str) for lang in target_langs):
        final_target_codes = target_langs
        # Print (F "Translation will be made in these languages: {Final_Target_codes}")
    else:
        final_target_codes = FALLBACK_DEFAULT_LANG_CODES
        if not isinstance(target_langs, list):
            user_input_type = type(target_langs).__name__
            print(f"Параметр target_langs должен быть списком, получен {user_input_type} ('{target_langs}'). "
                  f"Используется fallback список ({len(final_target_codes)} языков): {final_target_codes}")
        elif len(target_langs) == 0:
            print(f"Передан пустой список target_langs. "
                  f"Используется fallback список ({len(final_target_codes)} языков): {final_target_codes}")
        else: # The list is not empty, but it does not contain lines
             print(f"Список target_langs содержит некорректные значения. "
                  f"Используется fallback список ({len(final_target_codes)} языков): {final_target_codes}")


    for lang_code in final_target_codes:
        # Additional check if Fallback logic did not eliminate all incorrect codes above
        if not isinstance(lang_code, str) or not lang_code.strip():
            print(f"Пропущен некорректный или пустой код языка в списке: '{lang_code}'")
            # The key can be the incorrect lang_code for debugging
            translations[str(lang_code)] = "Некорректный код языка предоставлен"
            continue

        # We do not translate into the same language if it was defined (or set) and coincides
        if lang_code == determined_source_lang_code and determined_source_lang_code != 'auto':
            translations[lang_code] = f"{text_to_translate} (Оригинал)"
            continue
        try:
            # The API always has a SRC_LANG transmission, which the user set (maybe 'auto')
            # The library itself will cope with 'Auto'
            translated_obj = translator.translate(text_to_translate, src=src_lang, dest=lang_code)
            translations[lang_code] = translated_obj.text
        except Exception as e:
            target_lang_name_display = LANGUAGES.get(lang_code, lang_code)
            translations[lang_code] = f"Ошибка перевода на {target_lang_name_display} ({lang_code}): {e}"

    return translations

# Example of use:
if __name__ == "__main__":
    # Make sure the library is installed: PIP Install Googletrans-Py
    try:
        from googletrans import Translator, LANGUAGES
    except ImportError:
        print("Библиотека googletrans не найдена. Установите ее: pip install googletrans-py")
        exit()

    my_text_ru = "Привет, мир! Как твои дела сегодня?"
    my_text_en = "Hello, world! How are you doing today?"

    print("--- Перевод русского текста на языки по умолчанию (['en', 'ru']) ---")
    results_default = translate_to(my_text_ru)
    for lang, translation in results_default.items():
        print(f"{lang}: {translation}")

    print("\n--- Перевод английского текста на указанные языки ---")
    custom_langs = ['es', 'fr', 'de', 'ja', 'en'] # 'en' to check the original skill
    results_custom = translate_to(my_text_en, src_lang='en', target_langs=custom_langs)
    for lang, translation in results_custom.items():
        print(f"{lang}: {translation}")

    print("\n--- Перевод русского текста (автоопределение) на более широкий список языков ---")
    popular_langs = ['en', 'zh-cn', 'es', 'ar', 'pt', 'hi']
    results_popular = translate_to(my_text_ru, target_langs=popular_langs)
    for lang, translation in results_popular.items():
        print(f"{lang}: {translation}")

    print("\n--- Пример с некорректным списком языков (используется fallback) ---")
    results_fallback = translate_to(my_text_en, target_langs=[1, 'de', None])
    for lang, translation in results_fallback.items():
        print(f"{lang}: {translation}")

    print("\n--- Пример с пустым списком языков (используется fallback) ---")
    results_empty_list = translate_to(my_text_en, target_langs=[])
    for lang, translation in results_empty_list.items():
        print(f"{lang}: {translation}")