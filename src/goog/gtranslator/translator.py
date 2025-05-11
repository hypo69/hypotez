from googletrans import Translator, LANGUAGES

# Этот список используется как fallback, если предоставленный target_langs некорректен
# или если бы не было значения по умолчанию для target_langs.
# Можно выбрать 10 самых популярных, как в первоначальном запросе:
FALLBACK_DEFAULT_LANG_CODES = [
    'en', 'zh-cn', 'hi', 'es', 'fr', 'ar', 'ru', 'pt', 'de', 'ja'
]
# Или использовать более широкий список:
# FALLBACK_DEFAULT_LANG_CODES = [
# 'en', 'zh-cn', 'de', 'it', 'es', 'fr', 'ar', 'ru', 'pt', 'ko',
# 'tr', 'he', 'pl', 'uk', 'nl', 'cs', 'sv', 'da', 'ja'
# ]

def translate_to(text_to_translate: str,
                           src_lang: str = 'auto',
                           target_langs: list = ['en', 'ru']): # Значение по умолчанию согласно вашему запросу
    """
    Переводит текст на указанные языки.

    :param text_to_translate: Текст для перевода.
    :param src_lang: Исходный язык текста (например, 'en', 'ru', 'auto' для автоопределения).
    :param target_langs: Список кодов языков для перевода (например, ['en', 'es', 'fr']).
                         По умолчанию ['en', 'ru']. Если передан пустой список или
                         некорректное значение, используется fallback-список.
    :return: Словарь, где ключ - код языка (из target_langs), значение - переведенный текст или сообщение об ошибке.
    """
    translator = Translator()
    translations = {}

    # Логика определения исходного языка и его отображения
    determined_source_lang_code = src_lang
    if src_lang == 'auto':
        source_lang_name_display = "auto (ожидание определения)"
    else:
        source_lang_name_display = LANGUAGES.get(src_lang, src_lang)

    if src_lang == 'auto':
        try:
            detected = translator.detect(text_to_translate)
            determined_source_lang_code = detected.lang
            # Обновляем отображаемое имя исходного языка после успешного определения
            source_lang_name_display = f"{LANGUAGES.get(determined_source_lang_code, determined_source_lang_code)} (обнаружено)"
            print(f"Обнаружен исходный язык: {LANGUAGES.get(determined_source_lang_code, determined_source_lang_code)} ({determined_source_lang_code})")
        except Exception as e:
            print(f"Не удалось определить исходный язык: {e}. Используется 'auto' для перевода.")
            determined_source_lang_code = 'auto' # Остается 'auto' для сравнения
            source_lang_name_display = "auto (определение не удалось)"

    print(f"\nОригинал ({source_lang_name_display}): {text_to_translate}\n")

    # Определяем итоговый список целевых языков для перевода
    final_target_codes = []
    # Проверяем, что target_langs - это непустой список строк
    if isinstance(target_langs, list) and len(target_langs) > 0 and all(isinstance(lang, str) for lang in target_langs):
        final_target_codes = target_langs
        print(f"Перевод будет выполнен на указанные языки: {final_target_codes}")
    else:
        final_target_codes = FALLBACK_DEFAULT_LANG_CODES
        if not isinstance(target_langs, list):
            user_input_type = type(target_langs).__name__
            print(f"Параметр target_langs должен быть списком, получен {user_input_type} ('{target_langs}'). "
                  f"Используется fallback список ({len(final_target_codes)} языков): {final_target_codes}")
        elif len(target_langs) == 0:
            print(f"Передан пустой список target_langs. "
                  f"Используется fallback список ({len(final_target_codes)} языков): {final_target_codes}")
        else: # Список не пустой, но содержит не строки
             print(f"Список target_langs содержит некорректные значения. "
                  f"Используется fallback список ({len(final_target_codes)} языков): {final_target_codes}")


    for lang_code in final_target_codes:
        # Дополнительная проверка, если fallback логика выше не отсеяла все некорректные коды
        if not isinstance(lang_code, str) or not lang_code.strip():
            print(f"Пропущен некорректный или пустой код языка в списке: '{lang_code}'")
            # Ключом может быть сам некорректный lang_code для отладки
            translations[str(lang_code)] = "Некорректный код языка предоставлен"
            continue

        # Не переводим на тот же язык, если он был определен (или задан) и совпадает
        if lang_code == determined_source_lang_code and determined_source_lang_code != 'auto':
            translations[lang_code] = f"{text_to_translate} (Оригинал)"
            continue
        try:
            # В API всегда передаем src_lang, который пользователь задал (может быть 'auto')
            # Библиотека сама справится с 'auto'
            translated_obj = translator.translate(text_to_translate, src=src_lang, dest=lang_code)
            translations[lang_code] = translated_obj.text
        except Exception as e:
            target_lang_name_display = LANGUAGES.get(lang_code, lang_code)
            translations[lang_code] = f"Ошибка перевода на {target_lang_name_display} ({lang_code}): {e}"

    return translations

# Пример использования:
if __name__ == "__main__":
    # Убедитесь, что библиотека установлена: pip install googletrans-py
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
    custom_langs = ['es', 'fr', 'de', 'ja', 'en'] # 'en' для проверки пропуска оригинала
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