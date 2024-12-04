from typing import Any

class DBManager:

    def __init__(self, database:str, host:str = None, user:str = None, password:str = None, bdd_method:str = ""):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.bdd_method = bdd_method
        self.connection = None

    def connect(self):
        """
        Ouvre la connexion à la base de données.
        """
        pass

    def disconnect(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.connection or (self.bdd_method.lower() == 'mysql' and self.connection.is_connected()):
            self.connection.close()

    def test_connection(self) -> bool:
        if self.connection:
            if self.bdd_method.lower() == 'mysql' and not self.connection.is_connected():
                return False
            return True
        return False

    def execute_query(self, query, params=None, close_cursor=True) -> Any | bool:
        """
        Exécute une requête SQL.
        :param close_cursor:
        :param query: La requête SQL à exécuter.
        :param params: Les paramètres de la requête SQL (facultatif).
        :return: Le curseur de la requête.
        """
        if not self.test_connection():
            print("La connexion n'est pas active.")
            return
        try:
            print(query)
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            if close_cursor:
                cursor.close()
                return True
            return cursor
        except Exception as e:
            print(f'Erreur execute query : {e}')
            cursor.close()
            return False

    def insert_many(self, table:str, attributs:list[str], params:list[tuple]) -> bool:
        try:
            cursor = self.connection.cursor()
            str_attributs = ','.join(attributs)
            str_attributs_values = ','.join(['?' for i in range(len(attributs))])
            query = f"INSERT INTO {table} ({str_attributs}) VALUES ({str_attributs_values})"
            cursor.executemany(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            print(f'Erreur insert many : {e}')
            cursor.close()
            return False

    def insert_one(self, table:str, attributs:list[str], params:tuple) -> bool:
        try:
            str_attributs = ','.join(attributs)
            str_attributs_values = ','.join(['?' for i in range(len(attributs))])
            query = f"INSERT INTO {table} ({str_attributs}) VALUES ({str_attributs_values})"
            self.execute_query(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            print(f'Erreur insert one : {e}')
            return False

    def delete(self, table, attributs:list[str] = [], params:tuple = None) -> bool:
        """Supprime des données dans la base de données"""
        try:
            query, params = _format_condition(f"DELETE FROM {table}", attributs, params)
            cursor = self.execute_query(query, params, close_cursor=False)
            if cursor:
                return cursor.rowcount > 0
            return cursor
        except Exception as e:
            print(f'Erreur delete : {e}')
            return False

    def fetch_one(self, table, attributs:list[str] = [], params:tuple = None) -> tuple | None:
        """
        Récupère un seul résultat dans la base de données.
        """
        query, params = _format_condition(f"SELECT * FROM {table}", attributs, params)
        cursor = self.execute_query(query, params, False)
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        return None

    def fetch_all(self, table:str, attributs:list[str] = [], params:tuple = None) -> list[tuple]:
        """
        Récupère tous les résultats dans une base de données.
        """
        query, params = _format_condition(f"SELECT * FROM {table}", attributs, params)
        cursor = self.execute_query(query, params, False)
        if cursor:
            results = cursor.fetchall()
            cursor.close()
            return results
        return []

def _format_condition(query:str, attributs:list[str], params:tuple) -> (str, tuple | None):
    if len(attributs) == 0:
        query += ";"
        params = None
    else:
        condition = ""
        for i in range(len(attributs)):
            attribut = attributs[i]
            if i == len(attributs) - 1:
                condition += f"{attribut} = ?;"
            else:
                condition += f"{attribut} = ? AND "
        query += f" WHERE {condition}"
    return query, params