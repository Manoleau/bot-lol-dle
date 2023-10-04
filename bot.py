import discord
from discord.ext import commands
from discord import app_commands
import requests

import sqlite3


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

class Champion:
    def __init__(self, info_champion: dict) -> None:
        ""
        self.name = info_champion["name"]
        self.id = info_champion["key"]
        self.image = f"https://ddragon.leagueoflegends.com/cdn/{info_champion['version']}/img/champion/{info_champion['image']['full']}"

conn = sqlite3.connect('DB/LeagueDle.db')
cursor = conn.cursor()
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

    insert_query = "INSERT INTO versions (version) VALUES (?)"
    cursor.execute(insert_query, (versions[0],))

    for champion in league.champions:
        insert_query = "INSERT INTO champions (id, name, image) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (league.champions[champion].id, league.champions[champion].name, league.champions[champion].image))
    for item in league.items:
        insert_query = "INSERT INTO items (id, name, image) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (league.items[item].id, league.items[item].name, league.items[item].image))
    conn.commit()

conn.close()


def get_champion_image_by_id(idChampion:int) -> str:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT image FROM champions WHERE id = ?;"
    cursor.execute(select_query, (idChampion,))
    res = cursor.fetchone()[0]
    conn.close()
    return res

def get_champion_image_by_name(nameChampion:str) -> str:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT image FROM champions WHERE name = ?;"
    cursor.execute(select_query, (nameChampion,))
    res = cursor.fetchone()[0]
    conn.close()
    return res

def get_champion_id_by_name(nameChampion:str) -> int:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT id FROM champions WHERE name = ?;"
    cursor.execute(select_query, (nameChampion,))
    res = cursor.fetchone()[0]
    conn.close()
    return res

def get_champion_name_by_id(idChampion:int) -> str:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT name FROM champions WHERE id = ?;"
    cursor.execute(select_query, (idChampion,))
    res = cursor.fetchone()[0]
    conn.close()
    return res


def get_item_image_by_id(idItem:int) -> str:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT image FROM items WHERE id = ?;"
    cursor.execute(select_query, (idItem,))
    res = cursor.fetchone()[0]
    conn.close()
    return res

def get_item_image_by_name(nameItem:str) -> str:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT image FROM items WHERE name = ?;"
    cursor.execute(select_query, (nameItem,))
    res = cursor.fetchone()[0]
    conn.close()
    return res

def get_item_id_by_name(nameItem:str) -> int:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT id FROM items WHERE name = ?;"
    cursor.execute(select_query, (nameItem,))
    res = cursor.fetchone()[0]
    conn.close()
    return res

def get_item_name_by_id(idItem:int) -> str:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    select_query = "SELECT name FROM items WHERE id = ?;"
    cursor.execute(select_query, (idItem,))
    res = cursor.fetchone()[0]
    conn.close()
    return res


def get_random_champion() -> dict:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM champions ORDER BY RANDOM() LIMIT 1;")
    res = cursor.fetchone()
    conn.close()
    return {
        "id":res[0],
        "name":res[1],
        "image":res[2]
    }

def get_all_champions_in_list() -> list:
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM champions")
    champions = cursor.fetchall()
    conn.close()
    return [
        {
            "id":champion[0],
            "name":champion[1],
            "image":champion[2]
        }
        for champion in champions
    ]

    

@bot.event
async def on_ready():
    print('Le Bot '+bot.user.display_name+' Est Prêt !')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="play", description="Jouer au jeu")
@app_commands.describe(difficulte = "Quelle difficulté ?")
@app_commands.choices(difficulte=[
    discord.app_commands.Choice(name="Facile", value="facile"),
    discord.app_commands.Choice(name="Difficile", value="difficile")
])
async def play(interaction: discord.Interaction, difficulte: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    champion = get_random_champion()
    channelId = str(interaction.channel_id)
    guildId = str(interaction.guild_id)
    typeJeu = "champion"
    mot = champion["name"]

    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    insert_query = "INSERT INTO Jeu (channelId, guildId, typeJeu, mot) VALUES (?, ?, ?, ?);"
    #cursor.execute(insert_query, (channelId, guildId, typeJeu, mot))
    #conn.commit()
    conn.close()

    embed = discord.Embed()
    embed.set_image(url=champion["image"])
    
    if difficulte.value == "facile":
        champions = get_all_champions_in_list()
    else:
        ""
    await interaction.followup.send(embed=embed)


bot.run("MTE1OTA0NTA5MDUzMTA5MDUxNA.G_UKht.r5v82l70L_rKUrJ4iX0PXOeV5Dwh6ov0s648hI")
