import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from discord import app_commands
import aiohttp
import requests
import asyncio
import random
import re
import time
from unidecode import unidecode
import unicodedata

import sqlite3
conn = sqlite3.connect('DB/LeagueDle.db')
cursor = conn.cursor()

# bs4
# lxml
# unidecode

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

liste_serveur_emoji_id = [1154032237122158602, 1159513438310125698, 1159514828772229241, 1159514864616734760, 1159514890743054417, 1159514914491215963, 1159514941473165322, 1159514967905673279, 1159516097444323448]

versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()

assets = {
    "LoL" : {
        "name" : "League of Legends",
        "image-location": "assets/logo/League-of-Legends.png",
        "image" : "League-of-Legends.png"
    }
}

class League:
    ""
    def __init__(self) -> None:
        self.versions = versions
        self.items_info = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{self.versions[0]}/data/fr_FR/item.json").json()["data"]
        self.items = {self.items_info[item]["name"]: Item(self.items_info[item],self.versions[0]) for item in self.items_info}        
        self.champions_info = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{self.versions[0]}/data/fr_FR/champion.json").json()["data"]
        self.champions = {self.champions_info[champion]["name"]: Champion(self.champions_info[champion]) for champion in self.champions_info}

class Item:
    def __init__(self, info_item: dict, version:str) -> None:
        ""
        self.name = info_item["name"]
        image = info_item["image"]["full"]
        self.id = int(image.split(".")[0])
        self.image = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{image}"
        if info_item["description"] != "" and info_item["maps"]["11"] and not ("requiredAlly" in info_item) and "raritylegendary" not in self.name and not ("inStore"  in info_item):
            xml_data = info_item["description"]

            def remplacer_br(match):
                return '\n'
            
            self.description = re.sub(r'<br\s*/?>', remplacer_br, xml_data)
            self.description = re.sub(r'<.*?>', '', self.description)
        else:
            self.description = ""
        
class Champion:
    def __init__(self, info_champion: dict) -> None:
        ""
        self.name = info_champion["name"]
        self.id = info_champion["key"]
        self.image = f"https://ddragon.leagueoflegends.com/cdn/{info_champion['version']}/img/champion/{info_champion['image']['full']}"

        self.title = info_champion["title"]

        self.splash_art = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{info_champion['id']}_0.jpg"


# select_query = "SELECT * FROM versions WHERE version = ?;"
# cursor.execute(select_query, (versions[0],))
# res = cursor.fetchone()[0]
# if not res:
#     ## vide les table
#     league = League()
#     delete_query = "DELETE FROM items"
#     cursor.execute(delete_query)
#     delete_query = "DELETE FROM champions"
#     cursor.execute(delete_query)

#     conn.commit()

#     for champion in league.champions:
#         insert_query = "INSERT INTO champions (id, name, image, title, splash_art) VALUES (?, ?, ?, ?, ?);"
#         cursor.execute(insert_query, (league.champions[champion].id, league.champions[champion].name, league.champions[champion].image, league.champions[champion].title, league.champions[champion].splash_art))
#     for item in league.items:
#         insert_query = "INSERT INTO items (id, name, image, description) VALUES (?, ?, ?, ?)"
#         cursor.execute(insert_query, (league.items[item].id, league.items[item].name, league.items[item].image, league.items[item].description))

#     conn.commit()


def get_champion_image_by_id(idChampion:int) -> str:
    select_query = "SELECT image FROM champions WHERE id = ?;"
    cursor.execute(select_query, (idChampion,))
    res = cursor.fetchone()[0]
    return res
def get_champion_image_by_name(nameChampion:str) -> str:
    select_query = "SELECT image FROM champions WHERE name = ?;"
    cursor.execute(select_query, (nameChampion,))
    res = cursor.fetchone()[0]
    return res
def get_champion_id_by_name(nameChampion:str) -> int:
    select_query = "SELECT id FROM champions WHERE name = ?;"
    cursor.execute(select_query, (nameChampion,))
    res = cursor.fetchone()[0]
    return res
def get_champion_name_by_id(idChampion:int) -> str:
    select_query = "SELECT name FROM champions WHERE id = ?;"
    cursor.execute(select_query, (idChampion,))
    res = cursor.fetchone()[0]
    return res
def get_champion_splash_by_name(nameChampion:str) -> str:
    select_query = "SELECT splash_art FROM champions WHERE name = ?;"
    cursor.execute(select_query, (nameChampion,))
    res = cursor.fetchone()[0]
    return res
def get_champion_splash_by_id(idChampion:int) -> str:
    select_query = "SELECT splash_art FROM champions WHERE id = ?;"
    cursor.execute(select_query, (idChampion,))
    res = cursor.fetchone()[0]
    return res
def get_champion_by_name(nameChampion:str) -> dict:
    select_query = "SELECT * FROM champions WHERE name = ?;"
    cursor.execute(select_query, (nameChampion,))
    res = cursor.fetchone()[0]
    return {
        "id":res[0],
        "name":res[1],
        "image":res[2],
        "title":res[3],
        "splash_art":res[4],
    }
def get_champion_by_id(idChampion:int) -> dict:
    select_query = "SELECT * FROM champions WHERE id = ?;"
    cursor.execute(select_query, (idChampion,))
    res = cursor.fetchone()[0]
    return {
        "id":res[0],
        "name":res[1],
        "image":res[2],
        "title":res[3],
        "splash_art":res[4],
    }
def get_random_champion() -> dict:
    cursor.execute("SELECT * FROM champions ORDER BY RANDOM() LIMIT 1;")
    res = cursor.fetchone()
    return {
        "id":res[0],
        "name":res[1],
        "image":res[2],
        "description": res[3]
    }
def get_all_champions_in_list() -> list:
    cursor.execute("SELECT * FROM champions")
    champions = cursor.fetchall()
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


def get_item_image_by_id(idItem:int) -> str:
    select_query = "SELECT image FROM items WHERE id = ?;"
    cursor.execute(select_query, (idItem,))
    res = cursor.fetchone()
    if res:
        return res[0]
    return None
def get_item_image_by_name(nameItem:str) -> str:
    select_query = "SELECT image FROM items WHERE name = ?;"
    cursor.execute(select_query, (nameItem,))
    res = cursor.fetchone()
    if res:
        return res[0]
    return None
def get_item_id_by_name(nameItem:str) -> int:
    select_query = "SELECT id FROM items WHERE name = ?;"
    cursor.execute(select_query, (nameItem,))
    res = cursor.fetchone()
    if res:
        return res[0]
    return None
def get_item_name_by_id(idItem:int) -> str:
    select_query = "SELECT name FROM items WHERE id = ?;"
    cursor.execute(select_query, (idItem,))
    res = cursor.fetchone()
    if res:
        return res[0]
    return None
def get_random_item() -> dict:
    cursor.execute("SELECT * FROM items WHERE description != '' ORDER BY RANDOM() LIMIT 1;")
    res = cursor.fetchone()
    return {
        "id":res[0],
        "name":res[1],
        "image":res[2],
        "description": res[3]
    }
def get_item_by_id(idItem:int) -> dict:
    select_query = "SELECT * FROM items WHERE id = ? AND description != '';"
    cursor.execute(select_query, (idItem,))
    res = cursor.fetchone()
    if res:
        return {
            "id":res[0],
            "name":res[1],
            "image":res[2],
            "description":res[3]
        }
    return None
def get_item_by_name(nameItem:str) -> dict:
    select_query = "SELECT * FROM items WHERE name = ? AND description != '';"
    cursor.execute(select_query, (nameItem,))
    res = cursor.fetchone()
    if res:
        return {
            "id":res[0],
            "name":res[1],
            "image":res[2],
            "description":res[3]
        }
    return None
def get_all_items_in_list() -> list:
    cursor.execute("SELECT * FROM items WHERE description != '' ORDER BY name ASC;")
    items = cursor.fetchall()
    return [
        {
            "id":item[0],
            "name":item[1],
            "image":item[2],
            "description": item[3]
        }
        for item in items
    ]


def get_tous_infos()->list:
    select_query = "SELECT * FROM champions;"
    cursor.execute(select_query)

    res_champs = cursor.fetchall()
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

    select_query = "SELECT * FROM items WHERE description != '';"
    cursor.execute(select_query)
    res_items = cursor.fetchall()

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

def get_emoji(idThing:str) -> dict:
    select_query = "SELECT * FROM Emojis WHERE id_thing = ?;"
    cursor.execute(select_query, (idThing,))
    res = cursor.fetchone()
    return {
        "id":res[0],
        "nom_emoji":res[1],
        "id_thing":res[2]
    }
async def update_emoji():

    tous_infos = get_tous_infos()

    liste_serveur_emoji = [bot.get_guild(id_serv) for id_serv in liste_serveur_emoji_id]

    compteur = 0

    for i in range(0, len(liste_serveur_emoji)):
        serveur = liste_serveur_emoji[i]
        for j in range(50):
            if compteur >= len(tous_infos):
                break
            try:
                info = tous_infos[compteur]
                id_info = info["id"]
                name_info_for_emote = info["name"].replace("'","").replace(" ", "").replace(".","").replace("-","").replace("œ","oe").replace(",","")
                name_info_for_emote = unidecode(name_info_for_emote)

                emoji = await ajout_emote(serveur, name_info_for_emote, info["image"])
                
                insert_query = "INSERT INTO Emojis (id, nom_emoji, id_thing) VALUES(?, ?, ?)"
                cursor.execute(insert_query, (str(emoji.id), name_info_for_emote, str(id_info)))
                conn.commit()
                compteur += 1
                time.sleep(1.5)
            except:
                print("erreur")

def get_embed_indice(liste_lettre:list)->discord.Embed:
    embed = discord.Embed()
    mot = "`"
    for lettre in liste_lettre:
        mot+=lettre
    mot += "`"
    embed.description = ":bulb: **Indice** "+mot
    return embed


def get_joueur_by_id(idJoueur:str) -> dict:
    query = "SELECT * FROM Joueur WHERE id = ?;"
    cursor.execute(query, (idJoueur,))
    res = cursor.fetchone()
    if res:
        return {
            "id":res[0],
            "name":res[1],
            "avatar_url":res[2]
        }
    return None

def get_joueur_by_name(nomJoueur:str) -> dict:
    query = "SELECT * FROM Joueur WHERE name = ?;"
    cursor.execute(query, (nomJoueur,))
    res = cursor.fetchone()
    if res:
        return {
            "id":res[0],
            "name":res[1],
            "avatar_url":res[2]
        }
    return None

def insert_joueur_in_db(idJoueur:str, nomJoueur:str, avatarUrl:str):
    query = "INSERT INTO Joueur (id, name, avatar_url) VALUES (?, ?, ?);"
    cursor.execute(query, (idJoueur,nomJoueur,avatarUrl))
    conn.commit()



def update_jeu_gagnant(idGame:int, idGagnant:str):
    update_query = "UPDATE Jeu SET idGagnant = ? WHERE id = ?;"
    cursor.execute(update_query, (idGagnant, idGame))
    conn.commit()

async def timer_indice(interaction:discord.Interaction, channelId : str, guildId:str, mot:str):
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
            liste_pos_lettre.append(True)
            liste_lettre.append("_")
    
    
    
    message_indice = await interaction.channel.send(embed=get_embed_indice(liste_lettre))
    
    update_query = "UPDATE Jeu SET message_indice_id = ? WHERE channelId = ? AND guildId = ?;"
    cursor.execute(update_query, (str(message_indice.id),channelId, guildId))
    conn.commit()
    n = len(liste_lettre)
    if n < 5:
        secondint = 10
    if n >= 5 and n < 10:
        secondint = 25
    elif n >= 10 and n <15:
        secondint = 40
    elif n >= 15 and n <20:
        secondint = 55
    elif n >= 20 and n <25:
        secondint = 70
    elif n >= 25 and n <30:
        secondint = 85
    elif n >= 30 and n <35:
        secondint = 100
    elif n >= 35 and n <40:
        secondint = 115
    elif n >= 40 and n <45:
        secondint = 130
    elif n >= 45 and n <50:
        secondint = 145
    elif n >= 50 and n <55:
        secondint = 160
    else:
        secondint = 175
    while True:
        if secondint == 0:
            break
        try:
            secondint = secondint - 1
            if secondint % 5 == 0:
                for i in range(1):
                    pos = random.randint(0, n-1)
                    while not liste_pos_lettre[pos]:
                        pos = random.randint(0, n-1)
                    liste_lettre[pos] = mot[pos]
                    liste_pos_lettre[pos] = True
                await message_indice.edit(embed=get_embed_indice(liste_lettre))
        except:
            break
        await asyncio.sleep(1)

def create_embed_missing_joueur(nomJoueur:str) -> discord.Embed:
    embed = discord.Embed()
    embed.color = discord.Color.red()
    embed.description = nomJoueur+" n'a pas encore gagné de parties !"
    return embed
def create_embed_missing_item(nomItem:str) -> discord.Embed:
    embed = discord.Embed()
    embed.color = discord.Color.red()
    embed.description = "**"+nomItem+"** n'existe pas !"
    return embed

def compteur_victoire_un_joueur(liste_parties:list) -> dict:
    res = {
        "total" : 0,
        "champion" : {
            "total":0
        },
        "item": {
            "total":0
        }
    }
    for partie in liste_parties:
        if partie[5] not in res[partie[3]]:
            res[partie[3]][partie[5]] = {
                "total":1,
                partie[4]:1
            }
            res[partie[3]]["total"] +=1
            res["total"] +=1
        else:
            if partie[4] not in res[partie[3]][partie[5]]:
                res[partie[3]][partie[5]][partie[4]] = 1
                res[partie[3]]["total"] += 1
                res["total"] += 1
                if "total" not in res[partie[3]][partie[5]]:
                    res[partie[3]][partie[5]]["total"] = 1
                else:
                    res[partie[3]][partie[5]]["total"] += 1
            else:
                res[partie[3]][partie[5]][partie[4]] += 1
                res[partie[3]][partie[5]]["total"] += 1
                res[partie[3]]["total"] +=1
                res["total"] +=1
    trier_victoire(res)
    return res
def compteur_victoire_un_mode(liste_parties:list) -> dict:
    res = {
        "facile":False,
        "difficile":False,
        "joueurs":{}
    }
    dict_joueurs = {}
    for partie in liste_parties:
        if partie[7] not in dict_joueurs:
            dict_joueurs[partie[7]] = get_joueur_by_id(partie[7])
            dict_joueurs[partie[7]]
        if partie[5] == "difficile":
            res["difficile"] = True
        else:
            res["facile"] = True
    res["joueurs"] = dict_joueurs
    return res

def trier_victoire(dict_victoire:dict):
    if "facile" in dict_victoire["champion"]:
        dict_victoire["champion"]["facile"] = dict(sorted(dict_victoire["champion"]["facile"].items(), key=lambda item: item[1], reverse=True))
    if "difficile" in dict_victoire["champion"]:
        dict_victoire["champion"]["difficile"] = dict(sorted(dict_victoire["champion"]["difficile"].items(), key=lambda item: item[1], reverse=True))
    if "facile" in dict_victoire["item"]:
        dict_victoire["item"]["facile"] = dict(sorted(dict_victoire["item"]["facile"].items(), key=lambda item: item[1], reverse=True))
    if "difficile" in dict_victoire["item"]:
        dict_victoire["item"]["difficile"] = dict(sorted(dict_victoire["item"]["difficile"].items(), key=lambda item: item[1], reverse=True))


def has_accent(input_string):
    pattern = r'[À-ÖÙ-öÙ-ÿ]'
    return bool(re.search(pattern, input_string))

async def ajout_emote(guild:discord.Guild,name:str, url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                emoji_data = await resp.read()
                emoji = await guild.create_custom_emoji(name=name, image=emoji_data)
                return emoji
            else:
                return None

class RejouerBoutton(View):
    def __init__(self, mode:str, difficulte:str):
        super().__init__()
        self.mode = mode
        self.difficulte = difficulte

    @discord.ui.button(label="Rejouer", style=discord.ButtonStyle.green)
    async def rejouerBtn(self, interaction:discord.Interaction, button:Button):
        await interaction.response.defer()
    
        channelId = str(interaction.channel_id)
        guildId = str(interaction.guild_id)
        typeJeu = self.mode
        
        select_query = "SELECT * FROM Jeu WHERE channelId = ? AND guildId = ? AND idGagnant IS NULL;"
        cursor.execute(select_query, (channelId, guildId))
        res = cursor.fetchone()

        embed = discord.Embed()
        
        if res is None:
            embed.color = discord.Colour(0x425b8a)
            embed.set_footer(text="Version : "+versions[0])
            
            insert_query = "INSERT INTO Jeu (channelId, guildId, typeJeu, mot, difficulte) VALUES (?, ?, ?, ?, ?);"

            if self.difficulte == "facile":
                if typeJeu == "champion":
                    champion = get_random_champion()
                    mot = champion["name"]
                    cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, self.difficulte))
                    conn.commit()
                    embed.set_author(name="Qui est ce champion ?")
                    embed.set_image(url=champion["image"])
                elif typeJeu == "item":
                    item = get_random_item()
                    mot = item["name"]
                    cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, self.difficulte))
                    conn.commit()
                    embed.description = "*nom de l'item complet uniquement*"
                    embed.set_author(name="Quel est le nom de cet item ?")
                    embed.set_image(url=item["image"])
            else:
                if typeJeu == "champion":
                    champion = get_random_champion()
                    mot = champion["name"]
                    cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, self.difficulte))
                    conn.commit()
                    embed.add_field(name="Quel est le champion qui a ce titre ?", value="\u200b\n**"+champion["description"]+"**\n\u200b")
                elif typeJeu == "item":
                    item = get_random_item()
                    mot = item["name"]
                    cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, self.difficulte))
                    conn.commit()
                    embed.add_field(name="Quel est l'item qui correspond a cette description ?", value=item["description"])
                        
            await interaction.followup.send(embed=embed)
            
            await timer_indice(interaction=interaction, channelId=channelId, guildId=guildId, mot=mot)
        else:
            embed.description = "Une partie est déjà en cours..."
            await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    print('Le Bot '+bot.user.display_name+' Est Prêt !')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_disconnect():
    conn.close()
    print(f"Le bot {bot.user.name} s'est déconnecté.")

@bot.tree.command(name="play", description="Jouer au jeu")
@app_commands.describe(mode = "Item ou Champion ?")
@app_commands.choices(mode=[
    discord.app_commands.Choice(name="Item", value="item"),
    discord.app_commands.Choice(name="Champion", value="champion")
])
@app_commands.describe(difficulte = "Quelle difficulté ?")
@app_commands.choices(difficulte=[
    discord.app_commands.Choice(name="Facile", value="facile"),
    discord.app_commands.Choice(name="Difficile", value="difficile")
])
async def play(interaction: discord.Interaction, mode: discord.app_commands.Choice[str], difficulte: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    
    channelId = str(interaction.channel_id)
    guildId = str(interaction.guild_id)
    typeJeu = mode.value
    
    select_query = "SELECT * FROM Jeu WHERE channelId = ? AND guildId = ? AND idGagnant IS NULL;"
    cursor.execute(select_query, (channelId, guildId))
    res = cursor.fetchone()

    embed = discord.Embed()
    
    if res is None:
        embed.color = discord.Colour(0x425b8a)
        logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
        embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
        
        insert_query = "INSERT INTO Jeu (channelId, guildId, typeJeu, mot, difficulte) VALUES (?, ?, ?, ?, ?);"

        if difficulte.value == "facile":
            if typeJeu == "champion":
                champion = get_random_champion()
                mot = champion["name"]
                cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, difficulte.value))
                conn.commit()
                embed.set_author(name="Qui est ce champion ?")
                embed.set_image(url=champion["image"])
            elif typeJeu == "item":
                item = get_random_item()
                mot = item["name"].replace("œ","oe")
                cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, difficulte.value))
                conn.commit()
                embed.description = "*nom de l'item complet uniquement*"
                embed.set_author(name="Quel est le nom de cet item ?")
                embed.set_image(url=item["image"])
        else:
            if typeJeu == "champion":
                champion = get_random_champion()
                mot = champion["name"]
                cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, difficulte.value))
                conn.commit()
                embed.add_field(name="Quel est le champion qui a ce titre ?", value="\u200b\n**"+champion["description"]+"**\n\u200b")
            elif typeJeu == "item":
                item = get_random_item()
                mot = item["name"].replace("œ","oe")
                cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, difficulte.value))
                conn.commit()
                embed.add_field(name="Quel est l'item qui correspond a cette description ?", value=item["description"])
        await interaction.followup.send(embed=embed, file=logo_lol)
        
        await timer_indice(interaction=interaction, channelId=channelId, guildId=guildId, mot=mot)
        
        
        
    else:
        embed.description = "Une partie est déjà en cours..."
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="classement", description="Classement")
@app_commands.describe(joueur = "Nom du joueur")
@app_commands.describe(mode = "Mode de jeu")
@app_commands.choices(mode=[
    discord.app_commands.Choice(name="Item", value="item"),
    discord.app_commands.Choice(name="Champion", value="champion")
])
async def classement(interaction: discord.Interaction, joueur: str = None, mode: discord.app_commands.Choice[str] = None):
    await interaction.response.defer()
    dict_emojis = {}
    
    embed = discord.Embed()
    embed.color = discord.Colour(0x856d4d)
    logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
    embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
    if joueur and mode:
        joueur_info = get_joueur_by_name(joueur)
        if joueur_info:
            embed.set_thumbnail(url=joueur_info["avatar_url"])
            embed.description = "Victoires de **"+joueur+"** dans la catégorie *"+mode.value+"*"
            cursor.execute("SELECT * FROM Jeu WHERE idGagnant = ? AND typeJeu = ?;", (joueur_info["id"], mode.value))
            res = cursor.fetchall()
            compteurVictoire = compteur_victoire_un_joueur(res)[mode.value]
            if "facile" in compteurVictoire and "difficile" in compteurVictoire:
                msg_mode_facile = ""
                msg_mode_difficile = ""
                compteur = 0
                for champion_item in compteurVictoire["facile"]:
                    if compteur > 10:
                        break
                    if compteur != 0:
                        if champion_item not in dict_emojis:
                            if mode.value == "champion":
                                emoji = get_emoji(str(get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = get_emoji(str(get_item_id_by_name(champion_item)))
                            dict_emojis[champion_item] = emoji
                        msg_mode_facile += f"<:{dict_emojis[champion_item]['nom_emoji']}:{dict_emojis[champion_item]['id']}> {champion_item} : `{str(compteurVictoire['facile'][champion_item])}`\n"
                    compteur += 1
                compteur = 0
                for champion_item in compteurVictoire["difficile"]:
                    if compteur > 10:
                        break
                    if compteur != 0:
                        if champion_item not in dict_emojis:
                            if mode.value == "champion":
                                emoji = get_emoji(str(get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = get_emoji(str(get_item_id_by_name(champion_item)))
                            dict_emojis[champion_item] = emoji
                        msg_mode_difficile += f"<:{dict_emojis[champion_item]['nom_emoji']}:{dict_emojis[champion_item]['id']}> {champion_item} : `{str(compteurVictoire['difficile'][champion_item])}`\n"
                    compteur += 1
                embed.add_field(name="Mode Facile", value=msg_mode_facile)
                embed.add_field(name="Mode Difficile", value=msg_mode_difficile)
                if mode.value == "item":
                    embed.add_field(name="Totaux", value="Total : `"+str(compteurVictoire["total"])+"`\nFacile : `"+str(compteurVictoire["facile"]["total"])+"`\nDifficile : `"+str(compteurVictoire["difficile"]["total"])+"`", inline=False)
                else:
                    embed.add_field(name="Totaux", value="Total : `"+str(compteurVictoire["total"])+"`\nFacile : `"+str(compteurVictoire["facile"]["total"])+"`\nDifficile : `"+str(compteurVictoire["difficile"]["total"])+"`")
            elif "facile" in compteurVictoire:
                msg_mode_facile = ""
                compteur = 0
                for champion_item in compteurVictoire["facile"]:
                    if compteur > 10:
                        break
                    if compteur != 0:
                        if champion_item not in dict_emojis:
                            if mode.value == "champion":
                                emoji = get_emoji(str(get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = get_emoji(str(get_item_id_by_name(champion_item)))
                            dict_emojis[champion_item] = emoji
                        msg_mode_facile += f"<:{dict_emojis[champion_item]['nom_emoji']}:{dict_emojis[champion_item]['id']}> {champion_item} : `{str(compteurVictoire['facile'][champion_item])}`\n"
                    compteur += 1
                embed.add_field(name="Mode Facile", value=msg_mode_facile)
                if mode.value == "item":
                    embed.add_field(name="Totaux", value="Total : `"+str(compteurVictoire["total"])+"`\nFacile : `"+str(compteurVictoire["facile"]["total"])+"`", inline=False)
                else:
                    embed.add_field(name="Totaux", value="Total : `"+str(compteurVictoire["total"])+"`\nFacile : `"+str(compteurVictoire["facile"]["total"])+"`")
            elif "difficile" in compteurVictoire:
                msg_mode_difficile = ""
                compteur = 0
                for champion_item in compteurVictoire["difficile"]:
                    if compteur > 10:
                        break
                    if compteur != 0:
                        if champion_item not in dict_emojis:
                            if mode.value == "champion":
                                emoji = get_emoji(str(get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = get_emoji(str(get_item_id_by_name(champion_item)))
                            dict_emojis[champion_item] = emoji
                        msg_mode_difficile += f"<:{dict_emojis[champion_item]['nom_emoji']}:{dict_emojis[champion_item]['id']}> {champion_item} : `{str(compteurVictoire['difficile'][champion_item])}`\n"
                    compteur += 1
                embed.add_field(name="Mode Difficile", value=msg_mode_difficile)
                if mode.value == "item":
                    embed.add_field(name="Totaux", value="Total : `"+str(compteurVictoire["total"])+"`\nDifficile : `"+str(compteurVictoire["difficile"]["total"])+"`",inline=False)
                else:
                    embed.add_field(name="Totaux", value="Total : `"+str(compteurVictoire["total"])+"`\nDifficile : `"+str(compteurVictoire["difficile"]["total"])+"`")
            else:
                embed.add_field(name="Totaux", value="Total : `0`")
        else:
            embed = create_embed_missing_joueur(joueur)
            await interaction.followup.send(embed=embed)
            return
    elif joueur:
        joueur_info = get_joueur_by_name(joueur)
        if joueur_info:
            embed.description = "Victoires de **"+joueur+"** dans les catégories *champion* et *item*"
            embed.set_thumbnail(url=joueur_info["avatar_url"])
            cursor.execute("SELECT * FROM Jeu WHERE idGagnant = ?;", (joueur_info["id"],))
            res = cursor.fetchall()
            compteurVictoire = compteur_victoire_un_joueur(res)
            if compteurVictoire["champion"]["total"] != 0:
                msg_champ_totaux = "Totaux : `" + str(compteurVictoire["champion"]["total"]) + "`\n"
                if "facile" in compteurVictoire["champion"]:
                    msg_champ_totaux += "Facile : `"+str(compteurVictoire['champion']['facile']['total'])+"`\n"
                    msg_champ_facile = ""
                    compteur = 0
                    for champion in compteurVictoire["champion"]["facile"]:
                        if compteur > 5:
                            break
                        if compteur != 0:
                            if champion not in dict_emojis:
                                emoji = get_emoji(str(get_champion_id_by_name(champion)))
                                dict_emojis[champion] = emoji
                            msg_champ_facile += f"<:{dict_emojis[champion]['nom_emoji']}:{dict_emojis[champion]['id']}> {champion} : `{str(compteurVictoire['champion']['facile'][champion])}`\n"
                        compteur += 1
                else:
                    msg_champ_facile = "`0`"
                    msg_champ_totaux += "Facile : `0`\n"
                if "difficile" in compteurVictoire["champion"]:
                    msg_champ_totaux += "Difficile : `"+str(compteurVictoire['champion']['difficile']['total'])+"`\n"
                    msg_champ_difficile = ""
                    compteur = 0
                    for champion in compteurVictoire["champion"]["difficile"]:
                        if compteur > 5:
                            break
                        if compteur != 0:
                            if champion not in dict_emojis:
                                emoji = get_emoji(str(get_champion_id_by_name(champion)))
                                dict_emojis[champion] = emoji
                            msg_champ_difficile += f"<:{dict_emojis[champion]['nom_emoji']}:{dict_emojis[champion]['id']}> {champion} : `{str(compteurVictoire['champion']['difficile'][champion])}`\n"
                        compteur += 1
                else:
                    msg_champ_difficile = "`0`"
                    msg_champ_totaux += "Difficile : `0`\n"
            else:
                msg_champ_facile = "`0`"
                msg_champ_difficile = "`0`"
                msg_champ_totaux = "`0`"
            embed.add_field(name="Champion\nFacile", value=msg_champ_facile)
            embed.add_field(name="\u200b\nDifficile", value=msg_champ_difficile)
            embed.add_field(name="\u200b\nTotaux", value=msg_champ_totaux)
            if compteurVictoire["item"]["total"] != 0:
                msg_item_totaux = "Totaux : `" + str(compteurVictoire["item"]["total"]) + "`\n"
                if "facile" in compteurVictoire["item"]:
                    msg_item_totaux += "Facile : `"+str(compteurVictoire['item']['facile']['total'])+"`\n"
                    msg_item_facile = ""
                    compteur = 0
                    for item in compteurVictoire["item"]["facile"]:
                        if compteur > 5:
                            break
                        if compteur != 0:
                            if item not in dict_emojis:
                                emoji = get_emoji(str(get_item_id_by_name(item)))
                                dict_emojis[item] = emoji
                            msg_item_facile += f"<:{dict_emojis[item]['nom_emoji']}:{dict_emojis[item]['id']}> {item} : `{str(compteurVictoire['item']['facile'][item])}`\n"
                        compteur += 1
                else:
                    msg_item_facile = "`0`"
                    msg_item_totaux += "Facile : `0`\n"
                if "difficile" in compteurVictoire["item"]:
                    msg_item_totaux += "Difficile : `"+str(compteurVictoire['item']['difficile']['total'])+"`\n"
                    msg_item_difficile = ""
                    compteur = 0
                    for item in compteurVictoire["item"]["difficile"]:
                        if compteur > 5:
                            break
                        if compteur != 0:
                            if item not in dict_emojis:
                                emoji = get_emoji(str(get_item_id_by_name(item)))
                                dict_emojis[item] = emoji
                            msg_item_difficile += f"<:{dict_emojis[item]['nom_emoji']}:{dict_emojis[item]['id']}> {item} : `{str(compteurVictoire['item']['difficile'][item])}`\n"
                        compteur += 1
                else:
                    msg_item_difficile = "`0`"
                    msg_item_totaux += "Difficile : `0`\n"
            else:
                msg_item_facile = "`0`"
                msg_item_difficile = "`0`"
                msg_item_totaux = "`0`"
            embed.add_field(name="Item\nFacile", value=msg_item_facile)
            embed.add_field(name="\u200b\nDifficile", value=msg_item_difficile)
            embed.add_field(name="\u200b\nTotaux", value=msg_item_totaux)
        else:
            embed = create_embed_missing_joueur(joueur)
            await interaction.followup.send(embed=embed)
            return
    elif mode:
        embed.description = "Victoires dans les catégories *"+mode.value+"*"

        cursor.execute("SELECT * FROM Jeu WHERE typeJeu = ? AND idGagnant IS NOT NULL;", (mode.value,))
        compteurVictoire = compteur_victoire_un_mode(cursor.fetchall())

        cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
        classement_total_joueurs = cursor.fetchall()

        dict_joueurs = compteurVictoire["joueurs"]
        if compteurVictoire["facile"] and compteurVictoire["difficile"]:
            cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'facile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_facile_joueurs = cursor.fetchall()
            cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'difficile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_difficile_joueurs = cursor.fetchall()
            ##
            compteur = 1
            msg_classement_total = ""
            for joueur_classe in classement_total_joueurs:
                if compteur == 1:
                    embed.set_thumbnail(url=dict_joueurs[joueur_classe[0]]["avatar_url"])
                if compteur >= 10:
                    break
                nom_joueur = dict_joueurs[joueur_classe[0]]["name"]

                msg_classement_total += str(compteur)+"/ **"+nom_joueur+"** `"+str(joueur_classe[1])+"`\n"
                compteur += 1
            embed.add_field(name="Classement Total", value=msg_classement_total)
            ##
            compteur = 1
            msg_classement_facile = ""
            for joueur_classe in classement_facile_joueurs:
                if compteur >= 10:
                    break
                nom_joueur = dict_joueurs[joueur_classe[0]]["name"]

                msg_classement_facile += str(compteur)+"/ **"+nom_joueur+"** `"+str(joueur_classe[1])+"`\n"
                compteur += 1
            embed.add_field(name="Classement Facile", value=msg_classement_facile)
            ##
            compteur = 1
            msg_classement_difficile = ""
            for joueur_classe in classement_difficile_joueurs:
                if compteur >= 10:
                    break
                nom_joueur = dict_joueurs[joueur_classe[0]]["name"]
                
                msg_classement_difficile += str(compteur)+"/ **"+nom_joueur+"** `"+str(joueur_classe[1])+"`\n"
                compteur += 1
            embed.add_field(name="Classement Difficile", value=msg_classement_difficile)
        elif "facile" in compteurVictoire["parties"]:
            parties_facile = compteurVictoire["parties"]["facile"]
            cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'facile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_facile_joueurs = cursor.fetchall()
        elif "difficile" in compteurVictoire["parties"]:
            parties_difficile = compteurVictoire["parties"]["difficile"]
            
            cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'difficile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_difficile_joueurs = cursor.fetchall()
        else:
            embed.add_field(name="Totaux", value="`0`")
     
    else:
        # cursor.execute("SELECT * FROM Jeu WHERE idGagnant IS NOT NULL;")
        # res = cursor.fetchall()
        # for partie in res:
        #     print(partie)
        embed.add_field(name="en cours...", value="en cours...")
          
    await interaction.followup.send(embed=embed, file=logo_lol, ephemeral=True)

# @bot.tree.command(name="updateemote", description="updateemote")
# async def updateemote(interaction: discord.Interaction):
#     await interaction.response.defer()
#     update_emoji2()
#     await interaction.followup.send("fini")

@bot.tree.command(name="items", description="Affiche tous les items, si un item est séléctionné alors on affiche les stats")
@app_commands.describe(item = "Nom de l'item")
async def items(interaction: discord.Interaction, item: str = None):
    await interaction.response.defer()
    embed = discord.Embed()
    if item:
        item_info = get_item_by_name(item)
        if item_info:
            embed.set_thumbnail(url=item_info["image"])
            embed.set_author(name=item)
            embed.add_field(name="Description/Stats", value=item_info["description"],inline=False)
        else:
            embed = create_embed_missing_item(item)
        await interaction.followup.send(embed=embed)
            
    else:
        liste_embeds = []
        items_info = get_all_items_in_list()
        msg = ""
        lettre = "A"
        nb_lettres = 0
        nb_lettres_embed = 0

        
        for item_info in items_info:
            if unidecode(item_info["name"][0]).lower() != unidecode(lettre).lower():
                if msg != "" and msg != "\n":
                    embed.add_field(name=lettre, value=msg)
                
                msg = ""
                lettre = item_info["name"][0]
                nb_lettres = 0
            emoji = get_emoji(str(item_info["id"]))
            tmp = f"<:{emoji['nom_emoji']}:{emoji['id']}> {item_info['name']}\n"
            msg += tmp
            nb_lettres += len(tmp)
            nb_lettres_embed += len(tmp)

            if nb_lettres_embed >= 5900:
                nb_lettres_embed = nb_lettres
                liste_embeds.append(embed)
                embed = discord.Embed()
            if nb_lettres >= 950:
                nb_lettres = 0
                if nb_lettres_embed >= 5900:
                    nb_lettres_embed = 0
                    liste_embeds.append(embed)
                    embed = discord.Embed()
                
                embed.add_field(name=lettre, value=msg)
                msg = ""
            
        if msg != "":
            embed.add_field(name=lettre, value=msg)
        if embed not in liste_embeds:
            liste_embeds.append(embed)
            
        for i in range(len(liste_embeds)):
            if i == 0:
                await interaction.followup.send(embed=liste_embeds[i])
            else:
                await interaction.channel.send(embed=liste_embeds[i])

@bot.tree.command(name="champions", description="Affiche tous les champions, si un item est séléctionné alors on affiche ")
@app_commands.describe(champion = "Nom de l'item")
async def champions(interaction: discord.Interaction, champion: str = None):
    await interaction.response.defer()
    await interaction.followup.send("test")

@bot.event
async def on_message(message: discord.Message):
    if not message.author.bot:
        channelId = str(message.channel.id)
        guildId = str(message.guild.id)
        select_query = "SELECT * FROM Jeu WHERE channelId = ? AND guildId = ? AND idGagnant IS NULL;"
        cursor.execute(select_query, (channelId, guildId))
        res = cursor.fetchone()
        if res is not None:
            if(res[3] == "champion"):
                request = message.content.lower()
                if request == "!stop":
                    message_indice = await message.channel.fetch_message(int(res[6]))
                    await message_indice.delete()
                    cursor.execute("DELETE FROM Jeu WHERE id = ?;", (res[0],))
                    conn.commit()
                    embed = discord.Embed()
                    embed.set_author(name="Fin de partie")
                    embed.set_image(url=get_champion_splash_by_name(res[4]))
                    embed.description = "Le champion était : "+res[4]
                    await message.channel.send(embed=embed)
                else:
                    liste_possibilite = []
                    nomChampion = res[4].lower()
                    accent = has_accent(nomChampion)
                    liste_possibilite.append(nomChampion)
                    if accent:
                        liste_possibilite.append(unidecode(nomChampion))
                    if "'" in nomChampion:
                        if accent:
                            liste_possibilite.append(unidecode(nomChampion.replace("'", "")))
                            liste_possibilite.append(unidecode(nomChampion.replace("'", " ")))
                        liste_possibilite.append(nomChampion.replace("'", ""))
                        liste_possibilite.append(nomChampion.replace("'", " "))
                    if "." in nomChampion:
                        if accent:
                            liste_possibilite.append(unidecode(nomChampion.replace(".", "")))
                        liste_possibilite.append(nomChampion.replace(".", ""))
                    if " " in nomChampion:
                        if accent:
                            liste_possibilite.append(unidecode(nomChampion.replace(" ", "")))
                        liste_possibilite.append(nomChampion.replace(" ", ""))
                    if "." in nomChampion and " " in nomChampion:
                        if accent:
                            liste_possibilite.append(unidecode(nomChampion.replace(".", "").replace(" ", "")))
                        liste_possibilite.append(nomChampion.replace(".", "").replace(" ", ""))
                    if " " in nomChampion and "'" in nomChampion:
                        if accent:
                            liste_possibilite.append(unidecode(nomChampion.replace("'", " ").replace(" ", "")))
                            liste_possibilite.append(unidecode(nomChampion.replace("'", "").replace(" ", "")))
                        liste_possibilite.append(nomChampion.replace("'", " ").replace(" ", ""))
                        liste_possibilite.append(nomChampion.replace("'", "").replace(" ", ""))
                    if " " in nomChampion and "." in nomChampion and "'" in nomChampion:
                        if accent:
                            liste_possibilite.append(unidecode(nomChampion.replace(" ", "").replace(".", "").replace("'", "")))
                            liste_possibilite.append(unidecode(nomChampion.replace(" ", "").replace(".", "").replace("'", " ")))
                        liste_possibilite.append(nomChampion.replace(" ", "").replace(".", "").replace("'", ""))
                        liste_possibilite.append(nomChampion.replace(" ", "").replace(".", "").replace("'", " "))
                    if request in liste_possibilite:
                        embed = discord.Embed()
                        message_indice = await message.channel.fetch_message(int(res[6]))
                        await message_indice.delete()

                        message_possibilite = ""
                        for possibilite in liste_possibilite:
                            message_possibilite += "• "+possibilite+"\n"
                        embed.color = discord.Colour.green()
                        embed.set_author(name=message.author.name+" a gagné !")
                        embed.set_thumbnail(url=message.author.display_avatar.url)
                        embed.add_field(name="Réponse", value="**"+res[4]+"**", inline=True)
                        embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                        embed.set_image(url=get_champion_splash_by_name(res[4]))
                        if not get_joueur_by_id(str(message.author.id)):
                            insert_joueur_in_db(str(message.author.id), message.author.name, message.author.display_avatar.url)
                        update_jeu_gagnant(res[0], str(message.author.id))
                        await message.channel.send(embed=embed, view=RejouerBoutton(res[3], res[5]))
            elif(res[3] == "item"):
                request = message.content.lower().replace("œ","oe")
                if request == "!stop":
                    message_indice = await message.channel.fetch_message(int(res[6]))
                    await message_indice.delete()
                    cursor.execute("DELETE FROM Jeu WHERE id = ?;", (res[0],))
                    conn.commit()
                    embed = discord.Embed()
                    embed.set_author(name="Fin de partie")
                    embed.set_image(url=get_item_image_by_name(res[4]))
                    embed.description = "L'item était : "+res[4]
                    await message.channel.send(embed=embed)
                else:
                    liste_possibilite = []
                    nomItem = res[4].lower()
                    liste_possibilite.append(nomItem)
                    accent = has_accent(nomItem)
                    if accent:
                        liste_possibilite.append(unidecode(nomItem))
                    if "-" in nomItem:
                        liste_possibilite.append(nomItem.replace("-", " "))
                        if accent:
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ")))
                    if "'" in nomItem:
                        liste_possibilite.append(nomItem.replace("'", ""))
                        liste_possibilite.append(nomItem.replace("'", " "))
                        if accent:
                            liste_possibilite.append(unidecode(nomItem.replace("'", "")))
                            liste_possibilite.append(unidecode(nomItem.replace("'", " ")))
                    if "." in nomItem:
                        liste_possibilite.append(nomItem.replace(".", ""))
                        if accent:
                            liste_possibilite.append(unidecode(nomItem.replace(".", "")))
                    if "." in nomItem and "'" in nomItem:
                        if accent:
                            liste_possibilite.append(unidecode(nomItem.replace(".", "").replace("'", "")))
                            liste_possibilite.append(unidecode(nomItem.replace(".", "").replace("'", " ")))
                        liste_possibilite.append(nomItem.replace(".", "").replace("'", ""))
                        liste_possibilite.append(nomItem.replace(".", "").replace("'", " "))
                    if "-" in nomItem and "." in nomItem:
                        if accent:
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace(".", "")))
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace(".", " ")))
                        liste_possibilite.append(nomItem.replace("-", " ").replace(".", ""))
                        liste_possibilite.append(nomItem.replace("-", " ").replace(".", " "))
                    if "-" in nomItem and "'" in nomItem:
                        if accent:
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace("'", "")))
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace("'", " ")))
                        liste_possibilite.append(nomItem.replace("-", " ").replace("'", ""))
                        liste_possibilite.append(nomItem.replace("-", " ").replace("'", " "))
                    if "-" in nomItem and "'" in nomItem and "." in nomItem:
                        if accent:
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace("'", "").replace(".", " ")))
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace("'", " ").replace(".", " ")))
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace("'", "").replace(".", "")))
                            liste_possibilite.append(unidecode(nomItem.replace("-", " ").replace("'", " ").replace(".", "")))
                        liste_possibilite.append(nomItem.replace("-", " ").replace("'", "").replace(".", " "))
                        liste_possibilite.append(nomItem.replace("-", " ").replace("'", " ").replace(".", " "))
                        liste_possibilite.append(nomItem.replace("-", " ").replace("'", "").replace(".", ""))
                        liste_possibilite.append(nomItem.replace("-", " ").replace("'", " ").replace(".", ""))
                    if request in liste_possibilite:
                        embed = discord.Embed()
                        message_indice = await message.channel.fetch_message(int(res[6]))
                        await message_indice.delete()
                        message_possibilite = ""
                        for possibilite in liste_possibilite:
                            message_possibilite += "• "+possibilite+"\n"
                        embed.color = discord.Colour.green()
                        embed.set_author(name=message.author.name+" a gagné !")
                        embed.set_thumbnail(url=message.author.display_avatar.url)
                        embed.add_field(name="Réponse", value="**"+res[4]+"**", inline=True)
                        embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                        embed.set_image(url=get_item_image_by_name(res[4]))
                        if not get_joueur_by_id(str(message.author.id)):
                            insert_joueur_in_db(str(message.author.id), message.author.name, message.author.display_avatar.url)
                        update_jeu_gagnant(res[0], str(message.author.id))
                        await message.channel.send(embed=embed, view=RejouerBoutton(res[3], res[5]))

bot.run("MTE1OTA0NTA5MDUzMTA5MDUxNA.G_UKht.r5v82l70L_rKUrJ4iX0PXOeV5Dwh6ov0s648hI")