import datetime
from dotenv import load_dotenv
import os
from models import MySQLManager, SQLiteManager, DBManager
load_dotenv()
import subprocess




def setup_project(bdd:DBManager.DBManager):
    bdd.connect()
    debut = datetime.datetime.now()
    subprocess.run(["alembic", "upgrade", "head"])

    fin = datetime.datetime.now()

    print(f"Temps execution du setup : {(fin-debut).seconds} secondes")
    bdd.disconnect()


if os.getenv("DB_METHOD") == "sqlite":
    setup_project(SQLiteManager.SQLiteManager())
elif os.getenv("DB_METHOD") == "mysql":
    setup_project(MySQLManager.MySQLManager())
else:
    print("Méthode de base de données non supporté")

