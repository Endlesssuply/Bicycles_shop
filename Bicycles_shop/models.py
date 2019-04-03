class UsersModel:
    """Сущность пользователей"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(20) UNIQUE,
                             password_hash VARCHAR(128),
                             email VARCHAR(20),
                             is_admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, email, is_admin=False):
        """Вставка новой записи"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        """Проверка, есть ли пользователь в системе"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        row = cursor.fetchone()
        return (True, row[2], row[0]) if row else (False,)

    def get(self, user_id):
        """Возврат пользователя по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех пользователей"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


class DealersModel:
    """Сущность дилерских центров"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dealers 
                            (dealer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20) UNIQUE,
                             address VARCHAR(128)
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, address):
        """Добавление дилерского центра"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO dealers 
                          (name, address) 
                          VALUES (?,?)''',
                       (name, address))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск дилерского центра по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, dealer_id):
        """Запрос дилерского центра по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers WHERE dealer_id = ?", (str(dealer_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех дилерских центров"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers")
        rows = cursor.fetchall()
        return rows

    def delete(self, dealer_id):
        """Удаление дилерского центра"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM dealers WHERE dealer_id = ?''', (str(dealer_id)))
        cursor.close()
        self.connection.commit()


class BicyclesModel:
    """Сущность велосипедов"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bicycles 
                            (bicycle_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             model VARCHAR(20),
                             price INTEGER,
                             weight INTEGER,
                             electric VARCHAR(20),
                             color VARCHAR(20),
                             dealer INTEGER
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, model, price, weight, electric, color, dealer):
        """Добавление велосипеда"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO bicycles 
                          (model, price, weight, electric, color, dealer) 
                          VALUES (?,?,?,?,?,?)''',
                       (model, str(price), str(weight), electric, color, str(dealer)))
        cursor.close()
        self.connection.commit()

    def exists(self, model):
        """Поиск велосипеда по модели"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bicycles WHERE model = ?",
                       model)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, bicycle_id):
        """Поиск велосипеда по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bicycles WHERE bicycle_id = ?", (str(bicycle_id)))
        row = cursor.fetchone()
        return row
    
    def get_id(self, model, price, weight, electric, color):
            cursor = self.connection.cursor()
            cursor.execute("SELECT bicycle_id FROM bicycles WHERE model = ? AND price = ? AND weight = ? AND electric = ? AND color = ? AND dealer = ?", (str(price), str(weight), electric, color))    

    def get_all(self):
        """Запрос всех велосипедов"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, bicycle_id FROM bicycles")
        rows = cursor.fetchall()
        return rows

    def delete(self, bicycle_id):
        """Удаление велосипеда"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM bicycles WHERE bicycle_id = ?''', (str(bicycle_id)))
        cursor.close()
        self.connection.commit()

    def get_by_price(self, start_price, end_price):
        """Запрос велосипедов по цене"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, bicycle_id FROM bicycles WHERE price >= ? AND price <= ?", (str(start_price), str(end_price)))
        row = cursor.fetchall()
        return row

    def get_by_dealer(self, dealer_id):
        """Запрос велосипедов по дилерскому центру"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, bicycle_id FROM bicycles WHERE dealer = ?", (str(dealer_id)))
        row = cursor.fetchall()
        return row
