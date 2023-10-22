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

# from initBot import LeagueDleBot
def get(bot):
    @bot.tree.command(name="update-profile-lol", description="Montre votre profile League of Legends")
    @app_commands.describe(pseudo = "Un pseudo League of Legends")
    async def profilelol(interaction: discord.Interaction, pseudo:str = None):
        await interaction.response.defer()
        embed = discord.Embed()
        try:
            if not pseudo:
                pseudo = bot.D.get_joueur_lol_by_id(interaction.user.id)
                if not pseudo:
                    embed.color = discord.Colour.red()
                    embed.title = ":x:"
                    embed.description = f"Vous n'avez pas lié de pseudo LoL à votre compte discord !"
                    await interaction.followup.send(embed=embed)
                    return
            joueur = bot.D.get_compte_lol(pseudo)
            if not joueur:
                joueur = bot.lol_watcher.summoner.by_name("euw1", pseudo)
                leagues = bot.lol_watcher.league.by_summoner("euw1", joueur['id'])
                masterytmp = requests.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{joueur['puuid']}/top?count=5&api_key=RGAPI-262c2d47-ff25-4776-9fe5-78d6f1bdfc58").json()
                bot.D.add_compte_lol(joueur, leagues, masterytmp)
            else:
                joueur = bot.lol_watcher.summoner.by_name("euw1", pseudo)
                leagues = bot.lol_watcher.league.by_summoner("euw1", joueur['id'])
                masterytmp = requests.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{joueur['puuid']}/top?count=5&api_key=RGAPI-262c2d47-ff25-4776-9fe5-78d6f1bdfc58").json()
                bot.D.update_compte_lol(joueur, leagues, masterytmp)
            embed.color = discord.Colour.green()
            embed.title = ":white_check_mark: Succés"
            embed.description = f"**{pseudo}** a été mise à jour."
            embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/{bot.versionAc}/img/profileicon/{str(joueur['profileIconId'])}.png")
        except Exception as e:
            print(e)
            embed.color = discord.Colour.red()
            embed.title = ":x:"
            embed.description = f"**{pseudo}** n'existe pas"
        await interaction.followup.send(embed=embed)