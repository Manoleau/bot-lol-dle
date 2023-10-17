import discord
from discord.ext import commands
from discord import app_commands
import random
import requests
import re
from unidecode import unidecode

from MenuSelect.ChoixChampion import ChampView
from Boutton.RejouerItemChampionBoutton import Rejouer
from Boutton.ModalTestBtn import AfficheModal
from data_base import DB

# asyncio
# aiohttp
# re
# requests
# bs4
# lxml
# unidecode

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

liste_serveur_emoji_id = [1154032237122158602, 1159513438310125698, 1159514828772229241, 1159514864616734760, 1159514890743054417, 1159514914491215963, 1159514941473165322, 1159514967905673279, 1159516097444323448]

versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
D = DB(versions[0])

assets = {
    "LoL" : {
        "name" : "League of Legends",
        "image-location": "assets/logo/League-of-Legends.png",
        "image" : "League-of-Legends.png"
    }
}

roles = {
    "Assassin": "Assassin",
    "Fighter": "Combattant",
    "Mage": "Mage",
    "Marksman": "Tireur",
    "Support": "Support",
    "Tank": "Tank",
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
        self.tags = []
        self.title = info_champion["title"]
        self.splash_art = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{info_champion['id']}_0.jpg"
        for tag in info_champion["tags"]:
            self.tags.append(roles[tag])

if not D.has_version(versions[0]):
    update = True
else: 
    update = False

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
def create_embed_missing_champion(nomChampion:str) -> discord.Embed:
    embed = discord.Embed()
    embed.color = discord.Color.red()
    embed.description = "**"+nomChampion+"** n'existe pas !"
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
            dict_joueurs[partie[7]] = D.get_joueur_by_id(partie[7])
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

@bot.event
async def on_ready():
    print('Le Bot '+bot.user.display_name+' Est Prêt !')
    try:
        # if update:
        #     liste_serveur_emoji = [bot.get_guild(id_serv) for id_serv in liste_serveur_emoji_id]
        #     await D.update_emoji(liste_serveur_emoji)
        if update:
            b = {}
            for serveur_id in liste_serveur_emoji_id:
                serveur = bot.get_guild(serveur_id)
                b[str(serveur_id)] = {}
                for emoji in serveur.emojis:
                    b[str(serveur_id)][emoji.name] = emoji.id
                # print()
            # print(b)
            ## vide les table
            league = League()
            for champion in league.champions:
                ""
                # D.update_champion_when_lol_update(league.champions[champion])
                # D.add_champion(league.champions[champion].id, league.champions[champion].name, league.champions[champion].image, league.champions[champion].title, league.champions[champion].splash_art)
            for item in league.items:
                ""
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_disconnect():
    D.conn.close()
    print(f"Le bot {bot.user.name} s'est déconnecté.")

@bot.tree.command(name="test", description="test")
async def test(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed()
    embed.description = "Appuie sur le boutton pour afficher la modal de test"
    await interaction.followup.send(embed=embed, view=AfficheModal())


@bot.tree.command(name="guess-champion", description="Trouve le champion")
@app_commands.describe(difficulte = "Quelle difficulté ?")
@app_commands.choices(difficulte=[
    discord.app_commands.Choice(name="Facile", value="facile"),
    discord.app_commands.Choice(name="Difficile", value="difficile")
])
async def guesschampion(interaction: discord.Interaction, difficulte: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    channelId = str(interaction.channel_id)
    guildId = str(interaction.guild_id)
    typeJeu = "champion"
    res = D.get_game_by_channel_and_guild(channelId, guildId, False)
    embed = discord.Embed()
    if res is None:
        embed.color = discord.Colour(0x425b8a)
        logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
        embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
        if difficulte.value == "facile":
            champion = D.get_random_champion()
            mot = champion["name"]
            embed.set_author(name="Qui est ce champion ?")
            embed.set_image(url=champion["image"])
        else:
            champion = D.get_random_champion()
            mot = champion["name"]
            embed.add_field(name="Quel est le champion qui a ce titre ?", value="\u200b\n**"+champion["title"]+"**\n\u200b")
        D.add_game(channelId, guildId, typeJeu, mot, difficulte.value)
        await interaction.followup.send(embed=embed, file=logo_lol)
        gameId = D.get_game_id(channelId, guildId, False)
        await D.timer_indice(interaction=interaction, gameId=gameId, typeJeu=typeJeu, channelId=channelId, guildId=guildId, mot=mot)
    else:
        embed.description = "Une partie est déjà en cours dans ce channel..."
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="guess-item", description="Trouve l'item")
@app_commands.describe(difficulte = "Quelle difficulté ?")
@app_commands.choices(difficulte=[
    discord.app_commands.Choice(name="Facile", value="facile"),
    discord.app_commands.Choice(name="Difficile", value="difficile")
])
async def guessitem(interaction: discord.Interaction, difficulte: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    channelId = str(interaction.channel_id)
    guildId = str(interaction.guild_id)
    typeJeu = "item"
    res = D.get_game_by_channel_and_guild(channelId, guildId, False)
    embed = discord.Embed()
    if res is None:
        embed.color = discord.Colour(0x425b8a)
        logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
        embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
        if difficulte.value == "facile":
            item = D.get_random_item()
            mot = item["name"].replace("œ","oe")
            embed.description = "*nom de l'item complet uniquement*"
            embed.set_author(name="Quel est le nom de cet item ?")
            embed.set_image(url=item["image"])
        else:
            item = D.get_random_item()
            mot = item["name"].replace("œ","oe")
            embed.add_field(name="Quel est l'item qui correspond a cette description ?", value=item["description"])
        D.add_game(channelId, guildId, typeJeu, mot, difficulte.value)
        await interaction.followup.send(embed=embed, file=logo_lol)
        gameId = D.get_game_id(channelId, guildId, False)
        await D.timer_indice(interaction=interaction, gameId=gameId, typeJeu=typeJeu, channelId=channelId, guildId=guildId, mot=mot)
    else:
        embed.description = "Une partie est déjà en cours dans ce channel..."
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
        joueur_info = D.get_joueur_by_name(joueur)
        if joueur_info:
            embed.set_thumbnail(url=joueur_info["avatar_url"])
            embed.description = "Victoires de **"+joueur+"** dans la catégorie *"+mode.value+"*"
            D.cursor.execute("SELECT * FROM Jeu WHERE idGagnant = ? AND typeJeu = ?;", (joueur_info["id"], mode.value))
            res = D.cursor.fetchall()
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
                                emoji = D.get_emoji(str(D.get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = D.get_emoji(str(D.get_item_id_by_name(champion_item)))
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
                                emoji = D.get_emoji(str(D.get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = D.get_emoji(str(D.get_item_id_by_name(champion_item)))
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
                                emoji = D.get_emoji(str(D.get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = D.get_emoji(str(D.get_item_id_by_name(champion_item)))
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
                                emoji = D.get_emoji(str(D.get_champion_id_by_name(champion_item)))
                            elif mode.value == "item":
                                emoji = D.get_emoji(str(D.get_item_id_by_name(champion_item)))
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
        joueur_info = D.get_joueur_by_name(joueur)
        if joueur_info:
            embed.description = "Victoires de **"+joueur+"** dans les catégories *champion* et *item*"
            embed.set_thumbnail(url=joueur_info["avatar_url"])
            D.cursor.execute("SELECT * FROM Jeu WHERE idGagnant = ?;", (joueur_info["id"],))
            res = D.cursor.fetchall()
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
                                emoji = D.get_emoji(str(D.get_champion_id_by_name(champion)))
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
                                emoji = D.get_emoji(str(D.get_champion_id_by_name(champion)))
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
                                emoji = D.get_emoji(str(D.get_item_id_by_name(item)))
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
                                emoji = D.get_emoji(str(D.get_item_id_by_name(item)))
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

        D.cursor.execute("SELECT * FROM Jeu WHERE typeJeu = ? AND idGagnant IS NOT NULL;", (mode.value,))
        compteurVictoire = compteur_victoire_un_mode(D.cursor.fetchall())

        D.cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
        classement_total_joueurs = D.cursor.fetchall()

        dict_joueurs = compteurVictoire["joueurs"]
        if compteurVictoire["facile"] and compteurVictoire["difficile"]:
            D.cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'facile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_facile_joueurs = D.cursor.fetchall()
            D.cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'difficile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_difficile_joueurs = D.cursor.fetchall()
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
            D.cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'facile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_facile_joueurs = D.cursor.fetchall()
        elif "difficile" in compteurVictoire["parties"]:
            
            D.cursor.execute("SELECT idGagnant, COUNT(idGagnant) AS nombre_victoires FROM Jeu WHERE idGagnant IS NOT NULL AND typeJeu = ? AND difficulte = 'difficile' GROUP BY idGagnant ORDER BY nombre_victoires DESC;", (mode.value,))
            classement_difficile_joueurs = D.cursor.fetchall()
        else:
            embed.add_field(name="Totaux", value="`0`")
     
    else:
        embed.add_field(name="en cours...", value="en cours...")
          
    await interaction.followup.send(embed=embed, file=logo_lol, ephemeral=True)

@bot.tree.command(name="items", description="Affiche tous les items, si un item est séléctionné alors on affiche les stats")
@app_commands.describe(item = "Nom de l'item")
@app_commands.describe(lettre = "Une lettre")
async def items(interaction: discord.Interaction, item: str = None, lettre:str = None):
    await interaction.response.defer()
    embed = discord.Embed()
    if item:
        item_info = D.get_item_by_name(item)
        if item_info:
            logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
            embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
            embed.set_thumbnail(url=item_info["image"])
            embed.set_author(name=item)
            embed.add_field(name="Description/Stats", value=item_info["description"],inline=False)
            await interaction.followup.send(embed=embed, file=logo_lol)
        else:
            embed = create_embed_missing_item(item)
            lettre = item[0].upper()
            embed.description += "\nFaites /items lettre: "+lettre
            await interaction.followup.send(embed=embed)            
    elif lettre:
        lettre = lettre.upper()
        items_info = D.get_all_items_in_list_start_with(lettre)
        if items_info:
            logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
            embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
            embed.set_author(name="Items commençant par "+lettre)
            msg = ""
            nb_lettres = 0
            for item_info in items_info:
                emoji = D.get_emoji(str(item_info["id"]))
                tmp = f"<:{emoji['nom_emoji']}:{emoji['id']}> {item_info['name']}\n"
                msg += tmp
                nb_lettres += len(tmp)
                if nb_lettres >= 950:
                    nb_lettres = 0
                    embed.add_field(name="\u200b", value=msg)
                    msg = ""
            if msg != "":
                embed.add_field(name="\u200b", value=msg)
            await interaction.followup.send(embed=embed, file=logo_lol)
        else:
            await interaction.followup.send("Veillez entrer une lettre correct !")
    else:
        await interaction.followup.send(content="Veillez entrer une lettre ou un nom d'item !")

@bot.tree.command(name="champions", description="Affiche tous les champions, si un item est séléctionné alors on affiche ")
@app_commands.describe(champion = "Nom du champion")
@app_commands.describe(lettre = "Une lettre")
async def champions(interaction: discord.Interaction, champion: str = None, lettre:str = None):
    await interaction.response.defer()
    embed = discord.Embed()
    if champion:
        champion_info = D.get_champion_by_name(champion)
        if champion_info:
            logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
            embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
            embed.set_author(name=champion)
            embed.set_thumbnail(url=champion_info["image"])
            embed.description = champion_info["title"]
            embed.set_image(url=champion_info["splash_art"])
            roles = D.get_roles_champion_by_id(champion_info["id"])
            msg_roles = ""
            for role in roles:
                msg_roles += f"{role['name']}\n"
            embed.add_field(name="Genre", value=champion_info["genre"])
            embed.add_field(name="Ressource", value=champion_info["ressource"])
            embed.add_field(name="Année de sortie", value=str(champion_info["annee_sortie"]))
            embed.add_field(name="Role(s)", value=msg_roles)
            embed.add_field(name="Portée", value=champion_info["porte"])
            await interaction.followup.send(embed=embed, file=logo_lol)
        else:
            embed = create_embed_missing_champion(champion)
            lettre = champion[0].upper()
            embed.description += "\nFaites /champions lettre: "+lettre
            await interaction.followup.send(embed=embed)
        
    elif lettre:
        lettre = lettre.upper()
        champions_info = D.get_all_champions_in_list_start_with(lettre)
        if champions_info:
            logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
            embed.set_footer(text="Version : "+versions[0], icon_url="attachment://"+assets["LoL"]["image"])
            embed.set_author(name="Champions commençant par "+lettre)
            msg = ""
            nb_lettres = 0
            for champion_info in champions_info:
                emoji = D.get_emoji(str(champion_info["id"]))
                tmp = f"<:{emoji['nom_emoji']}:{emoji['id']}> {champion_info['name']}\n"
                msg += tmp
                nb_lettres += len(tmp)
                if nb_lettres >= 950:
                    nb_lettres = 0
                    embed.add_field(name="\u200b", value=msg)
                    msg = ""
            if msg != "":
                embed.add_field(name="\u200b", value=msg)
            await interaction.followup.send(embed=embed, file=logo_lol, view=ChampView(D,champions_info))
        else:
            await interaction.followup.send("Veillez entrer une lettre correct !")
    else:
        await interaction.followup.send("Veillez entrer une lettre ou un nom de champion !")

@bot.tree.command(name="region", description="Affiche tous les champions, si un item est séléctionné alors on affiche ")
@app_commands.describe(nom = "Nom de la région")
@app_commands.choices(nom=[
    discord.app_commands.Choice(name="Ionia", value="Ionia"),
    discord.app_commands.Choice(name="Bandle", value="Bandle"),
    discord.app_commands.Choice(name="Bilgewater", value="Bilgewater"),
    discord.app_commands.Choice(name="Demacia", value="Demacia"),
    discord.app_commands.Choice(name="Freljord", value="Freljord"),
    discord.app_commands.Choice(name="Ixtal", value="Ixtal"),
    discord.app_commands.Choice(name="Néant", value="Néant"),
    discord.app_commands.Choice(name="Noxus", value="Noxus"),
    discord.app_commands.Choice(name="Piltover", value="Piltover"),
    discord.app_commands.Choice(name="Shurima", value="Shurima"),
    discord.app_commands.Choice(name="Targon", value="Targon"),
    discord.app_commands.Choice(name="Zaun", value="Zaun"),
    discord.app_commands.Choice(name="Iles Obscures", value="Iles Obscures")
])
async def region(interaction: discord.Interaction, nom: discord.app_commands.Choice[str] = None):
    await interaction.response.defer()
    embed = discord.Embed()
    if nom:
        region = D.get_region_by_name(nom.value)
        if region:
            embed.set_author(name=region["name"])
            embed.set_thumbnail(url=region["logo"])
            embed.set_image(url=region["splash"])
            region["description"] = region["description"].replace("\n", "\n\n")
            if len(region["description"]) >= 1024:
                if "\n" in region["description"]:
                    espace = False
                    description = region["description"].split("\n")
                else:
                    espace = True
                    description = region["description"].split(" ")
                msg = ""
                for partie_desc in description:
                    tmp = msg
                    if espace:
                        msg += partie_desc + " "
                    else:
                        msg += partie_desc + "\n"
                    if len(msg) >= 1024:
                        
                        embed.add_field(name="Histoire", value=tmp, inline=False)
                        if espace:
                            msg = partie_desc + " "
                        else:
                            msg = partie_desc + "\n"
                embed.add_field(name="\u200b", value=msg, inline=False)

            else:
                embed.add_field(name="Histoire", value=region["description"], inline=False)
    else:
        msg = ""
        regions = D.get_all_regions()
        for region in regions:
            emoji = D.get_emoji(str(region['id']))
            msg += f"<:{emoji['nom_emoji']}:{emoji['id']}> {region['name']}\n"
        embed.add_field(name="Régions", value=msg)
    await interaction.followup.send(embed=embed)

@bot.event
async def on_message(message: discord.Message):
    if not message.author.bot:
        channelId = str(message.channel.id)
        guildId = str(message.guild.id)

        game = D.get_game_by_channel_and_guild(channelId, guildId, False)
        if game is not None:
            if(game["typeJeu"] == "champion"):
                request = message.content.lower()
                liste_possibilite = []
                nomChampion = game["mot"].lower()
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
                    message_indice = await message.channel.fetch_message(game["message_indice_id"])
                    await message_indice.delete()
                    if game["message_warn_id"]:
                        message_warn = await message.channel.fetch_message(game["message_warn_id"])
                        await message_warn.delete()
                    message_possibilite = ""
                    for possibilite in liste_possibilite:
                        message_possibilite += "• "+possibilite+"\n"
                    embed.color = discord.Colour.green()
                    embed.set_author(name=message.author.name+" a gagné !")
                    embed.set_thumbnail(url=message.author.display_avatar.url)
                    embed.add_field(name="Réponse", value="**"+game["mot"]+"**", inline=True)
                    embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                    embed.set_image(url=D.get_champion_splash_by_name(game["mot"]))
                    if not D.get_joueur_by_id(str(message.author.id)):
                        D.insert_joueur_in_db(str(message.author.id), message.author.name, message.author.display_avatar.url)
                    D.update_jeu_gagnant(game["id"], str(message.author.id))
                    await message.channel.send(embed=embed, view=Rejouer(D, game["typeJeu"], game["difficulte"]))
            elif(game["typeJeu"] == "item"):
                request = message.content.lower().replace("œ","oe")
                liste_possibilite = []
                nomItem = game["mot"].lower()
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
                    message_indice = await message.channel.fetch_message(game["message_indice_id"])
                    await message_indice.delete()
                    if game["message_warn_id"]:
                        message_warn = await message.channel.fetch_message(game["message_warn_id"])
                        await message_warn.delete()
                    message_possibilite = ""
                    for possibilite in liste_possibilite:
                        message_possibilite += "• "+possibilite+"\n"
                    embed.color = discord.Colour.green()
                    embed.set_author(name=message.author.name+" a gagné !")
                    embed.set_thumbnail(url=message.author.display_avatar.url)
                    embed.add_field(name="Réponse", value="**"+game["mot"]+"**", inline=True)
                    embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                    embed.set_image(url=D.get_item_image_by_name(game["mot"]))
                    if not D.get_joueur_by_id(str(message.author.id)):
                        D.insert_joueur_in_db(str(message.author.id), message.author.name, message.author.display_avatar.url)
                    D.update_jeu_gagnant(game["id"], str(message.author.id))
                    await message.channel.send(embed=embed, view=Rejouer(D, game["typeJeu"], game["difficulte"]))

bot.run("MTE1OTA0NTA5MDUzMTA5MDUxNA.G_UKht.r5v82l70L_rKUrJ4iX0PXOeV5Dwh6ov0s648hI")