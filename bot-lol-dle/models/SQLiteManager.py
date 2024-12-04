import os
import sqlite3

from dotenv import load_dotenv

from models.DBManager import DBManager

load_dotenv()

class SQLiteManager(DBManager):
    def __init__(self, db_name:str = os.getenv("DATABASE")):
        """
        Initialise la connexion à la base de données SQLite.
        """
        super().__init__(f"{db_name}.db", bdd_method="sqlite")

    def connect(self):
        """
        Ouvre la connexion à la base de données.
        """
        try:
            self.connection = sqlite3.connect(self.database)
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion : {e}")
