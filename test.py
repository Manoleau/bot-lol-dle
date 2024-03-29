import sqlite3
import requests
import random
from data_base import DB
conn = sqlite3.connect('DB/LeagueDle.db')
cursor = conn.cursor()
import time

# cursor.execute("""
# SELECT Skin.*
# FROM JoueurSkins
# JOIN Skin ON JoueurSkins.id_thing = Skin.id
# WHERE JoueurSkins.type = 'skin'  -- Supposons que 'type' doit être égal à 'Skin'
#     AND Skin.rarity = 'Utlime'
#     AND JoueurSkins.joueurId = 334695006663344151;  -- Remplacez par l'ID du joueur souhaité
# """)
# print(cursor.fetchall())
t = DB("qsdqs", None)
print(t.get_all_skins_of(334695006663344151, 'Ultime'))


# cursor.execute("""SELECT s.name, s.rarity
# FROM Skin s
# LEFT JOIN JoueurSkins js ON s.id = js.id_thing AND js.joueurId = 422208112225812511
# WHERE js.id_thing IS NULL;""")

# for f in cursor.fetchall():
#     print(f"{f[0]} : {f[1]}")



# cursor.execute("""
# CREATE TABLE "CompteLol" (
# 	"id"	VARCHAR(255) NOT NULL,
# 	"accountId"	VARCHAR(255) NOT NULL,
# 	"puuid"	VARCHAR(255) NOT NULL,
# 	"name"	VARCHAR(255) NOT NULL,
#     "profileIconUrl"	VARCHAR(255) NOT NULL,
# 	"profileIconId"	INTEGER NOT NULL,
# 	"summonerLevel"	INTEGER NOT NULL,
# 	PRIMARY KEY("id")
# )""")
# conn.commit()


# cursor.execute("""
# CREATE TABLE LeagueLol (
#     leagueId VARCHAR(36) PRIMARY KEY,
#     queueType VARCHAR(20),
#     tier VARCHAR(32),
#     rank VARCHAR(5),
#     summonerId VARCHAR(64),
#     summonerName VARCHAR(255),
#     leaguePoints INT,
#     wins INT,
#     losses INT
# );
# """)
# conn.commit()

# cursor.execute("SELECT DISTINCT Skin.name FROM Skin, JoueurSkins WHERE Skin.id NOT IN JoueurSkins.id_thing AND JoueurSkins.joueurId = 383497419460968448")

# t = DB("adsqdq")

# for i in range(5265):
#     tirage = t.tirage_skin(334695006663344151)
#     if tirage == None:
#         print("FINI")
#     else:
#         if tirage[0] == 1:
#             cursor.execute("INSERT INTO JoueurSkins VALUES(334695006663344151, ?, ?, 1)", (tirage[2]["id"], tirage[1]))
#         else:
#             cursor.execute("UPDATE JoueurSkins SET quantite = ? WHERE joueurId = 334695006663344151 AND id_thing = ?;",(tirage[0], tirage[2]["id"]))
#         conn.commit()
#     print(i)


# cursor.execute("DELETE FROM JoueurSkins WHERE joueurId = 334695006663344151")
# conn.commit()

# Normal = 0
# Epique = 0
# Hextech = 0
# Legendaire = 0
# Ultime = 0
# cursor.execute("SELECT COUNT(*) FROM Skin WHERE rarity = 'Ultime'")
# Ultime += cursor.fetchone()[0]
# cursor.execute("SELECT id, hasChroma FROM Skin WHERE rarity = 'Légendaire'")
# for skin in cursor.fetchall():
#     Legendaire += 1

# cursor.execute("SELECT id, hasChroma FROM Skin WHERE rarity = 'Hextech'")
# for skin in cursor.fetchall():
#     Hextech += 1

# cursor.execute("SELECT id, hasChroma FROM Skin WHERE rarity = 'Epique'")
# for skin in cursor.fetchall():
#     Epique += 1
        
# cursor.execute("SELECT id, hasChroma FROM Skin WHERE rarity = 'Normal'")
# for skin in cursor.fetchall():
#     Normal += 1

# totaux = Normal+Epique+Hextech+Legendaire+Ultime

# tmp = round(Ultime/totaux, 4)
# cursor.execute("UPDATE RaritySkinsChromas SET probabilite = ? WHERE name = 'Ultime'",(tmp,))
# tmp += round(Legendaire/totaux, 4)
# cursor.execute("UPDATE RaritySkinsChromas SET probabilite = ? WHERE name = 'Légendaire'",(tmp,))
# tmp += round(Hextech/totaux, 4)
# cursor.execute("UPDATE RaritySkinsChromas SET probabilite = ? WHERE name = 'Hextech'",(tmp,))
# tmp += round(Epique/totaux, 4)
# cursor.execute("UPDATE RaritySkinsChromas SET probabilite = ? WHERE name = 'Epique'", (tmp,))
# tmp += round(Normal/totaux, 4)
# cursor.execute("UPDATE RaritySkinsChromas SET probabilite = ? WHERE name = 'Normal'", (tmp,))
# conn.commit()




# cursor.execute("DELETE FROM JoueurSkins")
# conn.commit()


# print(cursor.fetchone())
# cursor.execute("UPDATE Skin SET rarity = 'Normal' WHERE rarity = 'NoRarity';")
# cursor.execute("UPDATE Skin SET rarity = 'Normal' WHERE rarity = 'Default';")
# cursor.execute("UPDATE Skin SET rarity = 'Normal' WHERE rarity = 'Rare';")
# cursor.execute("UPDATE Skin SET rarity = 'Epique' WHERE rarity = 'Epic';")
# cursor.execute("UPDATE Skin SET rarity = 'Hextech' WHERE rarity = 'Mythic';")
# cursor.execute("UPDATE Skin SET rarity = 'Légendaire' WHERE rarity = 'Legendary';")


# image = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/ LE RESTE"

# cursor.execute("SELECT id, name FROM Champions ORDER BY name ASC;")
# idchamp = cursor.fetchall()
# longueur = len(idchamp)
# for id in idchamp:
#     print(f"il reste {str(longueur)} champions")
#     champ = requests.get(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/fr_fr/v1/champions/{id[0]}.json").json()
#     championId = champ["id"]
#     for skin in champ["skins"]:
#         id = skin["id"]
        
#         name = skin["name"]
#         isBase = skin["isBase"]
#         if isBase:
#             rarity = "Default"
#         else:
#             rarityliste = skin["rarity"].split("k")
#             rarity = ""
#             for i in range(1, len(rarityliste)):
#                 rarity += f"{rarityliste[i]}"


#         splashPath = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/{skin['splashPath'].replace('/lol-game-data/assets/', '')}"
#         tilePath = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/{skin['tilePath'].replace('/lol-game-data/assets/', '')}"
#         loadScreenPath = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/{skin['loadScreenPath'].replace('/lol-game-data/assets/', '')}"
        
#         if "chromas" in skin:
#             hasChroma = True
#             # cursor.execute("INSERT INTO Skin VALUES(?,?,?,?,?,?,?,?,?)", (id, championId, name, isBase, rarity, splashPath, tilePath, loadScreenPath, hasChroma))
#             # conn.commit()
#             for chroma in skin["chromas"]:
#                 idChroma = chroma["id"]
#                 name = chroma["name"]
                
#                 chromaPath = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/{chroma['chromaPath'].replace('/lol-game-data/assets/', '')}"
#                 if len(chroma["colors"]) > 0:
#                     color = chroma["colors"][0]
#                 else:
#                     color = None
#                 cursor.execute("INSERT INTO Chroma VALUES(?,?,?,?,?)", (idChroma, name, chromaPath, color, id))
#                 conn.commit()
#         else:
#             hasChroma = False
#             # cursor.execute("INSERT INTO Skin VALUES(?,?,?,?,?,?,?,?,?)", (id, championId, name, isBase, rarity, splashPath, tilePath, loadScreenPath, hasChroma))
#             # conn.commit()
#     longueur -= 1


# cursor.execute("SELECT * FROM Regions;")
# res = cursor.fetchall()
# print(res) 
# cursor.execute("""
# CREATE TABLE Regions (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name VARCHAR(255),
#     logo VARCHAR(255),
#     splash VARCHAR(255),
#     description TEXT
# );
# """)



# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Aatrox")))


# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Aatrox"), ))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ahri")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Akali")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Akshan")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Alistar")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Amumu")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Anivia")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Annie")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Aphelios")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ashe")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Aurelion Sol")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Azir")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Bard")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Bel'Veth")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Blitzcrank")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Brand")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Braum")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Briar")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Caitlyn")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Camille")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Cassiopeia")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Cho'Gath")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Corki")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Darius")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Diana")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Dr. Mundo")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Draven")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ekko")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Elise")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Evelynn")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ezreal")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Fiddlesticks")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Fiora")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Fizz")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Galio")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Gangplank")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Garen")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Gnar")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Gragas")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Graves")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Gwen")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Hecarim")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Heimerdinger")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Illaoi")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Irelia")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ivern")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Janna")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Jarvan IV")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Jax")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Jayce")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Jhin")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Jinx")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("K'Santé")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kai'Sa")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kalista")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Karma")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Karthus")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kassadin")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Katarina")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kayle")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kayn")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kennen")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kha'Zix")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kindred")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kled")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Kog'Maw")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("LeBlanc")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Lee Sin")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Leona")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Lillia")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Lissandra")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Lucian")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Lulu")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Lux")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Malphite")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Malzahar")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Maokai")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Maître Yi")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Milio")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Miss Fortune")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Mordekaiser")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Morgana")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Naafiri")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Nami")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Nasus")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Nautilus")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Neeko")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Nidalee")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Nilah")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Nocturne")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Nunu et Willump")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Olaf")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Orianna")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ornn")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Pantheon")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Poppy")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Pyke")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Qiyana")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("uinn")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Rakan")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Rammus")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Rek'Sai")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Rell")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Renata Glasc")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Renekton")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Rengar")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Riven")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Rumble")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ryze")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Samira")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Sejuani")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Senna")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Sett")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Shaco")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Shen")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Shyvana")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Singed")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Sion")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("ivir")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Skarner")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Sona")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Soraka")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Swain")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Sylas")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Syndra")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Séraphine")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Tahm Kench")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Taliyah")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Talon")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Taric")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Teemo")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Thresh")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Tristana")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Trundle")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Tryndamere")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Twisted Fate")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Twitch")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Udyr")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Urgot")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Varus")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Vayne")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Veigar")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Vel'Koz")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Vex")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Vi")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Viego")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Viktor")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Vladimir")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Volibear")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Warwick")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Wukong")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Xayah")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Xerath")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Xin Zhao")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Yasuo")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Yone")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Yorick")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Yuumi")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Zac")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Zed")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Zeri")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Ziggs")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Zilean")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Zoé")))
# cursor.execute("INSERT INTO ChampionRegion (champion_id, region_id) VALUES(?, ?)", (D.get_champion_id_by_name("Zyra")))

# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Ionia', 'https://universe.leagueoflegends.com/images/iona_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/bltcea170f820e544c5/60ee0e19a471a34acb2c1f66/ionia-01.jpg', ?);", ("Entourée de mers capricieuses, Ionia est composée de plusieurs provinces alliées réparties à travers un gigantesque archipel appelé les Terres premières. La culture ionienne s'est développée dans le but de maintenir l'équilibre universel, et par conséquent, la frontière entre le monde matériel et le monde spirituel y est plus perméable, particulièrement dans les montagnes et les forêts sauvages.\nBien que la magie de ces terres soit imprévisible et que les créatures y soient dangereuses et féeriques, la plupart des Ioniens ont vécu dans la paix et la prospérité pendant des siècles. Les moines guerriers, les milices provinciales et Ionia elle-même ont suffi à les protéger.\nMais tout a basculé il y a douze ans, lorsque Noxus a attaqué les Terres premières. Les assauts incessants des forces impériales ravagèrent Ionia pendant de nombreuses années avant d'être vaincues, et le prix de la victoire fut terrible.\nDésormais, une paix fragile règne à Ionia. La guerre a provoqué différentes réactions et a divisé la région. Certains groupes, comme les moines de Shojin ou le Kinkou, souhaitent renouer avec leurs valeurs traditionnelles : l'isolement et le pacifisme. D'autres factions, comme la Fraternité Navori ou l'Ordre de l'ombre, sont plus radicales et demandent la militarisation de la magie de leurs terres afin de créer une nation puissante, unie et capable de se venger de Noxus.\nLe destin d'Ionia ne tient qu'à un fil que peu de gens sont prêts à trancher, mais que tous voient s'effilocher dangereusement sous leurs yeux.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Bandle', 'https://universe.leagueoflegends.com/images/bandle_city_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt57ea8bb74f8733f3/60ee0b95bc44fe5b48ba2a02/bandle-city_splash.jpg', ?);", ("Les opinions divergent quant à la localisation exacte du foyer d'origine des yordles, bien que quelques mortels prétendent avoir emprunté des chemins invisibles vers une terre d'enchantements étranges au-delà du monde matériel. Ils parlent d'un lieu fécond en magie, où l'imprudent peut se laisser distraire par des myriades de merveilles et se perdre dans un rêve.\nÀ Bandle, chaque sensation est décuplée pour les êtres qui ne sont pas des yordles. Les couleurs sont incroyablement vives, la nourriture et les boissons enivrent les sens pendant des années et, quand on y a goûté une fois, on n'en oublie plus jamais la saveur. La lumière du soleil est incroyablement dorée, l'eau y est claire comme du cristal et chaque récolte est abondante. Peut-être certaines de ces affirmations sont-elles vraies, peut-être aucune : aucun conteur ne semble d'accord avec les autres sur ce qu'il a vu.\nLa seule chose que l'on sache de façon certaine, c'est que Bandle et ses habitants vivent hors du temps. Cela explique peut-être pourquoi les mortels qui parviennent à revenir semblent avoir terriblement vieilli... et pourquoi la plupart ne reviennent jamais.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Bilgewater', 'https://universe.leagueoflegends.com/images/bilgewater_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt8efd86a20a7fc6ca/60ee0bd126ed9249f5484b8c/bilgewater_splash.jpg', ?);", ("Nichée dans l'archipel des Îles de la Flamme bleue, Bilgewater est une ville portuaire semblable à nulle autre : elle abrite les pêcheurs de serpents de mer, les gangs des docks et tous les contrebandiers du monde. Ici, les fortunes se font et les ambitions meurent en une fraction de seconde. Pour ceux qui fuient la justice, l'endettement ou la persécution, Bilgewater peut être le lieu d'un nouveau départ, car nul ici ne vous questionne sur votre passé. Pourtant, chaque matin, on retrouve dans les eaux du port des cadavres de voyageurs, la bourse vide et la gorge tranchée…\nBien que Bilgewater soit une cité dangereuse, elle regorge d'opportunités pour les aventuriers sans scrupule que limitent d'ordinaire les lois et les régulations commerciales. Si vous avez de l'argent, vous pouvez acheter n'importe quoi ici, des technologies Hextech illégales aux faveurs des seigneurs du crime organisé.\nLe dernier roi des pillards de Bilgewater ayant été récemment renversé, la cité est entrée dans une période de transition, alors que les capitaines les plus éminents tentent de se mettre d'accord sur son avenir. Néanmoins, tant qu'il y aura des navires en état de naviguer et des équipages pour les manœuvrer, Bilgewater demeurera certainement l'un des endroits de Runeterra les plus animés et les mieux connectés au reste du monde.",))

# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Demacia', 'https://universe.leagueoflegends.com/images/demacia_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/bltd170f10ccce6ba7e/614cc12077d06a0c9835f862/demacia_splash.jpeg', ?);", ("emacia est un royaume fort, fondé sur des lois strictes et riche d'un passé militaire prestigieux. Ses habitants ont toujours attaché une grande importance aux idéaux de justice, d'honneur et de devoir, et ils sont très fiers de leur héritage culturel. Mais malgré ses valeurs très nobles, cette nation parfaitement autosuffisante est devenue de plus en plus insulaire et isolationniste au cours de ces derniers siècles.\nAujourd'hui, le royaume de Demacia traverse une période trouble.\nLa capitale, la Grande cité de Demacia, a été fondée pour servir de refuge contre la sorcellerie après le cauchemar des Guerres runiques et a été bâtie sur le mystère de la pétricite, une étrange pierre blanche pouvant saper l'énergie magique. C'est de là que la famille royale a toujours veillé à la défense des villes et villages alentours, ainsi que des terres agricoles, des forêts et des montagnes riches en ressources minérales qui constituent le royaume.\nCependant, après le décès soudain du roi Jarvan III, les autres familles nobles n'ont toujours pas approuvé la succession au trône de son unique héritier, le jeune prince Jarvan.\nTous ceux qui vivent au-delà des frontières bien gardées du royaume sont perçus avec une suspicion grandissante, et en ces temps de doute, beaucoup d'anciens alliés se tournent vers de nouvelles sources de protection. Certains osent murmurer que l'âge d'or de Demacia est révolu et que si son peuple ne parvient pas à s'adapter à un monde en constante évolution, ce dont beaucoup le jugent incapable, le déclin du royaume est inévitable.\nEt toute la pétricite du monde ne pourra protéger Demacia de lui-même.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Freljord', 'https://universe.leagueoflegends.com/images/freljord_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/bltc15ba510f02e7e45/60ee0d9185b042284396138b/freljord_splash.jpg', ?);", ("reljord est une terre inhospitalière et hostile dont les habitants sont des guerriers-nés, contraints de persévérer envers et contre tout.\nAussi fières qu'elles sont outrageusement indépendantes, les tribus de Freljord sont souvent considérées comme barbares et sauvages par leurs voisins de Valoran, lesquels ignorent les traditions ancestrales qui les ont façonnées. Il y a plusieurs milliers d'années, l'alliance entre les sœurs Avarosa, Serylda et Lissandra fut brisée lorsqu'une guerre menaça de ravager tout Runeterra à son insu, ce qui plongea les territoires du nord dans le chaos d'un hiver quasi permanent. De nos jours, seuls les mortels exceptionnels qui semblent immunisés contre les ravages du feu ou de la glace sont destinés, ou tout du moins capables de gouverner.\nMalgré les efforts des Gardiens du givre, nombre de mythes et légendes relatent encore les récits des dieux anciens, yétis étranges et autres Gardiens des esprits. Les maraudeurs de la Griffe hivernale s'aventurent chaque année un peu plus loin, tourmentant Demacia au sud et Noxus à l'est. Finalement, en quête d'une destinée meilleure, les tribus indépendantes et irascibles ont commencé l'une après l'autre à accorder leur allégeance à Ashe, la jeune reine des Avarosans.\nL'avenir, pourtant, n'en reste pas moins maussade. Tôt ou tard, la guerre reviendra à Freljord, et nul ne peut espérer y échapper.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Ixtal', 'https://universe.leagueoflegends.com/images/ixtal_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt9a01601bbdff5c4a/60ee0e385fbfcb5e848229a5/ixtal_splash.jpg', ?);", ("Célèbre pour sa maîtrise de la magie élémentaire, Ixtal fut l'une des premières nations indépendantes à se joindre à l'empire de Shurima. En vérité, la culture d'Ixtal est bien plus ancienne que ça. Elle appartient à la grande diaspora de l'ouest qui a donné naissance à de nombreuses civilisations, parmi lesquelles Buhru, la magnifique Helia et Targon l'ascétique. Elle a probablement joué un rôle significatif dans la création des premiers Transfigurés.\nMais les mages d'Ixtal survécurent au Néant, et plus tard aux Darkin, en prenant leurs distances avec leurs voisins. Ils se retranchèrent dans la nature sauvage comme derrière une forteresse. Dans le chaos, ils avaient beaucoup perdu, mais ils avaient la ferme intention de préserver ce qui restait…\nAujourd'hui, la cité arcologique d'Ixaocan, perdue dans la jungle depuis des millénaires, perdure sans influence extérieure. Ayant assisté de loin à la ruine des Îles bénies et aux Guerres runiques, les Ixtali voient toutes les autres factions de Runeterra comme des parvenus et ils utilisent leur puissante magie pour éloigner les intrus.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Néant', 'https://universe.leagueoflegends.com/images/void_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt4754fc6a91233824/60ee139d5397524ead38918f/void-an-unknowable-power.jpg', ?);", ("pparu dans un cri assourdissant à la naissance de l'univers, le Néant est une manifestation de la non-existence qui s'étend « au-delà ». Cette force animée d'une faim insatiable attend depuis une éternité que ses maîtres, les mystérieux Veilleurs, sonnent l'heure de la fin des temps.\nLorsque le Néant touche un mortel, celui-ci reçoit un douloureux aperçu de l'irréalité éternelle, une vision capable de briser l'esprit le plus solide. Les habitants du royaume du Néant sont des créatures disparates à l'intelligence souvent limitée, mais tous partagent le même objectif : détruire Runeterra.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Noxus', 'https://universe.leagueoflegends.com/images/noxus_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt9d0c487b98ba6b42/60ee0ffb975ffd4ff25ec2f5/noxus_splash.jpg', ?);", ("Noxus est un puissant empire à la réputation terrifiante. Pour les étrangers qui vivent hors de ses frontières, il s'agit d'un pays brutal, expansionniste et agressif, mais ceux qui observent au-delà de cette façade belliqueuse découvrent une société ouverte, où la force et les talents du peuple sont valorisés et cultivés.\nLes Noxiis formaient autrefois un groupe de redoutables tribus barbares, jusqu'à ce qu'ils prennent d'assaut et s'installent dans l'ancienne cité qui constitue aujourd'hui le cœur de leur empire. Menacés de toutes parts, ils sont allés au-devant de leurs ennemis pour combattre, repoussant leurs frontières plus loin chaque année. Cette lutte pour la survie a fait des Noxiens modernes un peuple fier pour qui la force prime sur tout le reste, bien que cette force puisse s'exprimer de différentes façons.\nN'importe quelle personne peut s'élever à une position de pouvoir et de respect à Noxus, indépendamment de son statut social, de ses antécédents, de son lieu d'origine ou de sa richesse, du moment qu'elle fait montre des aptitudes nécessaires. Ceux qui sont capables de manipuler la magie sont tenus en haute estime et activement recherchés, dans l'espoir que leurs talents uniques puissent être affinés et mis au service de l'empire.\nPourtant, malgré cet idéal méritocratique, les vieilles maisons nobles conservent un pouvoir considérable... et certains craignent que la plus grande menace qui pèse sur Noxus ne vienne pas de ses ennemis, mais bien de l'intérieur.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Piltover', 'https://universe.leagueoflegends.com/images/piltover_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt5c307209ccbe2470/60ee10d06610ed4d42bc222e/piltover_splash.jpg', ?);", ("Piltover est une cité florissante animée par le progrès, dont la puissance et l'influence ne cessent de croître. C'est le centre culturel de Valoran, où l'art, l'artisanat, le commerce et l'innovation avancent main dans la main. Sa puissance ne repose pas sur sa force militaire, mais sur les rouages bien huilés du libre-échange et de la pensée progressiste. Située sur les falaises qui surplombent le district de Zaun et l'océan, cette ville est le point de convergence de flottes entières de vaisseaux, qui traversent ses titanesques portails marins pour y acheminer des marchandises venues de toutes parts. L'opulence dont profite la cité a conduit à un développement urbain spectaculaire et sans précédent. Piltover est parvenue - et parvient toujours ! - à se réinventer constamment, pour devenir une ville où quiconque peut faire fortune et vivre pleinement ses rêves. De jeunes guildes de marchands y financent les entreprises les plus folles : des projets artistiques extravagants et grandioses, des recherches ésotériques sur la technologie Hextech, ou encore des monuments architecturaux qui rendent hommage à leur puissance. Grâce à l'afflux toujours grandissant d'inventeurs venus explorer les possibilités du domaine Hextech, Piltover est aujourd'hui un centre névralgique qui attire les meilleurs artisans du monde entier.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Shurima', 'https://universe.leagueoflegends.com/images/shurima_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt5924e500520eabd9/60ee11fb94d70a1ef3123825/shurima_splash.jpg', ?);", ("L'empire de Shurima était autrefois une civilisation florissante qui s'étendait sur un continent tout entier. Forgé en un temps révolu par les puissants dieux-guerriers de l'Ost des Transfigurés, il scella l'union de tous les peuples disparates du sud et imposa entre eux une paix durable.\nRares étaient ceux qui osaient se rebeller. Ceux qui le faisaient, parmi lesquels la nation maudite d'Icathia, étaient broyés sans aucune pitié.\nPourtant, après plusieurs millénaires de croissance et de prospérité, la capitale fut transformée en un champ de ruines par l'échec de l'Ascension du dernier empereur de Shurima. Avec le temps, le récit de cette gloire passée devint un simple mythe. De nos jours, la plupart des habitants nomades du désert de Shurima luttent pour leur survie dans un territoire inhospitalier. Certains défendent de petits postes avancés construits autour de quelques oasis, tandis que d'autres s'enfoncent dans ces catacombes oubliées à la recherche des richesses qui y sont sûrement enterrées. D'autres encore acceptent du travail de mercenaire, empochant leur récompense avant de disparaître à nouveau dans les sables sans foi ni loi.\nQuelques-uns, pourtant, osent encore rêver d'une réémergence du passé. De fait, les tribus sont depuis peu agitées par un murmure qui provient du cœur du désert : leur empereur Azir serait de retour pour les mener vers un nouvel âge d'or.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Targon', 'https://universe.leagueoflegends.com/images/mt_targon_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt1ab39bfee4a3057d/60ee0f894fba2021cde587f6/mount-targon_splash.jpg', ?);", ("Du haut de son imposante aiguille de pierres stériles, le Mont Targon est le point culminant de la plus haute chaîne de montagnes de Runeterra. S'élevant aux confins de toute civilisation, il n'est accessible qu'aux explorateurs les plus déterminés. De nombreuses légendes entourent le Mont Targon, et comme tous les lieux mythologiques, il enflamme l'imagination des rêveurs, des fous, de tous ceux qui sont assoiffés d'aventure. Certaines de ces âmes courageuses tentent même de gravir l'insurmontable montagne, à la recherche peut-être de l'illumination ou de la gloire, ou répondant simplement au désir ardent d'en contempler le sommet. L'ascension vers le sommet est pratiquement impossible, et les rares élus qui parviennent à l'atteindre en vie ne parlent presque jamais de ce qu'ils y ont vu. Certains en reviennent avec une expression hantée et vide dans le regard ; d'autres deviennent totalement méconnaissables, imprégnés de la Manifestation d'un pouvoir surhumain venu d'un autre monde, chargés d'un destin que peu de mortels pourraient comprendre.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Zaun', 'https://universe.leagueoflegends.com/images/zaun_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/blt3d038a51072c6d5a/614cc18164c8007a9bdec0e2/zaun_splash.jpeg', ?);", ("Zaun est un vaste district relié à Piltover, qui s'étend dans les vallées et les profonds canyons situés en contrebas. Le peu de lumière qui atteint cette « basse-ville », filtré par les épaisses fumées émanant de l'entrelacs de tuyaux rouillés dont elle est parsemée, se reflète sur les vitres crasseuses de ses bâtiments à l'architecture industrielle. Zaun et Piltover constituaient autrefois une seule et même cité ; aujourd'hui, ces deux sociétés sont séparées mais vivent en symbiose. Bien qu'elle soit perpétuellement plongée dans un brouillard néfaste, Zaun est une ville florissante, dont les habitants sont dynamiques et la culture très riche. L'opulence de Piltover a permis à Zaun de se développer avec elle en tandem, comme un reflet sombre de la ville des hauteurs. La plupart des marchandises qui affluent vers la riche cité finissent par se retrouver sur les marchés noirs de sa sœur en contrebas, et les inventeurs Hextech qui jugent les réglementations de Piltover trop restrictives peuvent souvent mener librement leurs expériences, si dangereuses soient-elles, dans les tréfonds de Zaun. Le développement incontrôlé de diverses technologies à risque et l'industrialisation débridée ont transformé d'immenses portions de Zaun en quartiers pollués et mal famés. Des flots de résidus toxiques stagnent dans les bas-fonds de la ville, mais même dans ces secteurs, les habitants parviennent à mener leur vie et à prospérer.",))
# cursor.execute("INSERT INTO Regions (name, logo, splash, description) VALUES('Iles Obscures', 'https://universe.leagueoflegends.com/images/shadow_isles_crest_icon.png', 'https://images.contentstack.io/v3/assets/blt187521ff0727be24/bltd9cec6dc7ca0fc48/60ee11d22f7fa122fd574a11/shadow-isles_splash.jpg', ?);", ("ette terre maudite était autrefois une civilisation noble et éclairée, connue auprès de ses alliés et de ses émissaires sous le nom d'Îles bénies. Cependant, il y a plus d'un millier d'années, un cataclysme magique sans précédent réduisit en lambeaux la frontière entre le monde physique et le royaume spirituel, entraînant leur fusion... et condamnant instantanément tous les êtres vivants.\nAujourd'hui, la Brume noire recouvre en permanence les îles, et la terre elle-même est souillée par la magie noire. Les mortels qui osent s'aventurer sur ces côtes sinistres voient leur énergie vitale peu à peu drainée de leur corps, ce qui attire progressivement les esprits des morts, voraces et insatiables.\nCeux qui périssent au cœur de la Brume noire sont condamnés à hanter ces îles tourmentées pour toute l'éternité. Pire encore, le pouvoir des Îles obscures devient de plus en plus puissant chaque année, ce qui permet aux spectres d'étendre leur influence toujours plus loin dans tout Runeterra.",))

# cursor.execute("UPDATE Champions SET annee_sortie = 2023, porte = 'Mêlée', genre = 'Féminin', ressource = 'Fureur' WHERE  name = 'Briar';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2023, porte = 'Mêlée', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Naafiri';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2023, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Milio';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Mêlée', genre = 'Masculin', ressource = 'Puits de sang' WHERE  name = 'Aatrox';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Ahri';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Féminin', ressource = 'Energie' WHERE  name = 'Akali';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2021, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Akshan';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Alistar';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Amumu';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Anivia';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Annie';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2019, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Aphelios';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Ashe';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2016, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Aurelion Sol';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2014, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Azir';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2015, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Bard';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2022, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = ?;", ("Bel'Veth",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Blitzcrank';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Brand';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2014, porte = 'Mêlée', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Braum';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Caitlyn';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2016, porte = 'Mêlée', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Camille';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Cassiopeia';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = 'Mana' WHERE  name = ?;", ("Cho'Gath",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Corki';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Darius';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Féminin', ressource = 'Mana' WHERE  name = 'Diana';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = 'Aucune' WHERE  name = 'Dr. Mundo';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Distance', genre = 'Masculin', ressource = 'Mana' WHERE  name = 'Draven';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2015, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Ekko';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée et Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Elise';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Evelynn';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Ezreal';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Fiddlesticks';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Fiora';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Fizz';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Galio';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Gangplank';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Garen';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2014, porte = 'Mêlée et Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Gnar';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Gragas';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Graves';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2021, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Gwen';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Hecarim';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Heimerdinger';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2015, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Illaoi';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Irelia';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2016, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Ivern';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Janna';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Jarvan IV';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Jax';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée et Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Jayce';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2016, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Jhin';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Jinx';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2022, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = ?;", ("K'Santé",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2018, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = ?;", ("Kai'Sa",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2014, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Kalista';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Karma';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Karthus';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Kassadin';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Katarina';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Kayle';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2017, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Kayn';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Kennen';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = ?;", ("Kha'Zix",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2015, porte = 'Distance', genre = 'Autre', ressource = '' WHERE  name = 'Kindred';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2016, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Kled';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = ?;",("Kog'Maw",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'LeBlanc';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Lee Sin';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Leona';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2020, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Lillia';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Lissandra';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Lucian';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Lulu';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Lux';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Maître Yi';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Malphite';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Malzahar';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Maokai';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Miss Fortune';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Mordekaiser';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Morgana';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Nami';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Nasus';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Nautilus';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2018, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Neeko';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée et Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Nidalee';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2022, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Nilah';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Nocturne';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Nunu et Willump';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Olaf';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Orianna';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2017, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Ornn';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Pantheon';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Poppy';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2018, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Pyke';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2018, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Qiyana';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Quinn';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2017, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Rakan';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Rammus';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2014, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = ?;", ("Rek'Sai",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2020, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Rell';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2022, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Renata Glasc';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Renekton';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Rengar';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Riven';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Rumble';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Ryze';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2021, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Samira';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Sejuani';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2019, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Senna';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2020, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Séraphine';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2020, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Sett';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Shaco';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Shen';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Shyvana';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Singed';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Sion';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Sivir';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Skarner';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Sona';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Soraka';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Swain';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2019, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Sylas';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Syndra';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2015, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Tahm Kench';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2016, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Taliyah';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Talon';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Taric';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Teemo';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Thresh';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Tristana';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Trundle';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Tryndamere';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Twisted Fate';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Twitch';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Udyr';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Urgot';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Varus';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Vayne';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Veigar';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2014, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = ?;",("Vel'Koz",))
# cursor.execute("UPDATE Champions SET annee_sortie = 2021, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Vex';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Féminin', ressource = '' WHERE  name = 'Vi';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2021, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Viego';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Viktor';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Vladimir';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Volibear';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Warwick';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Wukong';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2017, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Xayah';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Xerath';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2010, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Xin Zhao';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Yasuo';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2020, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Yone';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2011, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Yorick';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2019, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Yuumi';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2013, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Zac';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Mêlée', genre = 'Masculin', ressource = '' WHERE  name = 'Zed';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2022, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Zeri';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Ziggs';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2009, porte = 'Distance', genre = 'Masculin', ressource = '' WHERE  name = 'Zilean';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2017, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Zoé';")
# cursor.execute("UPDATE Champions SET annee_sortie = 2012, porte = 'Distance', genre = 'Féminin', ressource = '' WHERE  name = 'Zyra';")

# conn.commit()
# 