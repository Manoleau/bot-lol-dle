from bot import Bot
from dotenv import load_dotenv
import os
from models import MySQLManager, SQLiteManager
load_dotenv()

if os.getenv("DB_METHOD") == "sqlite":
    bdd = SQLiteManager.SQLiteManager()
    bdd.connect()
elif os.getenv("DB_METHOD") == "mysql":
    bdd = MySQLManager.MySQLManager()
    bdd.connect()
else:
    bdd = None
    print("Méthode de base de données non supporté")
if bdd and bdd.test_connection():
    print("Connexion à la base de données réussi.")
    bdd.disconnect()
    bot = Bot()
    bot.run(os.getenv("TOKEN_DISCORD_BOT"))
else:
    print("Aucune connexion à la base de données.")