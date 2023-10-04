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

league = League()

@bot.event
async def on_ready():
    print('Le Bot '+bot.user.display_name+' Est Prêt !')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="play", description="Jouer au jeu")
async def play(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send("oui")

@bot.tree.command(name="download-image", description="telecharge image")
async def downloadimage(interaction: discord.Interaction):
    await interaction.response.defer()
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    conn.commit()
    conn.close()
    await interaction.followup.send("oui")



@bot.tree.command(name="inserer-dans-db", description="Insere dans la db les images")
async def insererdansdb(interaction: discord.Interaction):
    await interaction.response.defer()
    conn = sqlite3.connect('DB/LeagueDle.db')
    cursor = conn.cursor()
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS versions(
    #     version VARCHAR(255) PRIMARY KEY
    # );
    # """)
    # for version in league.versions:
    #     insert_query = "INSERT INTO versions (version) VALUES (?)"
    #     cursor.execute(insert_query, (version,))
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS champions(
    #     id NUMBER PRIMARY KEY,
    #     name VARCHAR(255),
    #     image VARCHAR(255)
    # );
    # """)
    
    # delete_query = "DELETE FROM items"
    # cursor.execute(delete_query)
    # delete_query = "DELETE FROM champions"
    # cursor.execute(delete_query)
    # for champion in league.champions:
    #     insert_query = "INSERT INTO champions (id, name, image) VALUES (?, ?, ?)"
    #     cursor.execute(insert_query, (league.champions[champion].id, league.champions[champion].name, league.champions[champion].image))
    # for item in league.items:
    #     insert_query = "INSERT INTO items (id, name, image) VALUES (?, ?, ?)"
    #     cursor.execute(insert_query, (league.items[item].id, league.items[item].name, league.items[item].image))
    conn.commit()
    conn.close()
    await interaction.followup.send("oui")

bot.run("MTE1OTA0NTA5MDUzMTA5MDUxNA.G_UKht.r5v82l70L_rKUrJ4iX0PXOeV5Dwh6ov0s648hI")
