import sqlite3
import asyncio
import aiohttp
import random
import discord
import requests
from discord import Embed
from Bouton.StopGameBoutton import StopGame
from unidecode import unidecode
import time


translate_ranked = {
    "IRON":"Fer",
    "BRONZE":"Bronze",
    "SILVER":"Argent",
    "GOLD":"Or",
    "PLATINUM":"Platine",
    "EMERALD":"Émeraude",
    "DIAMOND":"Diamant",
    "MASTER":"Maître",
    "GRANDMASTER":"Grand Maître",
    "CHALLENGER":"Challenger",
}
class DB:
    def __init__(self, versionLol:str, bot) -> None:
        self.conn = sqlite3.connect('DB/LeagueDle.db')
        self.cursor = self.conn.cursor()
        self.versionLol = versionLol
        self.bot = bot

    def get_champion_annee_by_id(self,idChampion:int) -> int:
        select_query = "SELECT annee_sortie FROM Champions WHERE id = ?;"
        self.cursor.execute(select_query, (idChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_annee_by_name(self,nameChampion:str) -> int:
        select_query = "SELECT annee_sortie FROM Champions WHERE name = ?;"
        self.cursor.execute(select_query, (nameChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_image_by_id(self,idChampion:int) -> str:
        select_query = "SELECT image FROM Champions WHERE id = ?;"
        self.cursor.execute(select_query, (idChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_image_by_name(self,nameChampion:str) -> str:
        select_query = "SELECT image FROM Champions WHERE name = ?;"
        self.cursor.execute(select_query, (nameChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_id_by_name(self,nameChampion:str) -> int:
        select_query = "SELECT id FROM Champions WHERE name = ?;"
        self.cursor.execute(select_query, (nameChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_name_by_id(self,idChampion:int) -> str:
        select_query = "SELECT name FROM Champions WHERE id = ?;"
        self.cursor.execute(select_query, (idChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_splash_by_name(self,nameChampion:str) -> str:
        select_query = "SELECT splash_art FROM Champions WHERE name = ?;"
        self.cursor.execute(select_query, (nameChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_splash_by_id(self,idChampion:int) -> str:
        select_query = "SELECT splash_art FROM Champions WHERE id = ?;"
        self.cursor.execute(select_query, (idChampion,))
        res = self.cursor.fetchone()[0]
        return res
    def get_champion_by_name(self,nameChampion:str) -> dict:
        select_query = "SELECT * FROM Champions WHERE name = ?;"
        self.cursor.execute(select_query, (nameChampion,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "name":res[1],
                "image":res[2],
                "title":res[3],
                "splash_art":res[4],
                "annee_sortie": res[5],
                "porte": res[6],
                "ressource": res[7],
                "genre": res[8],
            }
        return None
    def get_champion_by_id(self,idChampion:int) -> dict:
        select_query = "SELECT * FROM Champions WHERE id = ?;"
        self.cursor.execute(select_query, (idChampion,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "name":res[1],
                "image":res[2],
                "title":res[3],
                "splash_art":res[4],
                "annee_sortie": res[5],
                "porte": res[6],
                "ressource": res[7]
            }
        return None
    def get_random_champion(self) -> dict:
        self.cursor.execute("SELECT * FROM Champions ORDER BY RANDOM() LIMIT 1;")
        res = self.cursor.fetchone()
        return {
            "id":res[0],
            "name":res[1],
            "image":res[2],
            "title":res[3],
            "splash_art":res[4],
            "annee_sortie": res[5],
            "porte": res[6],
            "ressource": res[7]
        }
    def get_all_champions_in_list(self) -> list:
        self.cursor.execute("SELECT * FROM Champions")
        champions = self.cursor.fetchall()
        return [
            {
                "id":champion[0],
                "name":champion[1],
                "image":champion[2],
                "title":champion[3],
                "splash_art":champion[4],
                "annee_sortie": champion[5],
                "porte": champion[6],
                "ressource": champion[7],
                "genre": champion[8],
            }
            for champion in champions
        ]
    def get_all_champions_in_list_start_with(self,lettre:str) -> list:
        if lettre == "E":
            self.cursor.execute("SELECT * FROM Champions WHERE name LIKE 'É%' ORDER BY name ASC;")
            champions = self.cursor.fetchall()
            self.cursor.execute("SELECT * FROM Champions WHERE name LIKE '"+lettre+"%' ORDER BY name ASC;")
            champions += self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT * FROM Champions WHERE name LIKE '"+lettre+"%' ORDER BY name ASC;")
            champions = self.cursor.fetchall()
        if champions:
            return [
                {
                    "id":champion[0],
                    "name":champion[1],
                    "image":champion[2],
                    "title":champion[3],
                    "splash_art":champion[4],
                    "annee_sortie": champion[5],
                    "porte": champion[6],
                    "ressource": champion[7],
                    "genre": champion[8],
                }
                for champion in champions
            ]
        else:
            return None
    def get_roles_champion_by_id(self, idChampion:int) -> list:
        self.cursor.execute("""SELECT Roles.name, Roles.image, Roles.image_location FROM Champions JOIN RoleChampion ON Champions.id = RoleChampion.champion_id JOIN Roles ON RoleChampion.role_id = Roles.id WHERE Champions.id = ?;""", (idChampion,))
        tmp = self.cursor.fetchall()
        if tmp:
            res = []
            for role in tmp:
                res.append({
                    "name":role[0],
                    "image":role[1],
                    "image_location":role[2]
                })
            return res
        return None
    def get_roles_champion_by_name(self, nameChampion:str) -> list:
        self.cursor.execute("""SELECT Roles.name, Roles.image, Roles.image_location FROM Champions JOIN RoleChampion ON Champions.id = RoleChampion.champion_id JOIN Roles ON RoleChampion.role_id = Roles.id WHERE Champions.name = ?;""", (nameChampion,))
        tmp = self.cursor.fetchall()
        if tmp:
            res = []
            for role in tmp:
                res.append({
                    "name":role[0],
                    "image":role[1],
                    "image_location":role[2]
                })
            return res
        return None
    
    async def update_champion_when_lol_update(self, new_info_champ, old_info_champ, guildEmoji:discord.Guild):
        
        if new_info_champ.image != old_info_champ["image"]:
            self.cursor.execute("UPDATE Champions SET image = ? WHERE id = ?", (new_info_champ.image, new_info_champ.id))
            newName = unidecode(new_info_champ.name.replace("'","").replace(" ", "").replace(".","").replace("-","").replace("œ","oe").replace(",",""))
            newEmoji = await self.replace_emoji(guildEmoji, newName, new_info_champ.image, new_info_champ.id)
            self.cursor.execute("UPDATE Emojis SET id = ?, nom_emoji = ? WHERE id_thing = ?;",(newEmoji.id, newEmoji.name, new_info_champ.id))
        if new_info_champ.title != old_info_champ["title"]:
            self.cursor.execute("UPDATE Champions SET title = ? WHERE id = ?", (new_info_champ.title, new_info_champ.id))
        if new_info_champ.splash_art != old_info_champ["splash_art"]:
            self.cursor.execute("UPDATE Champions SET splash_art = ? WHERE id = ?", (new_info_champ.splash_art, new_info_champ.id))
        self.conn.commit()
    async def update_item_when_lol_update(self, new_info_item, old_info_item, guildEmoji:discord.Guild):
        
        if new_info_item.image != old_info_item["image"]:
            self.cursor.execute("UPDATE Items SET image = ? WHERE id = ?", (new_info_item.image, new_info_item.id))
            newName = unidecode(new_info_item.name.replace("'","").replace(" ", "").replace(".","").replace("-","").replace("œ","oe").replace(",",""))
            newEmoji = await self.replace_emoji(guildEmoji, newName, new_info_item.image, new_info_item.id)
            self.cursor.execute("UPDATE Emojis SET id = ?, nom_emoji = ? WHERE id_thing = ?;",(newEmoji.id, newEmoji.name, new_info_item.id))
        if new_info_item.description != old_info_item["description"]:
            self.cursor.execute("UPDATE Items SET description = ? WHERE id = ?", (new_info_item.description, new_info_item.id))
        self.conn.commit()

    def get_role_id(self, nameRole:str) ->int:
        self.cursor.execute("SELECT id FROM Roles WHERE name = ?;",(nameRole,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_role_name(self, idRole:int) ->str:
        self.cursor.execute("SELECT name FROM Roles WHERE id = ?;",(idRole,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None

    def add_roles_to_champion(self, liste_roles:list, idChampion:int):
        for role in liste_roles:
            self.cursor.execute("INSERT INTO RoleChampion (champion_id, role_id) VALUES (?, ?);",(idChampion, self.get_role_id(role)))
        self.conn.commit()

    def get_item_image_by_id(self,idItem:int) -> str:
        select_query = "SELECT image FROM Items WHERE id = ?;"
        self.cursor.execute(select_query, (idItem,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_item_image_by_name(self,nameItem:str) -> str:
        select_query = "SELECT image FROM Items WHERE name = ?;"
        self.cursor.execute(select_query, (nameItem,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_item_id_by_name(self,nameItem:str) -> int:
        select_query = "SELECT id FROM Items WHERE name = ?;"
        self.cursor.execute(select_query, (nameItem,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_item_name_by_id(self,idItem:int) -> str:
        select_query = "SELECT name FROM Items WHERE id = ?;"
        self.cursor.execute(select_query, (idItem,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_random_item(self) -> dict:
        self.cursor.execute("SELECT * FROM Items WHERE description != '' ORDER BY RANDOM() LIMIT 1;")
        res = self.cursor.fetchone()
        return {
            "id":res[0],
            "name":res[1],
            "image":res[2],
            "description": res[3]
        }
    def get_item_by_id(self,idItem:int) -> dict:
        select_query = "SELECT * FROM Items WHERE id = ? AND description != '';"
        self.cursor.execute(select_query, (idItem,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "name":res[1],
                "image":res[2],
                "description":res[3]
            }
        return None
    def get_item_by_name(self,nameItem:str) -> dict:
        select_query = "SELECT * FROM Items WHERE name = ? AND description != '';"
        self.cursor.execute(select_query, (nameItem,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "name":res[1],
                "image":res[2],
                "description":res[3]
            }
        return None
    def get_all_items_in_list(self) -> list:
        self.cursor.execute("SELECT * FROM Items WHERE description != '' ORDER BY name ASC;")
        items = self.cursor.fetchall()
        return [
            {
                "id":item[0],
                "name":item[1],
                "image":item[2],
                "description": item[3]
            }
            for item in items
        ]
    def get_all_items_in_list_start_with(self,lettre:str) -> list:
        if lettre == "E":
            self.cursor.execute("SELECT * FROM Items WHERE description != '' AND name LIKE 'É%' ORDER BY name ASC;")
            items = self.cursor.fetchall()
            self.cursor.execute("SELECT * FROM Items WHERE description != '' AND name LIKE '"+lettre+"%' ORDER BY name ASC;")
            items += self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT * FROM Items WHERE description != '' AND name LIKE '"+lettre+"%' ORDER BY name ASC;")
            items = self.cursor.fetchall()
        if items:

            return [
                {
                    "id":item[0],
                    "name":item[1],
                    "image":item[2],
                    "description": item[3]
                }
                for item in items
            ]
        else:
            return None


        select_query = "SELECT * FROM Items WHERE description != '';"
        self.cursor.execute(select_query)
        res_items = self.cursor.fetchall()

        liste_items = [
            {
                "id":item[0],
                "name":item[1],
                "image":item[2],
                "description":item[3],
            }
            for item in res_items
        ]
        return liste_champions + liste_items

    def get_emoji(self,idThing:int) -> dict:
        select_query = "SELECT * FROM Emojis WHERE id_thing = ?;"
        self.cursor.execute(select_query, (idThing,))
        res = self.cursor.fetchone()
        return {
            "id":res[0],
            "nom_emoji":res[1],
            "id_thing":res[2],
            "serveur_id":res[3]
        }
    def get_serveur_id(self, idThing:int) ->int:
        self.cursor.execute("SELECT serveur_id FROM Emojis WHERE id_thing = ?", (idThing,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def suppr_emojiDB(self, idThing:int) -> int:
        self.cursor.execute("DELETE FROM Emojis WHERE id_thing = ?", (idThing,))
        self.conn.commit()



    def get_level(self, numLevel:int) ->dict:
        self.cursor.execute("SELECT * FROM PaliersNiveau WHERE niveau = ?", (numLevel,))
        res = self.cursor.fetchone()
        if res:
            return {
                "niveau":res[0],
                "exp_requis":res[1]
            }
        return None
    def gainLevel(self, idJoueur:int, niveau:int, xp:int):
        self.cursor.execute("UPDATE Joueur SET niveau = ?, xp = ? WHERE id = ?",(niveau, xp, idJoueur))
        self.conn.commit()
    
    def insert_joueur_in_db(self,idJoueur:int, nomJoueur:str, niveau:int = 0, xp:int = 0, gold:int = 0, lasthourly:int = 0, lastdaily:int = 0):
        query = "INSERT INTO Joueur (id, name, niveau, xp, gold, lasthourly, lastdaily) VALUES (?, ?, ?, ?, ?, ?, ?);"
        self.cursor.execute(query, (idJoueur,nomJoueur,niveau,xp,gold, lasthourly, lastdaily))
        self.conn.commit()
    def update_jeu_gagnant(self,idGame:int, idGagnant:int, xpGain:int, goldGain:int) -> bool:
        lvlUp = None
        joueur = self.get_joueur_by_id(idGagnant)
        prochainLevel = self.get_level(joueur["niveau"]+1)
        if xpGain+joueur["xp"] >= prochainLevel["exp_requis"]:
            xpJoueur = xpGain+joueur["xp"] - prochainLevel["exp_requis"]
            self.gainLevel(idGagnant, joueur["niveau"]+1, xpJoueur)
            self.cursor.execute("UPDATE Joueur SET gold = ? WHERE id = ?",(goldGain+joueur["gold"]+200, idGagnant))
            lvlUp = joueur["niveau"]+1
        else:
            self.cursor.execute("UPDATE Joueur SET xp = ?, gold = ? WHERE id = ?", (xpGain+joueur["xp"], goldGain+joueur["gold"], idGagnant))
        update_query = "UPDATE JeuDle SET idGagnant = ? WHERE id = ?;"
        
        self.cursor.execute(update_query, (idGagnant, idGame))
        self.conn.commit()
        return lvlUp
    
    def get_joueur_daily_by_id(self,idJoueur:int) -> int:
        query = "SELECT lastdaily FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_joueur_hourly_by_id(self,idJoueur:int) -> int:
        query = "SELECT lasthourly FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None

    def daily_use_by(self, idJoueur:int, lastdaily:int):
        gold = self.get_joueur_gold_by_id(idJoueur) + 3600
        self.cursor.execute("UPDATE Joueur SET lastdaily = ?, gold = ? WHERE id = ?",(lastdaily, gold, idJoueur))
        self.conn.commit()
    def hourly_use_by(self, idJoueur:int, lasthourly:int):
        gold = self.get_joueur_gold_by_id(idJoueur) + 130
        self.cursor.execute("UPDATE Joueur SET lasthourly = ?, gold = ? WHERE id = ?",(lasthourly, gold, idJoueur))
        self.conn.commit()

    def if_joueur_in_db(self, idJoueur:int):
        query = "SELECT * FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        return self.cursor.fetchone() != None

    def get_joueur_by_id(self,idJoueur:int) -> dict:
        query = "SELECT * FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "name":res[1],
                "name_lol":res[2],
                "niveau":res[3],
                "xp":res[4],
                "gold":res[5],
                "lasthourly":res[6],
                "lastdaily":res[7],
            }
        return None
    def get_joueur_by_name(self,nomJoueur:str) -> dict:
        query = "SELECT * FROM Joueur WHERE name = ?;"
        self.cursor.execute(query, (nomJoueur,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "name":res[1],
                "name_lol":res[2],
                "niveau":res[3],
                "xp":res[4],
                "gold":res[5],
                "lasthourly":res[6],
                "lastdaily":res[7],
            }
        return None
    def get_joueur_gold_by_id(self,idJoueur:int) -> int:
        query = "SELECT gold FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res != None:
            return res[0]
        return None
    def get_joueur_gold_by_name(self,nomJoueur:str) -> int:
        query = "SELECT gold FROM Joueur WHERE name = ?;"
        self.cursor.execute(query, (nomJoueur,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_joueur_niv_by_id(self,idJoueur:int) -> int:
        query = "SELECT niveau FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res != None:
            return res[0]
        return None
    def get_joueur_niv_by_name(self,nomJoueur:str) -> int:
        query = "SELECT niveau FROM Joueur WHERE name = ?;"
        self.cursor.execute(query, (nomJoueur,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_joueur_xp_by_id(self,idJoueur:int) -> int:
        query = "SELECT xp FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_joueur_xp_by_name(self,nomJoueur:str) -> int:
        query = "SELECT xp FROM Joueur WHERE name = ?;"
        self.cursor.execute(query, (nomJoueur,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None
    def get_joueur_lol_by_id(self,idJoueur:int) -> str:
        query = "SELECT name_lol FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None

    def get_emoji_mastery(self, idMastery:int):
        self.cursor.execute("SELECT emoji FROM MasteryIcon WHERE level = ?",(idMastery,))
        res = self.cursor.fetchone()
        if res:
            return res[0]
        return None

    def add_compte_lol_to_joueur(self, idJoueur:str, pseudo:str):
        self.cursor.execute("UPDATE Joueur SET name_lol = ? WHERE id = ?",(pseudo, idJoueur))
        self.conn.commit()
    
    
    def if_compte_lol_in_db(self, idCompteLol:str) -> bool:
        query = "SELECT * FROM CompteLol WHERE id = ?;"
        self.cursor.execute(query, (idCompteLol,))
        return self.cursor.fetchone() != None
    
    def if_masterychamp_in_db(self, puuid:str, summonerId:str, champId:int) ->bool:
        self.cursor.execute("SELECT * FROM MasteryChampion WHERE puuid = ? AND summonerId = ? AND championId = ?",(puuid, summonerId, champId))
        return self.cursor.fetchone() != None

    def add_compte_lol(self, info_joueur:dict, info_league:list, info_mastery:list):
        self.cursor.execute("INSERT INTO CompteLol VALUES(?,?,?,?,?,?,?);",(info_joueur["id"],info_joueur["accountId"],info_joueur["puuid"],info_joueur["name"], f"https://ddragon.leagueoflegends.com/cdn/{self.versionLol}/img/profileicon/{str(info_joueur['profileIconId'])}.png",info_joueur["profileIconId"],info_joueur["summonerLevel"]))
        self.conn.commit()
        for league in info_league:
            if league["tier"] == "MASTER" or league["tier"] == "GRANDMASTER" or league["tier"] == "CHALLENGER":
                league['rank'] = ""
            self.cursor.execute("INSERT INTO LeagueLol VALUES(?,?,?,?,?,?,?,?,?)", (league["leagueId"],league["queueType"],translate_ranked[league["tier"]],league["rank"],league["summonerId"],league["summonerName"],league["leaguePoints"],league["wins"],league["losses"]))
            self.conn.commit()
        for champ in info_mastery:
            self.cursor.execute("INSERT INTO MasteryChampion VALUES(?,?,?,?,?)",(champ["puuid"], champ["championId"], champ["championLevel"], champ["championPoints"], champ["summonerId"]))
            self.conn.commit()

    def update_compte_lol(self, info_joueur:dict, info_league:list, info_mastery:list):
        self.cursor.execute("UPDATE CompteLol SET name = ?, profileIconUrl = ?, profileIconId = ?, summonerLevel = ? WHERE id = ?;",(info_joueur["name"], f"https://ddragon.leagueoflegends.com/cdn/{self.versionLol}/img/profileicon/{str(info_joueur['profileIconId'])}.png", info_joueur["profileIconId"],info_joueur["summonerLevel"], info_joueur["id"]))
        self.conn.commit()
        for league in info_league:
            if league["tier"] == "MASTER" or league["tier"] == "GRANDMASTER" or league["tier"] == "CHALLENGER":
                league['rank'] = ""
            self.cursor.execute("SELECT * FROM LeagueLol WHERE leagueId = ?",(league["leagueId"],))
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO LeagueLol VALUES(?,?,?,?,?,?,?,?,?)", (league["leagueId"],league["queueType"],translate_ranked[league["tier"]],league["rank"],league["summonerId"],league["summonerName"],league["leaguePoints"],league["wins"],league["losses"]))
                self.conn.commit()
            else:
                self.cursor.execute("UPDATE LeagueLol SET tier = ?, rank = ?, summonerName = ?, leaguePoints = ?, wins = ?, losses = ? WHERE leagueId = ? AND summonerId = ?", (translate_ranked[league["tier"]],league["rank"],league["summonerName"],league["leaguePoints"],league["wins"],league["losses"],league["leagueId"],league["summonerId"]))
                self.conn.commit()
        self.cursor.execute("DELETE FROM MasteryChampion WHERE puuid = ? AND summonerId = ?", (info_joueur["puuid"], info_joueur["id"]))
        self.conn.commit()
        for champ in info_mastery:
            self.cursor.execute("INSERT INTO MasteryChampion VALUES(?,?,?,?,?)",(champ["puuid"], champ["championId"], champ["championLevel"], champ["championPoints"], champ["summonerId"]))
            self.conn.commit()

    def get_compte_lol(self, pseudo:str) -> dict:
        self.cursor.execute("SELECT * FROM CompteLol WHERE name = ?", (pseudo,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "accountId":res[1],
                "puuid":res[2],
                "name":res[3],
                "profileIconUrl":res[4],
                "profileIconId":res[5],
                "summonerLevel":res[6],
            }
        return None
    def get_league_lol(self, summonerId:str) -> list:
        self.cursor.execute("SELECT * FROM LeagueLol WHERE summonerId = ?",(summonerId,))
        res = self.cursor.fetchall()
        if res:
            return [
                {
                    "queueType":league[1],
                    "tier":league[2],
                    "rank":league[3],
                    "leaguePoints":league[6],
                    "wins":league[7],
                    "losses":league[8]
                }
                for league in res
            ]
        return None
    def get_mastery_lol(self, puuid:str,summonerId:str):
        self.cursor.execute("SELECT Champions.name, Champions.id, MasteryChampion.championLevel, MasteryChampion.championPoints FROM MasteryChampion,Champions WHERE MasteryChampion.championId = Champions.id AND MasteryChampion.summonerId = ? AND MasteryChampion.puuid = ? ",(summonerId,puuid))
        res = self.cursor.fetchall()
        if res:
            return [
                {
                    "name":champ[0],
                    "id":champ[1],
                    "level":champ[2],
                    "points":champ[3],
                }
                for champ in res
            ]
        return None

    def get_ranked_icon(self, nameRanked:str) -> str:
        self.cursor.execute("SELECT image, emoji FROM RankedIcon WHERE name = ?",(nameRanked,))
        return self.cursor.fetchone()

    def get_game_id(self, channelId:str, guildId:str, gagnant:bool):
        if gagnant:
            self.cursor.execute("SELECT id FROM JeuDle WHERE channelId = ? AND guildId = ?;", (channelId, guildId))
        else:
            self.cursor.execute("SELECT id FROM JeuDle WHERE channelId = ? AND guildId = ? AND idGagnant IS NULL;", (channelId, guildId))
        gameId = self.cursor.fetchone()
        if gameId:
            return gameId[0]
        return None
    def add_game(self, channelId:str, guildId:str, typeJeu:str, mot:str, difficulte:str):
        insert_query = "INSERT INTO JeuDle (channelId, guildId, typeJeu, mot, difficulte) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, difficulte))
        self.conn.commit()
    def get_game_by_id(self, gameId:int, gagnant:bool) -> dict:
        if gagnant:
            self.cursor.execute("SELECT * FROM JeuDle WHERE id = ?;", (gameId, ))
        else:
            self.cursor.execute("SELECT * FROM JeuDle WHERE id = ? AND idGagnant IS NULL;", (gameId, ))
        game = self.cursor.fetchone()
        if game:
            return {
                "id":game[0],
                "channelId":game[1],
                "guildId":game[2],
                "typeJeu":game[3],
                "mot":game[4],
                "difficulte":game[5],
                "message_indice_id":game[6],
                "message_warn_id":game[7],
                "idGagnant":game[8],
            }
        return None
        return None
    def get_game_by_channel_and_guild(self, channelId:str, guildId:str, gagnant:bool) -> dict:
        if gagnant:
            self.cursor.execute("SELECT * FROM JeuDle WHERE channelId = ? AND guildId = ?;", (channelId, guildId))
        else:
            self.cursor.execute("SELECT * FROM JeuDle WHERE channelId = ? AND guildId = ? AND idGagnant IS NULL;", (channelId, guildId))
        game = self.cursor.fetchone()
        if game:
            return {
                "id":game[0],
                "channelId":game[1],
                "guildId":game[2],
                "typeJeu":game[3],
                "mot":game[4],
                "difficulte":game[5],
                "message_indice_id":game[6],
                "message_warn_id":game[7],
                "idGagnant":game[8],
            }
        return None

    async def timer_indice(self,interaction:discord.Interaction, gameId:int, typeJeu:str, channelId : str, guildId:str, mot:str):
        liste_lettre = []
        liste_pos_lettre = []
        for lettre in mot:
            if lettre == " ":
                liste_pos_lettre.append(True)
                liste_lettre.append(" ")
            elif lettre == "-":
                liste_pos_lettre.append(True)
                liste_lettre.append("-")
            elif lettre == ".":
                liste_pos_lettre.append(True)
                liste_lettre.append(".")
            elif lettre == ",":
                liste_pos_lettre.append(True)
                liste_lettre.append(",")
            elif lettre == "'":
                liste_pos_lettre.append(True)
                liste_lettre.append("'")
            else:
                liste_pos_lettre.append(False)
                liste_lettre.append("_")
        message_indice = await interaction.channel.send(embed=get_embed_indice(liste_lettre))
        await message_indice.edit(embed=get_embed_indice(liste_lettre), view = StopGame(self.bot, gameId, message_indice.id, typeJeu, mot))
        
        update_query = "UPDATE JeuDle SET message_indice_id = ? WHERE id = ?;"
        self.cursor.execute(update_query, (str(message_indice.id),gameId))
        self.conn.commit()
        n = 0
        for bool in liste_pos_lettre:
            if not bool:
                n += 1
        secondint = 5*(n-1)
        moitie = secondint//2
        if typeJeu == "champion":
            champ = True
            roles = self.get_roles_champion_by_name(mot)
            annee_sortie = self.get_champion_annee_by_name(mot)
        else:
            champ = False
        while True:
            if secondint == 0 and self.get_game_by_id(gameId, gagnant=False):
                message_attention = await interaction.channel.send("Vous avez 10 seconds pour trouver le mot.")
                self.cursor.execute("UPDATE JeuDle SET message_warn_id = ? WHERE id = ?;", (str(message_attention.id), gameId))
                self.conn.commit()
                await asyncio.sleep(10)
                
                game = self.get_game_by_id(gameId, gagnant=False)
                if game:
                    await message_attention.delete()
                    await message_indice.delete()
                    difficulte= game["difficulte"]
                    try:
                        self.cursor.execute("DELETE FROM JeuDle WHERE id = ?;", (game["id"],))
                        self.conn.commit()
                    except:
                        print("delete deja fais")
                    embed = discord.Embed()
                    embed.set_author(name="Fin de partie")
                    if game["typeJeu"] == "item":
                        embed.set_image(url=self.get_item_image_by_name(game["mot"]))
                        embed.description = "L'item était : "+game["mot"]
                    elif game["typeJeu"] == "champion":
                        embed.set_image(url=self.get_champion_splash_by_name(game["mot"]))
                        embed.description = "Le champion était : "+game["mot"]
                    await interaction.channel.send(embed=embed, view=self.bot.rejouerBtn(self.bot, game["typeJeu"], difficulte))
                break
            try:
                if secondint % 5 == 0:
                    for i in range(1):
                        pos = random.randint(0, n-1)
                        while liste_pos_lettre[pos]:
                            pos = random.randint(0, n-1)
                        liste_lettre[pos] = mot[pos]
                        liste_pos_lettre[pos] = True
                    embed = get_embed_indice(liste_lettre)
                    if secondint <= moitie and champ:
                        embed.add_field(name="Année de sortie", value=str(annee_sortie))
                        embed.add_field(name="Rôle principal", value=roles[0]["name"])
                    await message_indice.edit(embed=embed)
                secondint = secondint - 1
            except:
                break
            await asyncio.sleep(1)

    async def replace_emoji(self, guild:discord.Guild, newName:str, newUrl:str, oldIdThing:int):
        print(guild.name)
        oldEmojiDB = self.get_emoji(oldIdThing)
        oldEmoji = guild.get_emoji(int(oldEmojiDB["id"]))
        if oldEmoji:
            await guild.delete_emoji(oldEmoji)
        await asyncio.sleep(1.5)
        async with aiohttp.ClientSession() as session:
            async with session.get(newUrl) as resp:
                if resp.status == 200:
                    emoji_data = await resp.read()
                    emoji = await guild.create_custom_emoji(name=newName, image=emoji_data)
                    await asyncio.sleep(1.5)
                    return emoji
                else:
                    return None

    async def ajout_emoji_in_serveur(guild:discord.Guild, name:str, url:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    emoji_data = await resp.read()
                    emoji = await guild.create_custom_emoji(name=name, image=emoji_data)
                    return emoji
                else:
                    return None
    
    async def suppr_emoji(self, guild:discord.Guild, id_thing:int):
        emojiDB = self.get_emoji(id_thing)
        emoji = guild.get_emoji(emojiDB["id"])
        if emoji:
            await emoji.delete()
            await asyncio.sleep(1.5)
    
    def ajout_version(self, new_version:str):
        self.cursor.execute("INSERT INTO versions VALUES(?)", (new_version,))
        self.conn.commit()

    def has_version(self, version:str) -> bool:
        self.cursor.execute("SELECT * FROM versions WHERE version = ?;", (version,))
        res = self.cursor.fetchone()
        return res != None
    
    def delete_champion_by_id(self, idChampion:int):
        self.cursor.execute("DELETE FROM Champions WHERE id = ?", (idChampion,))
        self.conn.commit()
    def delete_item_by_id(self, idItem:int):
        self.cursor.execute("DELETE FROM Items WHERE id = ?", (idItem,))
        self.conn.commit()
    def delete_champion_by_name(self, nameChampion:str):
        self.cursor.execute("DELETE FROM Champions WHERE name = ?", (nameChampion,))
        self.conn.commit()
    def delete_item_by_name(self, nameItem:str):
        self.cursor.execute("DELETE FROM Items WHERE name = ?", (nameItem,))
        self.conn.commit()

    def add_champion(self, id:int, name:str, image:str, title:str, splash_art:str):
        insert_query = "INSERT INTO Champions (id, name, image, title, splash_art) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(insert_query, (id, name, image, title, splash_art))
        self.conn.commit()
    def add_item(self, id:int, name:str, image:str, description:str):
        insert_query = "INSERT INTO Items (id, name, image, description) VALUES (?, ?, ?, ?);"
        self.cursor.execute(insert_query, (id, name, image, description))
        self.conn.commit()

    def get_all_regions(self) -> list:
        self.cursor.execute("SELECT * FROM Regions;")
        regions = self.cursor.fetchall()
        if regions:
            res = []
            for region in regions:
                res.append({
                    "id":region[0],
                    "name":region[1],
                    "logo":region[2],
                    "splash":region[3],
                    "description":region[4]
                })
            return res
        return None
    def get_region_by_name(self, nameRegion:str) -> dict:
        self.cursor.execute("SELECT * FROM Regions WHERE name = ?;", (nameRegion,))
        region = self.cursor.fetchone()
        if region:
            return {
                "id":region[0],
                "name":region[1],
                "logo":region[2],
                "splash":region[3],
                "description":region[4]
            }
        return None
    def get_region_by_id(self, idRegion:int) -> dict:
        self.cursor.execute("SELECT * FROM Regions WHERE id = ?;", (idRegion,))
        region = self.cursor.fetchone()
        if region:
            return {
                "id":region[0],
                "name":region[1],
                "logo":region[2],
                "splash":region[3],
                "description":region[4]
            }
        return None

    def joueur_has_skin_or_chroma(self, idJoueur:int, id_thing:int) -> bool:
        self.cursor.execute("SELECT * FROM JoueurSkins WHERE joueurId = ? AND id_thing = ?", (idJoueur, id_thing))
        return self.cursor.fetchone() != None
    

    def get_rarity(self, rarity:str):
        self.cursor.execute("SELECT * FROM RaritySkinsChromas WHERE name = ?", (rarity,))
        res = self.cursor.fetchone()
        return {
            "name":res[0],
            "proba":res[1],
            "emoji":res[2],
            "image":res[3],
            "couleur":res[4],
        }
    def get_random_rarity(self):
        r = round(random.uniform(0, 1), 4)
        self.cursor.execute("SELECT * FROM RaritySkinsChromas WHERE ? <= probabilite ORDER BY probabilite LIMIT 1;", (r,))
        res = self.cursor.fetchone()
        return {
            "name":res[0],
            "proba":res[1],
            "emoji":res[2],
            "image":res[3],
            "couleur":res[4],
        }
    def get_random_skin_by_rarity(self, joueurId:int, rarity:str):
        self.cursor.execute("""SELECT Skin.*
        FROM Skin
        LEFT JOIN JoueurSkins ON Skin.id = JoueurSkins.id_thing AND JoueurSkins.joueurId = ?
        WHERE Skin.rarity = ? AND (JoueurSkins.quantite IS NULL OR JoueurSkins.quantite < 1)
        ORDER BY RANDOM()
        LIMIT 1;""", (joueurId, rarity))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "championId":res[1],
                "name":res[2],
                "isBase":res[3],
                "rarity":res[4],
                "splashPath":res[5],
                "tilePath":res[6],
                "loadScreenPath":res[7],
                "hasChroma":res[8],
            }
        return None

    def get_total_skins_chroma(self, joueurId:int = None):
        res = 0
        if joueurId:
            self.cursor.execute("SELECT COUNT(*) FROM JoueurSkins WHERE joueurId = ?;", (joueurId,))
            res += self.cursor.fetchone()[0]
        else:
            self.cursor.execute("SELECT COUNT(*) FROM Chroma;")
            res += self.cursor.fetchone()[0]
            self.cursor.execute("SELECT COUNT(*) FROM Skin;")
            res += self.cursor.fetchone()[0]
        return res
    
    def get_total_skins(self, joueurId:int = None, id_thing:int = None) -> int:
        res = 0
        if id_thing and joueurId:
            self.cursor.execute("SELECT quantite FROM JoueurSkins WHERE joueurId = ? AND id_thing = ?;", (joueurId,id_thing))
            count = self.cursor.fetchone()
            if count:
                res += count[0]
        elif joueurId:
            self.cursor.execute("SELECT COUNT(*) FROM JoueurSkins WHERE joueurId = ? AND type = 'skin';", (joueurId,))
            res += self.cursor.fetchone()[0]
        else:
            self.cursor.execute("SELECT COUNT(*) FROM Skin;")
            res += self.cursor.fetchone()[0]
        return res
    
    def get_total_skins_possible(self, joueurId:int = None) -> int:
        res = 0
        if joueurId:
            self.cursor.execute("SELECT quantite FROM JoueurSkins WHERE joueurId = ? AND type = 'skin';", (joueurId,))
            for nombre in self.cursor.fetchall():
                res += nombre[0]
        else:
            self.cursor.execute("SELECT COUNT(*) FROM Skin;")
            res += self.cursor.fetchone()[0]*1
        return res
    
    def get_total_chromas(self, joueurId:int = None, id_thing:int = None):
        if id_thing and joueurId:
            self.cursor.execute("SELECT quantite FROM JoueurSkins WHERE joueurId = ? AND id_thing = ?;", (joueurId,id_thing))
            count = self.cursor.fetchone()
            if count:
                res = count[0]
            else:
                res = 0
        elif joueurId:
            self.cursor.execute("SELECT COUNT(*) FROM JoueurSkins WHERE joueurId = ? AND type = 'chroma';", (joueurId,))
            res = self.cursor.fetchone()[0]
        else:
            self.cursor.execute("SELECT COUNT(*) FROM Chroma;")
            res = self.cursor.fetchone()[0]
        return res
    
    def get_chromas_of(self, idSkin:int) -> list:
        self.cursor.execute("SELECT * FROM Chroma WHERE skinId = ?", (idSkin,))
        return [
            {
                "id":chroma[0],
                "name":chroma[1],
                "chromaPath":chroma[2],
                "color":chroma[3],
            }
            for chroma in self.cursor.fetchall()
        ]

    def tirage_skin(self, idJoueur:int, nombre:int, prix:int):
        totauxskins = self.get_total_skins_possible()
        totauxskinsjoueur = self.get_total_skins_possible(idJoueur)
        if totauxskins - nombre + 1 > totauxskinsjoueur:
            res = []
            for i in range(nombre):
                rarity = self.get_random_rarity()
                skin = self.get_random_skin_by_rarity(idJoueur, rarity['name'])
                liste_rarity = []
                while skin == None:
                    liste_rarity.append(rarity)
                    while rarity in liste_rarity:
                        rarity = self.get_random_rarity()
                    skin = self.get_random_skin_by_rarity(idJoueur, rarity['name'])
                else:
                    quantite = self.get_total_skins(idJoueur, skin["id"])
                    res.append([quantite+1, "skin", skin, rarity])
            self.cursor.execute("UPDATE Joueur SET gold = gold-? WHERE id = ?",(prix,idJoueur))
            self.conn.commit()
            return res
        else:
            return None
        
    
    def tirage_chroma(self, idJoueur:int, idSkin:int):
        quantite_skin = self.get_total_skins(idJoueur, idSkin)
        if quantite_skin != 0:
            chromas = self.get_chromas_of(idSkin)
            longueur = len(chromas)
            r = random.randint(0, longueur-1)
            quantite = self.get_total_chromas(idJoueur, chromas[r]["id"])
            return [quantite+1, "chroma", chromas[r]]
        else:
            return None
    
    def get_all_skins_of(self, idJoueur:int, rarity:str = None):
        if rarity:
            self.cursor.execute("""
            SELECT Skin.*
            FROM JoueurSkins
            JOIN Skin ON JoueurSkins.id_thing = Skin.id
            JOIN Champions ON Champions.id = Skin.championId
            WHERE JoueurSkins.type = 'skin'
                AND Skin.rarity = ?
                AND JoueurSkins.joueurId = ?
            ORDER BY Champions.name ASC;
            """,(rarity, idJoueur))
        else:
            self.cursor.execute("""
            SELECT Skin.*
            FROM JoueurSkins
            JOIN Skin ON JoueurSkins.id_thing = Skin.id
            JOIN Champions ON Champions.id = Skin.championId
            JOIN RaritySkinsChromas ON RaritySkinsChromas.name = Skin.rarity
            WHERE JoueurSkins.type = 'skin'
                AND JoueurSkins.joueurId = ?
            ORDER BY RaritySkinsChromas.probabilite ASC;
            """,(idJoueur,))
        res = self.cursor.fetchall()
        if res != None:
            return [
                {
                    "id" : skin[0],
                    "championId" : skin[1],
                    "name" : skin[2],
                    "isBase" : skin[3],
                    "rarity" : skin[4],
                    "splashPath" : skin[5],
                    "tilePath" : skin[6],
                    "loadScreenPath" : skin[7],
                    "hasChroma" : skin[8]
                } for skin in res
            ]
        return None
            
    # def tirage_skin_or_chroma(self, idJoueur:int):
    #     rarity = self.get_random_rarity()
    #     skin = self.get_random_skin_by_rarity(idJoueur, rarity)
    #     if skin["hasChroma"] == 1:
    #         chromas = self.get_chromas_of(skin["id"])
    #         r = random.randint(0, len(chromas))
    #         if r == len(chromas):
    #             quantite = self.get_total_skins(idJoueur, skin["id"])
    #             return [quantite+1, "skin", skin]
                
    #         else:
    #             quantite = self.get_total_chromas(idJoueur, chromas[r]["id"])
    #             return [quantite+1, "chroma", chromas[r]]
    #     else:
    #         quantite = self.get_total_skins(idJoueur, skin["id"])
    #         return [quantite+1, "skin", skin]

def get_embed_indice(liste_lettre:list)->Embed:
    embed = Embed()
    mot = "`"
    for lettre in liste_lettre:
        mot+=lettre
    mot += "`"
    embed.description = ":bulb: **Indice** "+mot
    return embed