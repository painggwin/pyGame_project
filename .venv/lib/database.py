import sqlite3
class upgradesDataBase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE upgrades(
                        upgrade text,
                        state integer
                        )""")
        self.conn.commit()
    def add(self, name):
        self.cursor.execute("INSERT INTO upgrades VALUES (?, ?)", (name, 0))
        self.conn.commit()
    def toggle(self,name):
        self.cursor.execute("UPDATE upgrades SET state=1 WHERE upgrade=?", (name,))
        self.conn.commit()
    def get(self,name):
        self.cursor.execute("SELECT * FROM upgrades WHERE upgrade=?", (name,))
        self.conn.commit()
        return self.cursor.fetchall()[0][1]
test = upgradesDataBase()
test.add("speed")
print(test.get("speed"))
test.toggle("speed")
print(test.get("speed"))
test.add("attack")
# test.toggle("attack")
# print(test.get("speed"))
print(test.get("attack"))

class upgradesDataBase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE stats(
                        stat text,
                        level integer
                        )""")
        self.conn.commit()
    def add(self, name, level):
        self.cursor.execute("INSERT INTO stats VALUES (?, ?)", (name, level))
        self.conn.commit()
    def update(self,name,level):
        self.cursor.execute("UPDATE stats SET level=? WHERE stat=?", (level,name))
        self.conn.commit()
    def get(self,name):
        self.cursor.execute("SELECT * FROM stats WHERE stat=?", (name,))
        self.conn.commit()
        return self.cursor.fetchall()[0][1]
