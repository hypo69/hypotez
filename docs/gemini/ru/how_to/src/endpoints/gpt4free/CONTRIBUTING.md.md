## Как добавить поддержку нового сайта в GPT4Free
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой инструкцию для разработчиков, как добавить поддержку нового сайта в проект GPT4Free.

Шаги выполнения
-------------------------
1. Выберите сайт из списка [sites-to-reverse](https://github.com/xtekky/gpt4free/issues/40), который вы хотите добавить.
2. Создайте новый файл в директории [./etc/unittest/](https://github.com/xtekky/gpt4free/tree/main/etc/unittest/) с кодом, реализующим реверсирование сайта.
3. Рефакторите код и добавьте его в директорию [./g4f](https://github.com/xtekky/gpt4free/tree/main/g4f).

Пример использования
-------------------------

```python
# Выберите сайт из списка [sites-to-reverse](https://github.com/xtekky/gpt4free/issues/40).
site = "example.com"

# Создайте новый файл в директории [./etc/unittest/](https://github.com/xtekky/gpt4free/tree/main/etc/unittest/) с кодом, реализующим реверсирование сайта.
# Например: ./etc/unittest/example_com.py

# Рефакторите код и добавьте его в директорию [./g4f](https://github.com/xtekky/gpt4free/tree/main/g4f).
# Например: ./g4f/example_com.py