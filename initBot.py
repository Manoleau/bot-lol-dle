import discord
from discord.ext import commands
from discord import app_commands
from MenuSelect.ChoixChampion import ChampView
from Bouton.RejouerItemChampionBoutton import Rejouer
from Bouton.UpdateBtn import UpdateLol
from Bouton.StopGameBoutton import StopGame
from Bouton.PageBtn import Page

import Commandes.guess.champion as guesschampion
import Commandes.guess.item as guessitem

import Commandes.info.champions as champions
import Commandes.info.items as items
import Commandes.info.regions as region

import Commandes.profileDle.balance as balance
import Commandes.profileDle.niveau as niveau
import Commandes.profileDle.profile as profile
import Commandes.profileDle.pullskin as pullskin
import Commandes.profileDle.daily as daily
import Commandes.profileDle.hourly as hourly
import Commandes.profileDle.myskin as myskin

import Commandes.profileLol.linklol as linklol
import Commandes.profileLol.profile as profilelol
import Commandes.profileLol.updateprofile as updateprofile

import re
from data_base import DB
from riotwatcher import LolWatcher, ApiError
import requests
from unidecode import unidecode
from Class.League import League

versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()

class LeagueDleBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.versionAc = versions[0]
        self.rejouerBtn = Rejouer
        self.champView = ChampView
        self.updateBtn = UpdateLol
        self.stopBtn = StopGame
        self.pageBtn = Page
        self.update = False
        self.commandes = None
        self.liste_serveur_emoji_id = [1154032237122158602, 1159513438310125698, 1159514828772229241, 1159514864616734760, 1159514890743054417, 1159514914491215963, 1159514941473165322, 1159514967905673279, 1159516097444323448]
        self.lol_watcher = LolWatcher('RGAPI-262c2d47-ff25-4776-9fe5-78d6f1bdfc58')
        
    async def setup_hook(self) -> None:
        try:
            self.D = DB(versions[0], self)
            # if not self.D.has_version(versions[0]):
            #     self.update = True
            #     league = League()
            #     longueur = len(league.champions)
            #     for champion in league.champions:
            #         print(f"il reste {str(longueur)} champions")
            #         print(f"{league.champions[champion].name} : {league.champions[champion].image}\n")
            #         serveur_id = self.D.get_serveur_id(league.champions[champion].id)
            #         old_champ = self.D.get_champion_by_id(league.champions[champion].id)
            #         await self.D.update_champion_when_lol_update(league.champions[champion], old_champ, self.get_guild(serveur_id))
            #         longueur -=1
            #     longueur = len(league.items)
            #     for item in league.items:
            #         serveur_id = self.D.get_serveur_id(league.items[item].id)
            #         old_item = self.D.get_item_by_id(league.items[item].id)
            #         print(f"il reste {str(longueur)} items")
            #         print(f"{league.items[item].name} : {league.items[item].image}\n")
            #         if league.items[item].description != "":
            #             if old_item == None:
            #                 i = 1
            #                 serveur = self.get_guild(liste_serveur_emoji_id[0])
            #                 while i < len(liste_serveur_emoji_id) and len(serveur.emojis) >= serveur.emoji_limit:
            #                     serveur = self.get_guild(liste_serveur_emoji_id[i])
            #                     i+=1
            #                 if i != len(liste_serveur_emoji_id):
            #                     await self.D.ajout_emoji_in_serveur(serveur, unidecode(league.items[item].name).replace("'","").replace(" ", "").replace(".","").replace("-","").replace("œ","oe").replace(",",""), league.items[item].image)
            #                 else:
            #                     print("Veillez créer des nouveaux serveurs d'emoji !")
            #             try:
            #                 await self.D.update_item_when_lol_update(league.items[item], old_item, self.get_guild(serveur_id))
            #             except:
            #                 print(f"Dans le serveur {self.get_guild(serveur_id).name}, il faut update {league.items[item].name} : {league.items[item].image}")
            #         else:
            #             self.D.suppr_emojiDB(league.items[item].id)
            #         longueur -= 1
            #     self.update = False   
            #     self.D.ajout_version(versions[0])
            guesschampion.get(self)
            guessitem.get(self)
            champions.get(self)
            items.get(self)
            region.get(self)
            balance.get(self)
            niveau.get(self)
            profile.get(self)
            linklol.get(self)
            profilelol.get(self)
            pullskin.get(self)
            updateprofile.get(self)
            daily.get(self)
            hourly.get(self)
            myskin.get(self)
            self.commandes  = await self.tree.sync()
        except Exception as e:
            print(e)

    async def on_ready(self) -> None:
        # t = self.get_guild(1159514967905673279)
        # for e in t.emojis:
        #     print(f"<:{e.name}:{str(e.id)}>")
        print('Le Bot ' + self.user.display_name + ' Est Prêt !')
        print(f"Synced {len(self.commandes)} command(s)")
        
    
    async def on_disconnect(self):
        # self.D.conn.close()
        print(f"Le bot {self.user.name} s'est déconnecté.")
    
    def getLvlUpEmoji(self):
        return "<:levelup:1164279782364688484>"
    def getGoldsEmoji(self):
        return "<:dollarcoin:1164288247191584768>"
    def getXpEmoji(self):
        return "<:xp:1164291870680170516>"
    
    def create_embed_missing_joueur(self,nomJoueur:str) -> discord.Embed:
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.description = nomJoueur+" n'a pas encore de compte ! Il faut gagné au moins une partie."
        return embed
    def create_embed_missing_item(self,nomItem:str) -> discord.Embed:
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.description = "**"+nomItem+"** n'existe pas !"
        return embed
    def create_embed_missing_champion(self,nomChampion:str) -> discord.Embed:
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.description = "**"+nomChampion+"** n'existe pas !"
        return embed

    def compteur_victoire_un_joueur(self,liste_parties:list) -> dict:
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
        self.trier_victoire(res)
        return res
    def compteur_victoire_un_mode(self,liste_parties:list) -> dict:
        res = {
            "facile":False,
            "difficile":False,
            "joueurs":{}
        }
        dict_joueurs = {}
        for partie in liste_parties:
            if partie[7] not in dict_joueurs:
                dict_joueurs[partie[7]] = self.D.get_joueur_by_id(partie[7])
                dict_joueurs[partie[7]]
            if partie[5] == "difficile":
                res["difficile"] = True
            else:
                res["facile"] = True
        res["joueurs"] = dict_joueurs
        return res

    def trier_victoire(self,dict_victoire:dict):
        if "facile" in dict_victoire["champion"]:
            dict_victoire["champion"]["facile"] = dict(sorted(dict_victoire["champion"]["facile"].items(), key=lambda item: item[1], reverse=True))
        if "difficile" in dict_victoire["champion"]:
            dict_victoire["champion"]["difficile"] = dict(sorted(dict_victoire["champion"]["difficile"].items(), key=lambda item: item[1], reverse=True))
        if "facile" in dict_victoire["item"]:
            dict_victoire["item"]["facile"] = dict(sorted(dict_victoire["item"]["facile"].items(), key=lambda item: item[1], reverse=True))
        if "difficile" in dict_victoire["item"]:
            dict_victoire["item"]["difficile"] = dict(sorted(dict_victoire["item"]["difficile"].items(), key=lambda item: item[1], reverse=True))
    def has_accent(self,input_string:str):
        pattern = r'[À-ÖÙ-öÙ-ÿ]'
        return bool(re.search(pattern, input_string))

    def creer_liste_possibilite_champion(self, nomChampion:str):
        liste_possibilite = [nomChampion]
        accent = self.has_accent(nomChampion)
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
        return liste_possibilite
    def creer_liste_possibilite_item(self,nomItem:str):
        liste_possibilite = [nomItem]
        accent = self.has_accent(nomItem)
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
        return liste_possibilite

    
    async def on_message(self, message: discord.Message):
        # if message.author.id == 383497419460968448:
        #     if not message.author.dm_channel:
        #         dm = await message.author.create_dm()
        #         await dm.send("EZ")
        #     else:
        #         await message.author.dm_channel.send("EZ")
        if not message.author.bot and not self.update:
            if message.guild:

                channelId = str(message.channel.id)
                guildId = str(message.guild.id)

                game = self.D.get_game_by_channel_and_guild(channelId, guildId, False)
                if game is not None:
                    if(game["typeJeu"] == "champion"):
                        request = message.content.lower()
                        nomChampion = game["mot"].lower()
                        liste_possibilite = self.creer_liste_possibilite_champion(nomChampion)
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
                            embed.title = f"{message.author.display_name} a gagné !"
                            if game["difficulte"] == "facile":
                                embed.description = f"{self.getXpEmoji()} 30 xp\n{self.getGoldsEmoji()} 40 golds"
                                if not self.D.get_joueur_by_id(message.author.id):
                                    self.D.insert_joueur_in_db(message.author.id, message.author.name)
                                lvlUp = self.D.update_jeu_gagnant(game["id"], message.author.id, 30, 40)
                            else:
                                embed.description = f"{self.getXpEmoji()} 75 xp\n{self.getGoldsEmoji()} 90 golds"
                                if not self.D.get_joueur_by_id(message.author.id):
                                    self.D.insert_joueur_in_db(message.author.id, message.author.name)
                                lvlUp = self.D.update_jeu_gagnant(game["id"], message.author.id, 75, 90)

                            embed.set_thumbnail(url=message.author.display_avatar.url)
                            embed.add_field(name="Réponse", value="**"+game["mot"]+"**", inline=True)
                            embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                            embed.set_image(url=self.D.get_champion_splash_by_name(game["mot"]))
                            await message.channel.send(embed=embed, view=self.rejouerBtn(self, game["typeJeu"], game["difficulte"]))
                            if lvlUp:
                                embed = discord.Embed()
                                embed.color = discord.Colour.purple()
                                embed.title = f"{self.getLvlUpEmoji()} {message.author.display_name} a gagné un niveau !"
                                embed.description = f"Niveau : {str(lvlUp-1)} :arrow_right: {str(lvlUp)}\n{self.getGoldsEmoji()} 200 Golds"
                                embed.set_thumbnail(url=message.author.display_avatar.url)
                                await message.channel.send(embed=embed)
                    elif(game["typeJeu"] == "item"):
                        request = message.content.lower().replace("œ","oe")
                        liste_possibilite = []
                        nomItem = game["mot"].lower()
                        liste_possibilite = self.creer_liste_possibilite_item(nomItem)
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
                            if game["difficulte"] == "facile":
                                embed.description = f"{self.getXpEmoji()} 40 xp\n{self.getGoldsEmoji()} 50 golds"
                                if not self.D.get_joueur_by_id(message.author.id):
                                    self.D.insert_joueur_in_db(message.author.id, message.author.name)
                                lvlUp = self.D.update_jeu_gagnant(game["id"], message.author.id, 30, 40)
                            else:
                                embed.description = f"{self.getXpEmoji()} 85 xp\n{self.getGoldsEmoji()} 100 golds"
                                if not self.D.get_joueur_by_id(message.author.id):
                                    self.D.insert_joueur_in_db(message.author.id, message.author.name)
                                lvlUp = self.D.update_jeu_gagnant(game["id"], message.author.id, 75, 90)
                            embed.color = discord.Colour.green()
                            embed.title = f"{message.author.display_name} a gagné !"
                            embed.set_thumbnail(url=message.author.display_avatar.url)
                            embed.add_field(name="Réponse", value="**"+game["mot"]+"**", inline=True)
                            embed.add_field(name="Réponses Alternatives", value=message_possibilite, inline=True)
                            embed.set_image(url=self.D.get_item_image_by_name(game["mot"]))
                            await message.channel.send(embed=embed, view=self.rejouerBtn(self, game["typeJeu"], game["difficulte"]))
                            if lvlUp:
                                embed = discord.Embed()
                                embed.color = discord.Colour.purple()
                                embed.title = f"{self.getLvlUpEmoji()} {message.author.display_name} a gagné un niveau !"
                                embed.description = f"Niveau : {str(lvlUp-1)} :arrow_right: {str(lvlUp)}\n{self.getGoldsEmoji()} 200 Golds"
                                embed.set_thumbnail(url=message.author.display_avatar.url)
                                await message.channel.send(embed=embed)
            else:
                if message.content.lower() == "ez":
                    if not message.author.dm_channel:
                        dm = await message.author.create_dm()
                        await dm.send("EZ")
                    else:
                        await message.author.dm_channel.send("EZ")