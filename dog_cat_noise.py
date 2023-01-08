import sqlite3

class Animal:
    animal_total = 0

    def __init__(self, noise):
        self.noise = "NA"

    def get_noise(self):
        return self.noise

class Dog(Animal):
    def __init__(self, noise):
        super(Dog, self).__init__(noise)
        self.noise = noise

    def get_noise(self):
        return self.noise

class Cat(Animal):
    def __init__(self, noise):
        super(Cat, self).__init__(noise)
        self.noise = noise

    def get_noise(self):
        return self.noise

class SingletonDatabase:
    _instance = None

    def __init__(self):
        print("Constructor __init")
        self.name = "history.db"
        self.conn = self.get_conn(self.name)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls) #call only once
        return cls._instance

    @classmethod
    def get_conn(cls, name):
        conn = sqlite3.connect(name)
        conn.execute('''CREATE TABLE IF NOT EXISTS TABLE_HISTORY(COMMAND_ID INTEGER PRIMARY KEY AUTOINCREMENT, COMMAND TEXT);''')
        return conn

    def insert(self, noise):
        query = "INSERT INTO TABLE_HISTORY(COMMAND) VALUES('{}')".format(noise)
        self.conn.execute(query)
        self.conn.commit()

    def get_history(self):
        cursor = self.conn.execute('''SELECT COMMAND_ID, COMMAND FROM TABLE_HISTORY''')
        result = []
        for row in cursor:
            result.append([row[0], row[1]])
        return result

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    dog_noise = "Auau"
    cat_noise = "Miau"
    dog = Dog(dog_noise)
    cat = Cat(cat_noise)
    db = SingletonDatabase()

    value = 1
    while(value != 0):
        value = input("1-Cat, 2-Dog, 0-Exit, history to show all commands: ")
        try:
            value = int(value)
            #write in history file
            if value == 1:
                db.insert(cat.get_noise())
            elif value == 2:
                db.insert(dog.get_noise())
            else:
                value = 0
        except ValueError as ex:
            #show history or exit
            if str(value) == "history":
                print("Show history")
                history = db.get_history()
                for entry in history:
                    print("{}: {}".format(entry[0], entry[1]))
            else:
                value = 0
    db.close()
