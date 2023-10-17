import sqlite3
import asyncio
import aiohttp
import random
import discord
from discord import Embed
from Boutton.StopGameBoutton import StopGame
from Boutton.RejouerItemChampionBoutton import Rejouer
from unidecode import unidecode
import time


class DB:
    def __init__(self, versionLol:str) -> None:
        self.conn = sqlite3.connect('DB/LeagueDle.db')
        self.cursor = self.conn.cursor()
        self.versionLol = versionLol

    
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
                "description": champion[3],
                "splash_art":champion[4]
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
                    "description": champion[3]
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
    
    def update_champion_when_lol_update(self, info_champ):
        insert_query = "SELECT * FROM Champions WHERE id = ?"
        self.cursor.execute(insert_query, (info_champ.id,))
        old_info = self.cursor.fetchall()
        if info_champ.image != old_info[2]:
            self.cursor.execute("UPDATE Champions SET image = ? WHERE id = ?", (info_champ.image, info_champ.id))
        if info_champ.title != old_info[3]:
            self.cursor.execute("UPDATE Champions SET title = ? WHERE id = ?", (info_champ.title, info_champ.id))
        if info_champ.splash_art != old_info[4]:
            self.cursor.execute("UPDATE Champions SET splash_art = ? WHERE id = ?", (info_champ.splash_art, info_champ.id))
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

    def get_tous_infos(self)->list:
        select_query = "SELECT * FROM Champions;"
        self.cursor.execute(select_query)

        res_champs = self.cursor.fetchall()
        liste_champions = [
            {
                "id":champ[0],
                "name":champ[1],
                "image":champ[2],
                "title":champ[3],
                "splash_art":champ[4],
            }
            for champ in res_champs
        ]

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

    def get_emoji(self,idThing:str) -> dict:
        select_query = "SELECT * FROM Emojis WHERE id_thing = ?;"
        self.cursor.execute(select_query, (idThing,))
        res = self.cursor.fetchone()
        return {
            "id":res[0],
            "nom_emoji":res[1],
            "id_thing":res[2]
        }
    
    def get_joueur_by_id(self,idJoueur:str) -> dict:
        query = "SELECT * FROM Joueur WHERE id = ?;"
        self.cursor.execute(query, (idJoueur,))
        res = self.cursor.fetchone()
        if res:
            return {
                "id":res[0],
                "name":res[1],
                "avatar_url":res[2]
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
                "avatar_url":res[2]
            }
        return None
    def insert_joueur_in_db(self,idJoueur:str, nomJoueur:str, avatarUrl:str):
        query = "INSERT INTO Joueur (id, name, avatar_url) VALUES (?, ?, ?);"
        self.cursor.execute(query, (idJoueur,nomJoueur,avatarUrl))
        self.conn.commit()
    def update_jeu_gagnant(self,idGame:int, idGagnant:str):
        update_query = "UPDATE Jeu SET idGagnant = ? WHERE id = ?;"
        self.cursor.execute(update_query, (idGagnant, idGame))
        self.conn.commit()
    
    def get_game_id(self, channelId:str, guildId:str, gagnant:bool):
        if gagnant:
            self.cursor.execute("SELECT id FROM Jeu WHERE channelId = ? AND guildId = ?;", (channelId, guildId))
        else:
            self.cursor.execute("SELECT id FROM Jeu WHERE channelId = ? AND guildId = ? AND idGagnant IS NULL;", (channelId, guildId))
        gameId = self.cursor.fetchone()
        if gameId:
            return gameId[0]
        return None
    def add_game(self, channelId:str, guildId:str, typeJeu:str, mot:str, difficulte:str):
        insert_query = "INSERT INTO Jeu (channelId, guildId, typeJeu, mot, difficulte) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, difficulte))
        self.conn.commit()
    def get_game_by_id(self, gameId:int, gagnant:bool) -> dict:
        if gagnant:
            self.cursor.execute("SELECT * FROM Jeu WHERE id = ?;", (gameId, ))
        else:
            self.cursor.execute("SELECT * FROM Jeu WHERE id = ? AND idGagnant IS NULL;", (gameId, ))
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
            self.cursor.execute("SELECT * FROM Jeu WHERE channelId = ? AND guildId = ?;", (channelId, guildId))
        else:
            self.cursor.execute("SELECT * FROM Jeu WHERE channelId = ? AND guildId = ? AND idGagnant IS NULL;", (channelId, guildId))
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
        await message_indice.edit(embed=get_embed_indice(liste_lettre), view = StopGame(self, gameId, message_indice.id, typeJeu, mot))
        
        update_query = "UPDATE Jeu SET message_indice_id = ? WHERE id = ?;"
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
            if secondint == 0:
                message_attention = await interaction.channel.send("Vous avez 10 seconds pour trouver le mot.")
                self.cursor.execute("UPDATE Jeu SET message_warn_id = ? WHERE id = ?;", (str(message_attention.id), gameId))
                self.conn.commit()
                await asyncio.sleep(10)
                
                game = self.get_game_by_id(gameId, gagnant=False)
                if game:
                    await message_attention.delete()
                    await message_indice.delete()
                    difficulte= game["difficulte"]
                    try:
                        self.cursor.execute("DELETE FROM Jeu WHERE id = ?;", (game["id"],))
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
                    await interaction.channel.send(embed=embed, view=Rejouer(self, game["typeJeu"], difficulte))
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

    async def ajout_emote(guild:discord.Guild,name:str, url:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    emoji_data = await resp.read()
                    emoji = await guild.create_custom_emoji(name=name, image=emoji_data)
                    return emoji
                else:
                    return None
    # async def suppr_all_emojis(self,guild:discord.Guild):
    #     emojis = await guild.fetch_emojis()
    #     for emoji in emojis:
    #         await emoji.delete()
    #         time.sleep(0.5)
    # async def update_emoji(self, liste_serveur_emoji:list):
    #     self.cursor.execute("DELETE FROM Emojis;")
    #     self.conn.commit()
    #     tous_infos = self.get_tous_infos()
    #     compteur = 0
    #     for i in range(0, len(liste_serveur_emoji)):
    #         serveur = liste_serveur_emoji[i]
    #         await self.suppr_all_emojis(serveur)
    #         for j in range(50):
    #             if compteur >= len(tous_infos):
    #                 break
    #             try:
    #                 info = tous_infos[compteur]
    #                 id_info = info["id"]
    #                 name_info_for_emote = info["name"].replace("'","").replace(" ", "").replace(".","").replace("-","").replace("œ","oe").replace(",","")
    #                 name_info_for_emote = unidecode(name_info_for_emote)

    #                 emoji = await self.ajout_emote(serveur, name_info_for_emote, info["image"])
                    
    #                 insert_query = "INSERT INTO Emojis (id, nom_emoji, id_thing) VALUES(?, ?, ?)"
    #                 self.cursor.execute(insert_query, (str(emoji.id), name_info_for_emote, str(id_info)))
    #                 self.conn.commit()
    #                 compteur += 1
    #                 time.sleep(1.5)
    #             except:
    #                 print("erreur")

    def has_version(self, version:str):
        self.cursor.execute("SELECT * FROM versions WHERE version = ?;", (version,))
        res = self.cursor.fetchone()
        return res != None
    
    def delete_all_items(self):
        self.cursor.execute("DELETE FROM Items")
        self.conn.commit()
    def delete_all_champions(self):
        self.cursor.execute("DELETE FROM Champions")
        self.conn.commit()
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

def get_embed_indice(liste_lettre:list)->Embed:
    embed = Embed()
    mot = "`"
    for lettre in liste_lettre:
        mot+=lettre
    mot += "`"
    embed.description = ":bulb: **Indice** "+mot
    return embed