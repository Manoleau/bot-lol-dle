import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from discord import app_commands
import requests
import asyncio
import random



import re

import sqlite3
conn = sqlite3.connect('DB/LeagueDle.db')
cursor = conn.cursor()
# bs4
# lxml

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()

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

select_query = "SELECT * FROM versions WHERE version = ?;"
cursor.execute(select_query, (versions[0],))
res = cursor.fetchone()[0]
if not res:
    ## vide les table
    league = League()
    delete_query = "DELETE FROM items"
    cursor.execute(delete_query)
    delete_query = "DELETE FROM champions"
    cursor.execute(delete_query)

    conn.commit()

    for champion in league.champions:
        insert_query = "INSERT INTO champions (id, name, image, title, splash_art) VALUES (?, ?, ?, ?, ?);"
        cursor.execute(insert_query, (league.champions[champion].id, league.champions[champion].name, league.champions[champion].image, league.champions[champion].title, league.champions[champion].splash_art))
    for item in league.items:
        insert_query = "INSERT INTO items (id, name, image, description) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, (league.items[item].id, league.items[item].name, league.items[item].image, league.items[item].description))

    conn.commit()


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


def get_item_image_by_id(idItem:int) -> str:
    select_query = "SELECT image FROM items WHERE id = ?;"
    cursor.execute(select_query, (idItem,))
    res = cursor.fetchone()[0]
    
    return res

def get_item_image_by_name(nameItem:str) -> str:
    select_query = "SELECT image FROM items WHERE name = ?;"
    cursor.execute(select_query, (nameItem,))
    res = cursor.fetchone()[0]
    
    return res

def get_item_id_by_name(nameItem:str) -> int:
    select_query = "SELECT id FROM items WHERE name = ?;"
    cursor.execute(select_query, (nameItem,))
    res = cursor.fetchone()[0]
    
    return res

def get_item_name_by_id(idItem:int) -> str:
    select_query = "SELECT name FROM items WHERE id = ?;"
    cursor.execute(select_query, (idItem,))
    res = cursor.fetchone()[0]
    
    return res


def get_random_champion() -> dict:
    cursor.execute("SELECT * FROM champions ORDER BY RANDOM() LIMIT 1;")
    res = cursor.fetchone()
    return {
        "id":res[0],
        "name":res[1],
        "image":res[2],
        "description": res[3]
    }

def get_random_item() -> dict:
    cursor.execute("SELECT * FROM items WHERE description != '' ORDER BY RANDOM() LIMIT 1;")
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
            "description": champion[3]
        }
        for champion in champions
    ]

def get_embed_indice(liste_lettre:list)->discord.Embed:
    embed = discord.Embed()
    mot = "`"
    for lettre in liste_lettre:
        mot+=lettre
    mot += "`"
    embed.description = ":bulb: **Indice** "+mot
    return embed


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
        
        select_query = "SELECT * FROM Jeu WHERE channelId = ? AND guildId = ? AND nomGagnant IS NULL;"
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
            
            liste_lettre = []
            liste_pos_lettre = []

            for lettre in mot:
                if lettre == " ":
                    liste_pos_lettre.append(False)
                    liste_lettre.append(" ")
                elif lettre == "-":
                    liste_pos_lettre.append(True)
                    liste_lettre.append("-")
                else:
                    liste_pos_lettre.append(True)
                    liste_lettre.append("_")
            
            await interaction.followup.send(embed=embed)
            
            message_indice = await interaction.channel.send(embed=get_embed_indice(liste_lettre))
            
            update_query = "UPDATE Jeu SET message_indice_id = ? WHERE channelId = ? AND guildId = ?;"
            cursor.execute(update_query, (str(message_indice.id),channelId, guildId))
            conn.commit()
            n = len(liste_lettre)
            if n < 5:
                secondint = 10
            if n >= 5 and n < 10:
                secondint = 20
            elif n >= 10 and n <15:
                secondint = 30
            elif n >= 15 and n <20:
                secondint = 40
            elif n >= 20 and n <25:
                secondint = 50
            elif n >= 25 and n <30:
                secondint = 50
            elif n >= 30 and n <35:
                secondint = 60
            elif n >= 35 and n <40:
                secondint = 70
            elif n >= 40 and n <45:
                secondint = 80
            elif n >= 45 and n <50:
                secondint = 90
            elif n >= 50 and n <55:
                secondint = 100
            else:
                secondint = 110
            while True:
                if secondint == 0:
                    break
                try:
                    secondint = secondint - 1
                    if secondint % 10 == 0:
                        for i in range(2):
                            pos = random.randint(0, n-1)
                            while not liste_pos_lettre[pos]:
                                pos = random.randint(0, n-1)
                            liste_lettre[pos] = mot[pos]
                            liste_pos_lettre[pos] = True
                        await message_indice.edit(embed=get_embed_indice(liste_lettre))
                except:
                    break
                await asyncio.sleep(1)
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
    
    select_query = "SELECT * FROM Jeu WHERE channelId = ? AND guildId = ? AND nomGagnant IS NULL;"
    cursor.execute(select_query, (channelId, guildId))
    res = cursor.fetchone()

    embed = discord.Embed()
    
    if res is None:
        embed.color = discord.Colour(0x425b8a)
        embed.set_footer(text="Version : "+versions[0])
        
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
                mot = item["name"]
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
                mot = item["name"]
                cursor.execute(insert_query, (channelId, guildId, typeJeu, mot, difficulte.value))
                conn.commit()
                embed.add_field(name="Quel est l'item qui correspond a cette description ?", value=item["description"])
        liste_lettre = []
        liste_pos_lettre = []

        for lettre in mot:
            if lettre == " ":
                liste_pos_lettre.append(False)
                liste_lettre.append(" ")
            elif lettre == "-":
                liste_pos_lettre.append(True)
                liste_lettre.append("-")
            else:
                liste_pos_lettre.append(True)
                liste_lettre.append("_")
        
        await interaction.followup.send(embed=embed)
        
        message_indice = await interaction.channel.send(embed=get_embed_indice(liste_lettre))
        
        update_query = "UPDATE Jeu SET message_indice_id = ? WHERE channelId = ? AND guildId = ?;"
        cursor.execute(update_query, (str(message_indice.id),channelId, guildId))
        conn.commit()
        n = len(liste_lettre)
        if n < 5:
            secondint = 10
        if n >= 5 and n < 10:
            secondint = 20
        elif n >= 10 and n <15:
            secondint = 30
        elif n >= 15 and n <20:
            secondint = 40
        elif n >= 20 and n <25:
            secondint = 50
        elif n >= 25 and n <30:
            secondint = 50
        elif n >= 30 and n <35:
            secondint = 60
        elif n >= 35 and n <40:
            secondint = 70
        elif n >= 40 and n <45:
            secondint = 80
        elif n >= 45 and n <50:
            secondint = 90
        elif n >= 50 and n <55:
            secondint = 100
        else:
            secondint = 110
        while True:
            if secondint == 0:
                break
            try:
                secondint = secondint - 1
                if secondint % 10 == 0:
                    for i in range(2):
                        pos = random.randint(0, n-1)
                        while not liste_pos_lettre[pos]:
                            pos = random.randint(0, n-1)
                        liste_lettre[pos] = mot[pos]
                        liste_pos_lettre[pos] = True
                    await message_indice.edit(embed=get_embed_indice(liste_lettre))
            except:
                break
            await asyncio.sleep(1)
        
    else:
        embed.description = "Une partie est déjà en cours..."
        await interaction.followup.send(embed=embed)

@bot.event
async def on_message(message: discord.Message):
    if not message.author.bot:
        channelId = str(message.channel.id)
        guildId = str(message.guild.id)
        select_query = "SELECT * FROM Jeu WHERE channelId = ? AND guildId = ? AND nomGagnant IS NULL;"
        cursor.execute(select_query, (channelId, guildId))
        res = cursor.fetchone()
        if res is not None:
            if(res[4] == "champion"):
                request = message.content.lower()
                if request == "!stop":
                    ""
                else:
                    liste_possibilite = []
                    nomChampion = res[5].lower()
                    print(nomChampion+" : "+request)
                    liste_possibilite.append(nomChampion)
                    if "'" in nomChampion:
                        liste_possibilite.append(nomChampion.replace("'", ""))
                        liste_possibilite.append(nomChampion.replace("'", " "))
                    if "." in nomChampion:
                        liste_possibilite.append(nomChampion.replace(".", ""))
                    if " " in nomChampion:
                        liste_possibilite.append(nomChampion.replace(" ", ""))
                    if "." in nomChampion and " " in nomChampion:
                        liste_possibilite.append(nomChampion.replace(".", "").replace(" ", ""))
                    if " " in nomChampion and "'" in nomChampion:
                        liste_possibilite.append(nomChampion.replace("'", " ").replace(" ", ""))
                        liste_possibilite.append(nomChampion.replace("'", "").replace(" ", ""))
                    if " " in nomChampion and "." in nomChampion and "'" in nomChampion:
                        liste_possibilite.append(nomChampion.replace(" ", "").replace(".", "").replace("'", ""))
                        liste_possibilite.append(nomChampion.replace(" ", "").replace(".", "").replace("'", " "))
                    
                    if request in liste_possibilite:
                        embed = discord.Embed()
                        message_indice = await message.channel.fetch_message(int(res[7]))
                        await message_indice.delete()

                        message_possibilite = ""
                        for possibilite in liste_possibilite:
                            message_possibilite += "• "+possibilite+"\n"
                        embed.color = discord.Colour.green()
                        embed.set_author(name=message.author.display_name+" a gagné !")
                        embed.set_thumbnail(url=message.author.display_avatar.url)
                        embed.add_field(name="Réponse", value="**"+res[5]+"**", inline=True)
                        embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                        embed.set_image(url=get_champion_splash_by_name(res[5]))
                        update_query = "UPDATE Jeu SET nomGagnant = ? WHERE id = ?;"
                        cursor.execute(update_query, (message.author.display_name, res[0]))
                        conn.commit()
                        await message.channel.send(embed=embed, view=RejouerBoutton(res[4], res[6]))
            elif(res[4] == "item"):
                request = message.content.lower()
                if request == "!stop":
                    ""
                else:
                    liste_possibilite = []
                    nomItem = res[5].lower()
                    print(nomItem+" : "+request)
                    liste_possibilite.append(nomItem)
                    if "'" in nomItem:
                        liste_possibilite.append(nomItem.replace("'", ""))
                        liste_possibilite.append(nomItem.replace("'", " "))
                    if "." in nomItem:
                        liste_possibilite.append(nomItem.replace(".", ""))
                    if "." in nomItem and "'" in nomItem:
                        liste_possibilite.append(nomItem.replace(".", "").replace("'", ""))
                        liste_possibilite.append(nomItem.replace(".", "").replace("'", " "))
                    
                    if request in liste_possibilite:
                        embed = discord.Embed()
                        message_indice = await message.channel.fetch_message(int(res[7]))
                        await message_indice.delete()
                        message_possibilite = ""
                        for possibilite in liste_possibilite:
                            message_possibilite += "• "+possibilite+"\n"
                        embed.color = discord.Colour.green()
                        embed.set_author(name=message.author.display_name+" a gagné !")
                        embed.set_thumbnail(url=message.author.display_avatar.url)
                        embed.add_field(name="Réponse", value="**"+res[5]+"**", inline=True)
                        embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                        embed.set_image(url=get_item_image_by_name(res[5]))
                        update_query = "UPDATE Jeu SET nomGagnant = ? WHERE id = ?;"
                        cursor.execute(update_query, (message.author.display_name, res[0]))
                        conn.commit()
                        await message.channel.send(embed=embed, view=RejouerBoutton(res[4], res[6]))



bot.run("MTE1OTA0NTA5MDUzMTA5MDUxNA.G_UKht.r5v82l70L_rKUrJ4iX0PXOeV5Dwh6ov0s648hI")
