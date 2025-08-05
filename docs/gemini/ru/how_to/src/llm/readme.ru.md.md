## \file hypotez/src/llm/readme.ru.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль llm
===============================================================
Модуль llm реализует основные функции для работы с большими языковыми моделями (LLM).
Он предоставляет инструменты для обработки текста, генерации ответов, перевода и других задач, связанных с обработкой естественного языка. 

.. module:: src.llm
"""
<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/readme.ru.md'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/readme.ru.md'>src</A> /
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/llm/readme.ru.md'>llm</A> 
</TD>

<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/llm/README.MD'>English</A>
</TD>
</TABLE>

## Модуль llm
Модуль **llm** предоставляет функциональность для взаимодействия с моделями LLM. 
Он включает в себя различные инструменты для:

* **Обработки текста**: 
    * Токенизация, лемматизация, стеминг.
    * Анализ тональности.
    * Извлечение ключевых слов.
    * Классификация текста.
* **Генерации текста**:
    * Создание текстов различных типов (статьи, истории, описания).
    * Перефразирование текста.
    * Автоматическое завершение текста.
* **Перевода**: 
    * Перевод текста с одного языка на другой.
* **Интеграции с различными API LLM**:
    * OpenAI (GPT, DALL-E)
    * Google AI (PaLM)
    * Anthropic (Claude)
    * Hugging Face

### **Подмодули**:
Модуль **llm** включает в себя следующие подмодули:

1. **anthropic**  \n
   Обеспечивает интеграцию с моделями ИИ Anthropic, что позволяет выполнять задачи, связанные с продвинутым пониманием языка и генерацией ответов.
   [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/anthropic/readme.ru.md)
2. **dialogflow**  \n
   Интегрируется с Google Dialogflow, поддерживает обработку естественного языка (NLU) и функции разговорного ИИ для создания интерактивных приложений.
   [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/dialogflow/readme.ru.md)
3. **gemini**  \n
   Управляет соединениями с моделями ИИ Gemini, предоставляя поддержку для приложений, которые требуют уникальных возможностей ИИ Gemini.
   [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/gemini/readme.ru.md)
4. **helicone**  \n
   Подключается к моделям Helicone, предоставляя доступ к специализированным функциям для настройки решений на базе ИИ.
      [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/helicone/readme.ru.md)
5. **llama**  \n
   Интерфейс для LLaMA (Large Language Model Meta AI), предназначен для задач, связанных с пониманием и генерацией естественного языка в различных приложениях.
      [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/llama/readme.ru.md)
6. **myai**  \n
   Кастомный подмодуль ИИ, разработанный для специализированных конфигураций моделей и реализации, обеспечивающий уникальные функции ИИ, специфичные для проекта.
      [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/myai/readme.ru.md)
7. **openai**  \n
   Интегрируется с API OpenAI, предоставляя доступ к их набору моделей (например, GPT) для таких задач, как генерация текста, классификация, перевод и другие.
      [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/openai/readme.ru.md)
8. **tiny_troupe**  \n
   Обеспечивает интеграцию с моделями ИИ от Microsoft, предлагая решения для обработки естественного языка и задач анализа данных с использованием маленьких моделей, оптимизированных для производительности.
      [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/tiny_troupe/readme.ru.md)
9. **revai**  \n
    Интегрируется с моделью от rev.com, которая специализируется на работе с аудиофайлами, такими как записи переговоров, совещаний, звонков и других аудио-материалов.
    [Перейти к модулю](https://github.com/hypo69/hypotez/blob/master/src/llm/revai/readme.ru.md)
    <HR>
10. **prompts**  \n
   Системные и командные промпты в формате `markdown`, для моделей ИИ.

### Вклад
Вклад приветствуется! Не стесняйтесь отправлять pull request или открывать issue, если вы столкнулись с какими-либо проблемами или имеете предложения по улучшению.

### Лицензия
Этот проект лицензирован под MIT License. Подробности смотрите в файле [LICENSE](../../LICENSE).