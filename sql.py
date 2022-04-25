import sqlite3
import os
import sys
from typing import List

class Database():
    def __init__(self, db_name: str):
        for c in db_name:
            if not c.isalnum() or c not in ' _-':
                raise Exception(f"'{db_name}' is not a valid filename")

        if not db_name.endswith(".db"):
            db_name += ".db"
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.setup_commands = []


    def __save(self):
        self.conn.commit()


    def execute(self, query: str, parameters=None):
        if parameters is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, parameters)
        self.__save()


    def executemany(self, query: str, parameters):
        self.cur.execute(query, parameters)
        self.__save()


    def get(self, query: str, parameters=None):
        self.execute(query, parameters)
        return self.cur.fetchall()


    def initialize(self, commands: List[str]):
        self.setup_commands = commands
        for command in self.setup_commands:
            self.execute(command)


    def reset(self):
        self.cur.execute("""SELECT name 
                            FROM sqlite_master 
                            WHERE type = 'table' 
                            AND name NOT LIKE 'sqlite_%'""")
        names = self.cur.fetchall()
        for table_name in names:
            self.cur.execute("DROP TABLE ?", (table_name,))


db = Database("chungus")
