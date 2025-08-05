## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода `setup.py`  является конфигурационным файлом для установки пакета `gpt4free`. Он определяет метаданные, зависимости, точки входа и другие настройки для проекта.

Шаги выполнения
-------------------------
1. **Определение метаданных**: Устанавливает имя проекта (`g4f`), версию (`G4F_VERSION`), автора (`Tekky`), контактную информацию (`support@g4f.ai`), описание (`The official gpt4free repository | various collection of powerful language models`) и др.
2. **Обработка README.md**: Считывает файл `README.md` и добавляет к описанию проекта.
3. **Определение зависимостей**: Определяет список обязательных (`INSTALL_REQUIRE`) и дополнительных (`EXTRA_REQUIRE`) зависимостей пакета. 
4. **Настройка точки входа**: Устанавливает точку входа для консольного скрипта `g4f`, который запускается командой `g4f`.
5. **Настройка проекта**: Устанавливает URL-адреса проекта, ключевые слова, классификаторы и др.

Пример использования
-------------------------

```python
# ... 
setup(
    name='g4f',
    version=os.environ.get("G4F_VERSION"),
    author='Tekky',
    author_email='<support@g4f.ai>',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    package_data={
        'g4f': [
            'g4f/interference/*', 
            'g4f/gui/client/*', 
            'g4f/gui/server/*', 
            'g4f/Provider/npm/*', 
            'g4f/local/models/*'
        ]
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    entry_points={
        'console_scripts': ['g4f=g4f.cli:main'],
    },
    url='https://github.com/xtekky/gpt4free',  # Link to your GitHub repository
    project_urls={
        'Source Code': 'https://github.com/xtekky/gpt4free',  # GitHub link
        'Bug Tracker': 'https://github.com/xtekky/gpt4free/issues',  # Link to issue tracker
    },
    # ... 
)
```