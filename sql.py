import sqlite3
import os
import sys
from typing import List


class Database():

    """ Class representing a database with methods used to interact with and manipulate both the data contained within
    as well as the metadata concerning the structure of the database its self """

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
        """ Commits any changes made to the database by the connection into the file"""

        self.conn.commit()

    def execute(self, query: str, parameters=None):
        """ Execute a SQL command with optional parameters

        :param query: The query to send to the connection
        :param parameters: The parameters of the query to be sent
        """

        if parameters is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, parameters)
        self.__save()

    def executemany(self, query: str, parameters):
        """ Execute multiple SQL commands with optional parameters

        :param query: The query to send to the connection
        :param parameters: The parameters of the query to be sent
        """

        self.cur.execute(query, parameters)
        self.__save()

    def get(self, query: str, parameters=None):
        """ Retrieve a piece of data from the database and return it

        :param query: The query to send to the connection
        :param parameters: The parameters of the query to be sent
        :return: The result of the query returned by the connection
        """

        self.execute(query, parameters)
        return self.cur.fetchall()

    def initialize(self, commands: List[str]):
        self.setup_commands = commands
        for command in self.setup_commands:
            self.execute(command)

    def reset(self):
        """ Wipes the database of all of its data and tables """

        self.cur.execute("""SELECT name 
                            FROM sqlite_master 
                            WHERE type = 'table' 
                            AND name NOT LIKE 'sqlite_%'""")
        names = self.cur.fetchall()
        for table_name in names:
            self.cur.execute("DROP TABLE ?", (table_name,))


db = Database("chungus")
