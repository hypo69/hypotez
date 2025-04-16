# Управление веб-сайтами PrestaShop

Этот файл `README` объясняет структуру и использование ваших веб-сайтов PrestaShop, а также хранение и использование ключей API.

## Веб-сайты

Ваши веб-сайты PrestaShop:

1.  [e-cat.co.il](https://e-cat.co.il)
2.  [emil-design.com](https://emil-design.com)
3.  [sergey.mymaster.co.il](https://sergey.mymaster.co.il)

Каждый из этих веб-сайтов использует API для взаимодействия с различными параметрами и функциями.

## Хранение ключей API

Ключи API для каждого веб-сайта хранятся в файле `credentials.kdbx`. Этот файл является безопасной базой данных паролей и содержит следующие данные для каждого веб-сайта:

*   URL веб-сайта
*   Ключ API
*   Дополнительные метаданные (если необходимо)

Для работы с ключами из файла используйте менеджер паролей, поддерживающий формат `.kdbx`, такой как [KeePass](https://keepass.info/) или [KeePassXC](https://keepassxc.org/).

## Пример использования API

Чтобы подключиться к API одного из ваших веб-сайтов, следуйте шаблону ниже:

### Пример API-запроса

**Шаблон API-запроса:**

```bash
curl -X GET 'https://<SITE_URL>/api/<endpoint>' \
-H 'Authorization: Basic <base64(API_KEY)>'
```

**Объяснение параметров:**

*   `<SITE_URL>` — адрес веб-сайта, например, `e-cat.co.il`.
*   `<endpoint>` — конечная точка API (например, `products`, `customers`).
*   `<API_KEY>` — ключ API, закодированный в Base64.

### Пример вызова API

Чтобы получить список товаров с `e-cat.co.il`:

```bash
curl -X GET 'https://e-cat.co.il/api/products' \
-H 'Authorization: Basic <base64(API_KEY)>'
```

## Рекомендации по безопасности

*   Никогда не передавайте файл `credentials.kdbx` другим лицам. ❗
*   Убедитесь, что файл хранится в безопасном месте, доступном только вам. (Папка `secrets` в корне проекта исключена из `git`).
*   Регулярно обновляйте свои ключи API и пароли базы данных.

## Дополнительные ресурсы

Если у вас возникнут какие-либо проблемы или вопросы о подключении к API, обратитесь к [официальной документации PrestaShop API](https://devdocs.prestashop.com/), в которой представлена информация о доступных конечных точках и способах взаимодействия с ними.

[Root ↑](https://github.com/hypo69/hypotez/blob/master/readme.ru.md)
[src](https://github.com/hypo69/hypotez/blob/master/src/README.MD)
[endpoints](https://github.com/hypo69/hypotez/blob/master/src/endpoints/README.MD)
[Русский](https://github.com/hypo69/hypotez/blob/master/src/endpoints/prestashop/readme.ru.md)