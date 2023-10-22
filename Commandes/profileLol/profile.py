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
    @bot.tree.command(name="profile-lol", description="Montre votre profile League of Legends", )
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
            new = False
            if not joueur:
                new = True
                joueur = bot.lol_watcher.summoner.by_name("euw1", pseudo)
                leagues = bot.lol_watcher.league.by_summoner("euw1", joueur['id'])
                masterytmp = requests.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{joueur['puuid']}/top?count=5&api_key=RGAPI-262c2d47-ff25-4776-9fe5-78d6f1bdfc58").json()
                bot.D.add_compte_lol(joueur, leagues, masterytmp)
                mastery = [
                    {
                        "name":bot.D.get_champion_name_by_id(champ["championId"]),
                        "id":champ["championId"],
                        "level":champ["championLevel"],
                        "points":champ["championPoints"],
                    } for champ in masterytmp
                ]
            else:
                leagues = bot.D.get_league_lol(joueur["id"])
                mastery = bot.D.get_mastery_lol(joueur['puuid'],joueur['id'])
            msgLeagueSolo = "N/A"
            msgLeagueFlex = "N/A"
            if leagues:
                for league in leagues:
                    if new:
                        rankedIcon = bot.D.get_ranked_icon(translate_ranked[league["tier"]])
                    else:
                        rankedIcon = bot.D.get_ranked_icon(league["tier"])
                    
                    winrate = int(round(league['wins'] / (league['wins']+league['losses']) * 100, 0))
                    if "FLEX" in league["queueType"]:
                        msgLeagueFlex = ""
                        msgLeagueFlex += f"{rankedIcon[1]} **{league['tier']} {league['rank']}**\n"
                        msgLeagueFlex += f">>> LP : {str(league['leaguePoints'])}\nVictoires : {str(league['wins'])}\nDéfaites : {str(league['losses'])}\nWinrate : {str(winrate)}%"
                        
                    elif "SOLO" in league["queueType"]:
                        msgLeagueSolo = ""
                        msgLeagueSolo += f"{rankedIcon[1]} **{league['tier']} {league['rank']}**\n"
                        msgLeagueSolo += f">>> LP : {str(league['leaguePoints'])}\nVictoires : {str(league['wins'])}\nDéfaites : {str(league['losses'])}\nWinrate : {str(winrate)}%"
            
            if mastery:
                msg_mastery = ">>> "
                for champ in mastery:
                    emojichamp = bot.D.get_emoji(champ['id'])
                    if champ["level"] <= 3:
                        emojimastery = bot.D.get_emoji_mastery(-1)
                    elif champ["level"] == 4:
                        emojimastery = bot.D.get_emoji_mastery(4)
                    elif champ["level"] == 5:
                        emojimastery = bot.D.get_emoji_mastery(5)
                    elif champ["level"] == 6:
                        emojimastery = bot.D.get_emoji_mastery(6)
                    else:
                        emojimastery = bot.D.get_emoji_mastery(7)
                    msg_mastery += f"{emojimastery} <:{emojichamp['nom_emoji']}:{emojichamp['id']}> {champ['name']} {str(champ['points'])} points\n"
                embed.title = f"{joueur['name']}"
            else:
                msg_mastery = "N/A"
            embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/{bot.versionAc}/img/profileicon/{str(joueur['profileIconId'])}.png")
            embed.description = f">>> Niveau d'invocateur : **{str(joueur['summonerLevel'])}**"
            embed.add_field(name="Solo/Duo", value=msgLeagueSolo)
            embed.add_field(name="\u200b",value="\u200b")
            embed.add_field(name="Flex", value=msgLeagueFlex)
            embed.add_field(name="Maitrise",value=msg_mastery, inline=False)
            embed.add_field(name="Historique des matchs",value="10 parties récentes",inline=False)


            embed.set_footer(text="Version : "+bot.versionAc, icon_url="attachment://"+assets["LoL"]["image"])
            embed.color = discord.Colour.gold()
            # await interaction.followup.send(embed=embed, view=bot.updateBtn(bot, pseudo))
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)
            embed.color = discord.Colour.red()
            embed.title = ":x:"
            embed.description = f"{pseudo} n'existe pas"
            await interaction.followup.send(embed=embed)
