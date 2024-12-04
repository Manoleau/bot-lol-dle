import os
import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
load_dotenv()

from models.DBManager import DBManager


class MySQLManager(DBManager):
    def __init__(self):
        """
        Initialise la connexion à la base de données MySQL.
        """
        super().__init__(
            database=os.getenv("DATABASE"),
            host=os.getenv("MYSQL_HOST"),
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            user="root",
            bdd_method=os.getenv("DB_METHOD")
        )

    def connect(self):
        """Établit la connexion à la base de données."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

        except Error as e:
            print(f"Erreur lors de la connexion : {e}")
            self.connection = None

    def insert_many(self, table:str, attributs:list[str], params:list[tuple]):
        ""
    def fetch_results(self, query, params=None) -> list[tuple]:
        """
        Récupère les résultats d'une requête SELECT.
        :param query: La requête SQL SELECT à exécuter.
        :param params: Les paramètres pour la requête SQL (facultatif).
        :return: Les résultats sous forme de liste de tuples.
        """
        if not self.connection or not self.connection.is_connected():
            print("La connexion n'est pas active.")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erreur lors de la récupération des résultats : {e}")
            return []
        finally:
            cursor.close()
