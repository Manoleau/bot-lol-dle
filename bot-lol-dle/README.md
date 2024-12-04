# bot-lol-dle

# Installation
### Prérequis
- Python
- Git
### Clonage
```
git clone https://github.com/Manoleau/bot-lol-dle.git
```
### Env
- Créez un fichier .env à la racine du projet
- Ajoutez les lignes suivantes dans le fichier
- Changez le token par votre token de bot
```
TOKEN_DISCORD_BOT=ChangerToken
DB_METHOD=mysql
DATABASE=leaguedle

MYSQL_ROOT_PASSWORD=root
MYSQL_HOST=localhost
MYSQL_USER=db
MYSQL_PASSWORD=db
```
### Base de données
Veillez à bien executer le `docker-compose up` pour initialiser mysql et phpmyadmin.
<br>Pour accéder à PhpMyAdmin : [http://localhost:8080](http://localhost:8080)

### Lancer
```
pip install -r requirements.txt
python main.py
```