# Модуль для работы с Mega.co.nz API
===============================================

Модуль предоставляет класс `Mega`, который используется для взаимодействия с API сервиса Mega.co.nz. 
Он позволяет выполнять различные операции, такие как авторизация, получение списка файлов, загрузка и скачивание файлов.

## Оглавление
- ## Классы
  - ### `Mega`
    - **Описание**: Класс для работы с Mega API.
    - **Атрибуты**:
      - `seqno`: Последовательный номер запроса API.
      - `sid`: Идентификатор сессии.
      - `master_key`: Основной ключ, используемый для шифрования/дешифрования данных.
      - `rsa_priv_key`: Частный ключ RSA, используемый для дешифрования сессионного ID.
      - `root_id`: Идентификатор корневой папки (Cloud Drive).
      - `inbox_id`: Идентификатор папки "Входящие".
      - `trashbin_id`: Идентификатор папки "Корзина".
    - **Методы**:
      - `api_req(data)`: Отправляет запрос к API Mega.
      - `login_user(email, password)`: Авторизация с использованием электронной почты и пароля.
      - `login_ephemeral()`: Создание временной учетной записи.
      - `_login_common(res, password)`: Общий метод для завершения авторизации.
      - `get_files()`: Получение списка файлов и папок.
      - `download_from_url(url)`: Скачивание файла по общедоступной ссылке.
      - `download_file(file_id, file_key, public=False, store_path=None)`: Скачивание файла по ID и ключу.
      - `get_public_url(file_id, file_key)`: Получение общедоступной ссылки на файл.
      - `uploadfile(filename, dst=None)`: Загрузка файла на Mega.
- ## Функции 
  - ### `prepare_key(key)`:
    - **Назначение**: Подготовка ключа для шифрования/дешифрования.
    - **Параметры**:
      - `key`: Ключ для подготовки.
    - **Возвращает**:
      - `list`: Подготовленный ключ.
  - ### `stringhash(email, password_aes)`:
    - **Назначение**: Вычисление хэша от электронной почты и пароля.
    - **Параметры**:
      - `email`: Электронная почта.
      - `password_aes`: Пароль, зашифрованный с помощью AES.
    - **Возвращает**:
      - `str`: Хэш-строка.
  - ### `encrypt_key(key, password_key)`:
    - **Назначение**: Шифрование ключа с использованием парольного ключа.
    - **Параметры**:
      - `key`: Ключ для шифрования.
      - `password_key`: Парочный ключ.
    - **Возвращает**:
      - `list`: Зашифрованный ключ.
  - ### `decrypt_key(enc_key, password)`:
    - **Назначение**: Дешифрование ключа с использованием пароля.
    - **Параметры**:
      - `enc_key`: Зашифрованный ключ.
      - `password`: Пароль.
    - **Возвращает**:
      - `list`: Дешифрованный ключ.
  - ### `enc_attr(attributes, key)`:
    - **Назначение**: Шифрование атрибутов файла.
    - **Параметры**:
      - `attributes`: Словарь атрибутов.
      - `key`: Ключ для шифрования.
    - **Возвращает**:
      - `bytes`: Зашифрованные атрибуты.
  - ### `dec_attr(attributes, key)`:
    - **Назначение**: Дешифрование атрибутов файла.
    - **Параметры**:
      - `attributes`: Зашифрованные атрибуты.
      - `key`: Ключ для дешифрования.
    - **Возвращает**:
      - `dict`: Дешифрованные атрибуты.
  - ### `aes_cbc_encrypt_a32(data, key)`:
    - **Назначение**: Шифрование данных с использованием AES в режиме CBC.
    - **Параметры**:
      - `data`: Данные для шифрования.
      - `key`: Ключ для шифрования.
    - **Возвращает**:
      - `list`: Зашифрованные данные.
  - ### `a32_to_str(data)`:
    - **Назначение**: Преобразование данных из формата A32 в строку.
    - **Параметры**:
      - `data`: Данные в формате A32.
    - **Возвращает**:
      - `str`: Строка.
  - ### `str_to_a32(data)`:
    - **Назначение**: Преобразование строки в формат A32.
    - **Параметры**:
      - `data`: Строка.
    - **Возвращает**:
      - `list`: Данные в формате A32.
  - ### `a32_to_base64(data)`:
    - **Назначение**: Преобразование данных из формата A32 в Base64.
    - **Параметры**:
      - `data`: Данные в формате A32.
    - **Возвращает**:
      - `str`: Base64-строка.
  - ### `base64_to_a32(data)`:
    - **Назначение**: Преобразование Base64-строки в формат A32.
    - **Параметры**:
      - `data`: Base64-строка.
    - **Возвращает**:
      - `list`: Данные в формате A32.
  - ### `mpi2int(data)`:
    - **Назначение**: Преобразование данных из формата MPI в целое число.
    - **Параметры**:
      - `data`: Данные в формате MPI.
    - **Возвращает**:
      - `int`: Целое число.
  - ### `base64urlencode(data)`:
    - **Назначение**: Кодирование данных в Base64URL.
    - **Параметры**:
      - `data`: Данные для кодирования.
    - **Возвращает**:
      - `str`: Кодированная Base64URL-строка.
  - ### `base64urldecode(data)`:
    - **Назначение**: Декодирование Base64URL-строки.
    - **Параметры**:
      - `data`: Base64URL-строка для декодирования.
    - **Возвращает**:
      - `bytes`: Декодированные данные.
  - ### `get_chunks(file_size)`:
    - **Назначение**: Разделение файла на чанки для загрузки/скачивания.
    - **Параметры**:
      - `file_size`: Размер файла в байтах.
    - **Возвращает**:
      - `dict`: Словарь, содержащий информацию о чанках.
- ## Исключения
  - ### `MegaRequestException`:
    - **Описание**: Исключение, возникающее при ошибке запроса к API Mega.
  - ### `MegaIncorrectPasswordExcetion`:
    - **Описание**: Исключение, возникающее при неверном вводе электронной почты и/или пароля.

## Классы

### `Mega`
```python
class Mega(object):
    """Класс для работы с Mega API.

    Attributes:
        seqno (int): Последовательный номер запроса API.
        sid (str): Идентификатор сессии.
        master_key (list): Основной ключ, используемый для шифрования/дешифрования данных.
        rsa_priv_key (list): Частный ключ RSA, используемый для дешифрования сессионного ID.
        root_id (str): Идентификатор корневой папки (Cloud Drive).
        inbox_id (str): Идентификатор папки "Входящие".
        trashbin_id (str): Идентификатор папки "Корзина".

    Methods:
        api_req(data): Отправляет запрос к API Mega.
        login_user(email, password): Авторизация с использованием электронной почты и пароля.
        login_ephemeral(): Создание временной учетной записи.
        _login_common(res, password): Общий метод для завершения авторизации.
        get_files(): Получение списка файлов и папок.
        download_from_url(url): Скачивание файла по общедоступной ссылке.
        download_file(file_id, file_key, public=False, store_path=None): Скачивание файла по ID и ключу.
        get_public_url(file_id, file_key): Получение общедоступной ссылки на файл.
        uploadfile(filename, dst=None): Загрузка файла на Mega.
    """
    def __init__(self):
        """Инициализация класса Mega."""
        self.seqno = random.randint(0, 0xFFFFFFFF)
        self.sid = None

    @classmethod
    def from_credentials(cls, email, password):
        """Создание экземпляра Mega с использованием электронной почты и пароля.

        Args:
            email (str): Электронная почта.
            password (str): Пароль.

        Returns:
            Mega: Экземпляр класса Mega.
        """
        inst = cls()
        inst.login_user(email, password)
        return inst

    @classmethod
    def from_ephemeral(cls):
        """Создание экземпляра Mega с использованием временной учетной записи.

        Returns:
            Mega: Экземпляр класса Mega.
        """
        inst = cls()
        inst.login_ephemeral()
        return inst

    def api_req(self, data):
        """Отправляет запрос к API Mega.

        Args:
            data (dict): Данные для отправки.

        Returns:
            dict: Ответ от API Mega.

        Raises:
            MegaRequestException: Если возникла ошибка при отправке запроса.
        """
        params = {'id': self.seqno}
        self.seqno += 1
        if self.sid:
            params.update({'sid': self.sid})
        data = json.dumps([data])
        req = requests.post(
            'https://g.api.mega.co.nz/cs', params=params, data=data)
        json_data = req.json()
        if isinstance(json_data, int):
            raise MegaRequestException(json_data)
        return json_data[0]

    def login_user(self, email, password):
        """Авторизация с использованием электронной почты и пароля.

        Args:
            email (str): Электронная почта.
            password (str): Пароль.

        Raises:
            MegaIncorrectPasswordExcetion: Если введены неверные данные.
        """
        password_aes = prepare_key(str_to_a32(password))
        uh = stringhash(email, password_aes)
        res = self.api_req({'a': 'us', 'user': email, 'uh': uh})
        self._login_common(res, password_aes)

    def login_ephemeral(self):
        """Создание временной учетной записи.
        """
        random_master_key = [random.randint(0, 0xFFFFFFFF)] * 4
        random_password_key = [random.randint(0, 0xFFFFFFFF)] * 4
        random_session_self_challenge = [random.randint(0, 0xFFFFFFFF)] * 4
        user_handle = self.api_req({
            'a': 'up',
            'k': a32_to_base64(encrypt_key(random_master_key,
                                           random_password_key)),
            'ts': base64urlencode(a32_to_str(random_session_self_challenge) +
                                  a32_to_str(encrypt_key(
                                      random_session_self_challenge,
                                      random_master_key)))
        })
        res = self.api_req({'a': 'us', 'user': user_handle})
        self._login_common(res, random_password_key)

    def _login_common(self, res, password):
        """Общий метод для завершения авторизации.

        Args:
            res (dict): Ответ от API Mega.
            password (list): Пароль, зашифрованный с помощью AES.

        Raises:
            MegaIncorrectPasswordExcetion: Если введены неверные данные.
        """
        if res in (-2, -9):
            raise MegaIncorrectPasswordExcetion(
                "Incorrect e-mail and/or password.")

        enc_master_key = base64_to_a32(res['k'])
        self.master_key = decrypt_key(enc_master_key, password)
        if 'tsid' in res:
            tsid = base64urldecode(res['tsid'])
            key_encrypted = a32_to_str(
                encrypt_key(str_to_a32(tsid[:16]), self.master_key))
            if key_encrypted == tsid[-16:]:
                self.sid = res['tsid']
        elif 'csid' in res:
            enc_rsa_priv_key = base64_to_a32(res['privk'])
            rsa_priv_key = decrypt_key(enc_rsa_priv_key, self.master_key)

            privk = a32_to_str(rsa_priv_key)
            self.rsa_priv_key = [0, 0, 0, 0]

            for i in range(4):
                l = ((privk[0] * 256 + privk[1] + 7) // 8) + 2
                self.rsa_priv_key[i] = mpi2int(privk[:l])
                privk = privk[l:]

            enc_sid = mpi2int(base64urldecode(res['csid']))
            decrypter = RSA.construct(
                (self.rsa_priv_key[0] * self.rsa_priv_key[1],
                 0,
                 self.rsa_priv_key[2],
                 self.rsa_priv_key[0],
                 self.rsa_priv_key[1]))
            sid = '%x' % decrypter.key._decrypt(enc_sid)
            sid = binascii.unhexlify(
                '0' + sid if len(sid) % 2 else sid)
            self.sid = base64urlencode(sid[:43])

    def get_files(self):
        """Получение списка файлов и папок.

        Returns:
            dict: Словарь, содержащий информацию о файлах и папках.
        """
        files_data = self.api_req({'a': 'f', 'c': 1})
        for file in files_data['f']:
            if file['t'] in (0, 1):
                key = file['k'].split(':')[1]
                key = decrypt_key(base64_to_a32(key), self.master_key)
                # file
                if file['t'] == 0:
                    k = (key[0] ^ key[4],
                         key[1] ^ key[5],
                         key[2] ^ key[6],
                         key[3] ^ key[7])
                # directory
                else:
                    k = key
                attributes = base64urldecode(file['a'])
                attributes = dec_attr(attributes, k)
                file['a'] = attributes
                file['k'] = key
            # Root ("Cloud Drive")
            elif file['t'] == 2:
                self.root_id = file['h']
            # Inbox
            elif file['t'] == 3:
                self.inbox_id = file['h']
            # Trash Bin
            elif file['t'] == 4:
                self.trashbin_id = file['h']
        return files_data

    def download_from_url(self, url):
        """Скачивание файла по общедоступной ссылке.

        Args:
            url (str): Общедоступная ссылка на файл.

        Returns:
            str: Имя скачанного файла.

        Raises:
            ValueError: Если URL не содержит ID файла и ключа.
        """
        url_object = URLObject(url)
        file_id, file_key = url_object.fragment[1:].split('!')

        #return the filename
        return self.download_file(file_id, file_key, public=True)

    def download_file(self, file_id, file_key, public=False, store_path=None):
        """Скачивание файла по ID и ключу.

        Args:
            file_id (str): ID файла.
            file_key (str): Ключ файла.
            public (bool): Флаг, указывающий на то, является ли файл общедоступным.
            store_path (str): Путь для сохранения файла.

        Returns:
            str: Имя скачанного файла.

        Raises:
            ValueError: Если MAC не совпадает.
        """
        if public:
            file_key = base64_to_a32(file_key)
            file_data = self.api_req({'a': 'g', 'g': 1, 'p': file_id})
        else:
            file_data = self.api_req({'a': 'g', 'g': 1, 'n': file_id})

        k = (file_key[0] ^ file_key[4],
             file_key[1] ^ file_key[5],
             file_key[2] ^ file_key[6],
             file_key[3] ^ file_key[7])
        iv = file_key[4:6] + (0, 0)
        meta_mac = file_key[6:8]

        file_url = file_data['g']
        file_size = file_data['s']
        attributes = base64urldecode(file_data['at'])
        attributes = dec_attr(attributes, k)
        file_name = attributes['n']

        infile = requests.get(file_url, stream=True).raw
        if store_path:
            file_name = os.path.join(store_path, file_name)
        outfile = open(file_name, 'wb')

        counter = Counter.new(
            128, initial_value=((iv[0] << 32) + iv[1]) << 64)
        decryptor = AES.new(a32_to_str(k), AES.MODE_CTR, counter=counter)

        file_mac = (0, 0, 0, 0)
        for chunk_start, chunk_size in sorted(get_chunks(file_size).items()):
            chunk = infile.read(chunk_size)
            chunk = decryptor.decrypt(chunk)
            outfile.write(chunk)

            chunk_mac = [iv[0], iv[1], iv[0], iv[1]]
            for i in range(0, len(chunk), 16):
                block = chunk[i:i+16]
                if len(block) % 16:
                    block += b'\x00' * (16 - (len(block) % 16))
                block = str_to_a32(block)
                chunk_mac = [
                    chunk_mac[0] ^ block[0],
                    chunk_mac[1] ^ block[1],
                    chunk_mac[2] ^ block[2],
                    chunk_mac[3] ^ block[3]
                ]
                chunk_mac = aes_cbc_encrypt_a32(chunk_mac, k)

            file_mac = [
                file_mac[0] ^ chunk_mac[0],
                file_mac[1] ^ chunk_mac[1],
                file_mac[2] ^ chunk_mac[2],
                file_mac[3] ^ chunk_mac[3]
            ]
            file_mac = aes_cbc_encrypt_a32(file_mac, k)

        outfile.close()

        # Integrity check
        if (file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3]) != meta_mac:
            raise ValueError('MAC mismatch')

        return file_name

    def get_public_url(self, file_id, file_key):
        """Получение общедоступной ссылки на файл.

        Args:
            file_id (str): ID файла.
            file_key (list): Ключ файла.

        Returns:
            str: Общедоступная ссылка на файл.
        """
        public_handle = self.api_req({'a': 'l', 'n': file_id})
        decrypted_key = a32_to_base64(file_key)
        return 'http://mega.co.nz/#!%s!%s' % (public_handle, decrypted_key)

    def uploadfile(self, filename, dst=None):
        """Загрузка файла на Mega.

        Args:
            filename (str): Имя файла для загрузки.
            dst (str): ID папки для загрузки файла.

        Returns:
            dict: Ответ от API Mega.

        Raises:
            Exception: Если возникла ошибка при загрузке файла.
        """
        if not dst:
            root_id = getattr(self, 'root_id', None)
            if root_id == None:
                self.get_files()
            dst = self.root_id
        infile = open(filename, 'rb')
        size = os.path.getsize(filename)
        ul_url = self.api_req({'a': 'u', 's': size})['p']

        ul_key = [random.randint(0, 0xFFFFFFFF) for _ in range(6)]
        counter = Counter.new(
            128, initial_value=((ul_key[4] << 32) + ul_key[5]) << 64)
        encryptor = AES.new(
            a32_to_str(ul_key[:4]),
            AES.MODE_CTR,
            counter=counter)

        file_mac = [0, 0, 0, 0]
        for chunk_start, chunk_size in sorted(get_chunks(size).items()):
            chunk = infile.read(chunk_size)

            chunk_mac = [ul_key[4], ul_key[5], ul_key[4], ul_key[5]]
            for i in range(0, len(chunk), 16):
                block = chunk[i:i+16]
                if len(block) % 16:
                    block += b'\x00' * (16 - len(block) % 16)
                block = str_to_a32(block)
                chunk_mac = [chunk_mac[0] ^ block[0],
                             chunk_mac[1] ^ block[1],
                             chunk_mac[2] ^ block[2],
                             chunk_mac[3] ^ block[3]]
                chunk_mac = aes_cbc_encrypt_a32(chunk_mac, ul_key[:4])

            file_mac = [file_mac[0] ^ chunk_mac[0],
                        file_mac[1] ^ chunk_mac[1],
                        file_mac[2] ^ chunk_mac[2],
                        file_mac[3] ^ chunk_mac[3]]
            file_mac = aes_cbc_encrypt_a32(file_mac, ul_key[:4])

            chunk = encryptor.encrypt(chunk)
            url = '%s/%s' % (ul_url, str(chunk_start))
            outfile = requests.post(url, data=chunk, stream=True).raw

            # assume utf-8 encoding. Maybe this entire section can be simplified
            # by not looking at the raw output
            # (http://docs.python-requests.org/en/master/user/advanced/#body-content-workflow)

            completion_handle = outfile.read().decode('utf-8')
        infile.close()

        meta_mac = (file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3])

        attributes = {'n': os.path.basename(filename)}
        enc_attributes = base64urlencode(enc_attr(attributes, ul_key[:4]))
        key = [ul_key[0] ^ ul_key[4],
               ul_key[1] ^ ul_key[5],
               ul_key[2] ^ meta_mac[0],
               ul_key[3] ^ meta_mac[1],
               ul_key[4], ul_key[5],
               meta_mac[0], meta_mac[1]]
        encrypted_key = a32_to_base64(encrypt_key(key, self.master_key))
        data = self.api_req({'a': 'p', 't': dst, 'n': [
            {'h': completion_handle,
             't': 0,
             'a': enc_attributes,
             'k': encrypted_key}]})
        return data
```

## Функции

### `prepare_key(key)`
```python
def prepare_key(key):
    """Подготовка ключа для шифрования/дешифрования.

    Args:
        key (list): Ключ для подготовки.

    Returns:
        list: Подготовленный ключ.
    """
    ...
```
### `stringhash(email, password_aes)`
```python
def stringhash(email, password_aes):
    """Вычисление хэша от электронной почты и пароля.

    Args:
        email (str): Электронная почта.
        password_aes (list): Пароль, зашифрованный с помощью AES.

    Returns:
        str: Хэш-строка.
    """
    ...
```
### `encrypt_key(key, password_key)`
```python
def encrypt_key(key, password_key):
    """Шифрование ключа с использованием парольного ключа.

    Args:
        key (list): Ключ для шифрования.
        password_key (list): Парочный ключ.

    Returns:
        list: Зашифрованный ключ.
    """
    ...
```
### `decrypt_key(enc_key, password)`
```python
def decrypt_key(enc_key, password):
    """Дешифрование ключа с использованием пароля.

    Args:
        enc_key (list): Зашифрованный ключ.
        password (list): Пароль.

    Returns:
        list: Дешифрованный ключ.
    """
    ...
```
### `enc_attr(attributes, key)`
```python
def enc_attr(attributes, key):
    """Шифрование атрибутов файла.

    Args:
        attributes (dict): Словарь атрибутов.
        key (list): Ключ для шифрования.

    Returns:
        bytes: Зашифрованные атрибуты.
    """
    ...
```
### `dec_attr(attributes, key)`
```python
def dec_attr(attributes, key):
    """Дешифрование атрибутов файла.

    Args:
        attributes (bytes): Зашифрованные атрибуты.
        key (list): Ключ для дешифрования.

    Returns:
        dict: Дешифрованные атрибуты.
    """
    ...
```
### `aes_cbc_encrypt_a32(data, key)`
```python
def aes_cbc_encrypt_a32(data, key):
    """Шифрование данных с использованием AES в режиме CBC.

    Args:
        data (list): Данные для шифрования.
        key (list): Ключ для шифрования.

    Returns:
        list: Зашифрованные данные.
    """
    ...
```
### `a32_to_str(data)`
```python
def a32_to_str(data):
    """Преобразование данных из формата A32 в строку.

    Args:
        data (list): Данные в формате A32.

    Returns:
        str: Строка.
    """
    ...
```
### `str_to_a32(data)`
```python
def str_to_a32(data):
    """Преобразование строки в формат A32.

    Args:
        data (str): Строка.

    Returns:
        list: Данные в формате A32.
    """
    ...
```
### `a32_to_base64(data)`
```python
def a32_to_base64(data):
    """Преобразование данных из формата A32 в Base64.

    Args:
        data (list): Данные в формате A32.

    Returns:
        str: Base64-строка.
    """
    ...
```
### `base64_to_a32(data)`
```python
def base64_to_a32(data):
    """Преобразование Base64-строки в формат A32.

    Args:
        data (str): Base64-строка.

    Returns:
        list: Данные в формате A32.
    """
    ...
```
### `mpi2int(data)`
```python
def mpi2int(data):
    """Преобразование данных из формата MPI в целое число.

    Args:
        data (bytes): Данные в формате MPI.

    Returns:
        int: Целое число.
    """
    ...
```
### `base64urlencode(data)`
```python
def base64urlencode(data):
    """Кодирование данных в Base64URL.

    Args:
        data (bytes): Данные для кодирования.

    Returns:
        str: Кодированная Base64URL-строка.
    """
    ...
```
### `base64urldecode(data)`
```python
def base64urldecode(data):
    """Декодирование Base64URL-строки.

    Args:
        data (str): Base64URL-строка для декодирования.

    Returns:
        bytes: Декодированные данные.
    """
    ...
```
### `get_chunks(file_size)`
```python
def get_chunks(file_size):
    """Разделение файла на чанки для загрузки/скачивания.

    Args:
        file_size (int): Размер файла в байтах.

    Returns:
        dict: Словарь, содержащий информацию о чанках.
    """
    ...
```

## Исключения

### `MegaRequestException`
```python
class MegaRequestException(Exception):
    """Исключение, возникающее при ошибке запроса к API Mega."""
    ...
```
### `MegaIncorrectPasswordExcetion`
```python
class MegaIncorrectPasswordExcetion(Exception):
    """Исключение, возникающее при неверном вводе электронной почты и/или пароля."""
    ...