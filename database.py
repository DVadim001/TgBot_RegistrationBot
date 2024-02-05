import sqlite3

connection = sqlite3.connect("catalog.db", check_same_thread=False)
sql = connection.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER,"
            "name TEXT,"
            "number TEXT,"
            "location TEXT);")


# Методы для пользователя
# Регистрация
def registration(id, name, number, location):
    sql.execute("INSERT INTO users VALUES(?, ?, ?, ?);", (id, name, number, location))
    connection.commit()


# Проверка на наличие пользователя в базе
def check_in_base(id):
    check = sql.execute("SELECT id FROM users WHERE id=?;", (id,))
    if check.fetchone():
        return True
    else:
        return False
