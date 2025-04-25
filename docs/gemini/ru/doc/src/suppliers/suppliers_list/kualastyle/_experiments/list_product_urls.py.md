# Модуль для сбора URL-адресов продуктов Kualastyle

## Обзор

Данный модуль содержит список URL-адресов продуктов для интернет-магазина Kualastyle.

## Подробней

Список URL-адресов продуктов Kualastyle хранится в переменной `product_urls`. В этом модуле нет дополнительных функций или методов, это просто список URL-адресов, который используется в других частях проекта.

## Переменные

### `product_urls`

**Описание**: Список URL-адресов продуктов Kualastyle.

**Тип**: `list` 

**Примеры**: 

```python
# Получение первого URL-адреса из списка
first_url = product_urls[0]

# Вывод всех URL-адресов на экран
for url in product_urls:
    print(url)

# Проверка наличия определенного URL-адреса в списке
url_to_check = 'https://kualastyle.com/collections/%D7%A1%D7%A4%D7%95%D7%AA-%D7%9E%D7%A2%D7%95%D7%A6%D7%91%D7%95%D7%AA/products/verona'
if url_to_check in product_urls:
    print(f'URL {url_to_check} найден в списке.')
else:
    print(f'URL {url_to_check} не найден в списке.')
```