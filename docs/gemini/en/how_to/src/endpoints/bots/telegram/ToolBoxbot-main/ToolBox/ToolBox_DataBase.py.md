**Instructions for Generating Code Documentation**

How to Use This Code Block
========================================================================================

Description
-------------------------
The code implements a `DataBase` class that provides functionality for interacting with a SQLite database. 

Execution Steps
-------------------------
1. **Initialization:** The `__init__` method initializes the database connection, setting the database name, table name, and column titles and types.
2. **Database Creation:** The `create` method creates the table specified in the initialization if it doesn't already exist.
3. **Insert or Update Data:** The `insert_or_update_data` method adds a new record or updates an existing record in the database table. It takes the record ID and a dictionary of values. 
4. **Load Data:** The `load_data_from_db` method retrieves all data from the database table and returns it as a dictionary, where the keys are the record IDs and the values are dictionaries representing the record data.

Usage Example
-------------------------

```python
    base = DataBase(db_name="UsersData.db", table_name="users_data_table", titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]",
                        "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                        "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                        "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                        "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"})
    base.create() 
    db = base.load_data_from_db() 

    uid = input() 

    if uid != '':
        if "pro" in uid:
            db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 1.7*10**5, "outgoing_tokens": 5*10**5, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(months=1), "promocode": False, "ref": ""}
        elif 'admin' in uid:
            db[uid.split()[0]] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": True, "pro": True, "incoming_tokens": 100*10**5, "outgoing_tokens": 100*10**5, "free_requests": 1000, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(years=5), "promocode": False, "ref": ""}
        else:
            db[uid] = {"text": [0]*N, "sessions_messages": [], "some": False, "images": "", "free": False, "basic": False, "pro": False, "incoming_tokens": 0, "outgoing_tokens": 0, "free_requests": 10, "datetime_sub": datetime.now().replace(microsecond=0)+relativedelta(days=1), "promocode": False, "ref": ""}
        base.insert_or_update_data(uid.split()[0], db[uid.split()[0]])