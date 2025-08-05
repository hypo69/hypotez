## \file /hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/README.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module::  hypotez.src.endpoints.bots.telegram.ToolBoxbot-main.README
:platform: Windows, Unix
:synopsis: 

This module provides functions to generate a welcome message for the Toolbox Telegram bot.
"""

## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода генерирует приветственное сообщение для бота Toolbox в Telegram. Сообщение содержит информацию о возможностях бота,  его преимуществах и приглашение к использованию.

### Шаги выполнения
-------------------------
1. **Генерирует HTML-код** с заголовком `<h1>Toolbox AI</h1>` и подзаголовком `<h3>🛠 Welcome to Toolbox! This is a universal assistant that can generate content for various work tasks!</h3>`.
2. **Добавляет абзац** с описанием бота как универсального помощника для генерации контента для различных задач.
3. **Перечисляет возможности бота:**
    - **Генерация уникальных текстов** для SMM, email-рассылок, SEO-продвижения, рекламных кампаний и т. д.
    - **Генерация креативных идей** для реализации.
    - **Генерация изображений** на основе описания.
    - **Транскрипция подкастов, вебинаров и видео**.
4. **Приглашает пользователя попробовать бот** и выбрать нужную команду.
5. **Указывает, что пользователю доступно 5 бесплатных генераций** для ознакомления с сервисом.
6. **Предлагает выбрать тарифный план** после исчерпания бесплатных генераций.

### Пример использования
-------------------------

```python
                <h1>Toolbox AI</h1>
<h3>🛠 Welcome to Toolbox! This is a universal assistant that can generate content for various work tasks!</h3>

<p>With Toolbox, you always have powerful neural network-based tools at your fingertips for writing compelling texts, generating creative ideas, and creating visual content. Forget about tasteless templates and the agony of creativity!</p>

<p>🖋 Thanks to neural network models, you can easily create unique texts for SMM, email newsletters, SEO promotion, advertising campaigns, and much more. Just <b>choose the task you need</b>, write the <b>input</b>, and get the <b>ready-made content</b> as a result.</p>

<p>💡 Toolbox will easily brainstorm and suggest fresh creative concepts for implementation.</p>

<p>🖼 In addition to texts, the bot also allows you to generate images based on a description. Create visual content for posts, banners, illustrations from scratch - without photo banks and designers.</p>

<p>🎙 Save time and automate the transcription of podcasts, webinars, and videos using the built-in function.</p>

<p>Ready to try Toolbox and simplify your life? Just choose the command you need. I'll be happy to help with any task!</p>

<p>P.S. You have <b>5 free generations</b> to get acquainted with the service. Then you can choose a tariff plan that covers all your work tasks!</p>

                ```