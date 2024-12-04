import datetime
from dotenv import load_dotenv
import os
from sqlalchemy.sql.ddl import CreateTable
from models import MySQLManager, SQLiteManager, DBManager
import models.orm as orm
import inspect
load_dotenv()



def setup_project(bdd:DBManager.DBManager):
    bdd.connect()
    debut = datetime.datetime.now()
    entities = inspect.getmembers(orm, inspect.isclass)
    for class_name, class_obj in entities:
        if "Model" in class_obj.__name__:
            bdd.execute_query(str(CreateTable(class_obj.__table__).compile()).replace('TABLE', 'TABLE IF NOT EXISTS'))

    

    fin = datetime.datetime.now()

    print(f"Temps execution du setup : {(fin-debut).microseconds} microseconds")
    bdd.disconnect()


if os.getenv("DB_METHOD") == "sqlite":
    setup_project(SQLiteManager.SQLiteManager())
elif os.getenv("DB_METHOD") == "mysql":
    setup_project(MySQLManager.MySQLManager())
else:
    print("Méthode de base de données non supporté")

