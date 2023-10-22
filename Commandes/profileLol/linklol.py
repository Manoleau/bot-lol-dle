import discord
from discord.ext import commands
from discord import app_commands
import requests
assets = {
    "LoL" : {
        "name" : "LeagueLogo",
        "image-location": "assets/logo/LeagueLogo.png",
        "image" : "LeagueLogo.png"
    }
}
# from initBot import LeagueDleBot
def get(bot):
    @bot.tree.command(name="link-account-lol", description="Lie votre compte lol à discord")
    @app_commands.describe(pseudo = "Votre pseudo League of Legends")
    async def linklol(interaction: discord.Interaction, pseudo:str):
        await interaction.response.defer()
        embed = discord.Embed()
        try:
            joueur = bot.lol_watcher.summoner.by_name("euw1", pseudo)
            league = bot.lol_watcher.league.by_summoner("euw1", joueur['id'])
            masterytmp = requests.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{joueur['puuid']}/top?count=3&api_key=RGAPI-262c2d47-ff25-4776-9fe5-78d6f1bdfc58").json()
            if not bot.D.if_joueur_in_db(interaction.user.id):
                bot.D.insert_joueur_in_db(interaction.user.id, interaction.user.name)
            if not bot.D.if_compte_lol_in_db(joueur["id"]):
                bot.D.add_compte_lol(joueur, league, masterytmp)
            else:
                bot.D.update_compte_lol(joueur, league, masterytmp)
            bot.D.add_compte_lol_to_joueur(interaction.user.id, joueur["name"])
            embed.title = ":white_check_mark: Succés"
            embed.color = discord.Colour.green()
            embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/{bot.versionAc}/img/profileicon/{str(joueur['profileIconId'])}.png")
            embed.description = f"*{pseudo}* vient d'être lié avec votre compte discord."
        except Exception as e:
            print(e)
            embed.color = discord.Colour.red()
            embed.title = ":x:"
            embed.description = f"{pseudo} n'existe pas"
        await interaction.followup.send(embed=embed)
