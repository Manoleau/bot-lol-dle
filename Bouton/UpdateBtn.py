import discord
from discord.ui import Select, View, Button
import requests
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

class UpdateLol(View):
    def __init__(self, bot, pseudo:str):
        super().__init__()
        self.bot = bot
        self.DB = bot.D
        self.lol_watcher = bot.lol_watcher
        self.pseudo = pseudo

    @discord.ui.button(label="Update", style=discord.ButtonStyle.primary)
    async def update(self, interaction:discord.Interaction, button:Button):
        embed = discord.Embed()
        joueur = self.lol_watcher.summoner.by_name("euw1", self.pseudo)
        leagues = self.lol_watcher.league.by_summoner("euw1", joueur['id'])
        masterytmp = requests.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{joueur['puuid']}/top?count=3&api_key=RGAPI-262c2d47-ff25-4776-9fe5-78d6f1bdfc58").json()
        self.DB.update_compte_lol(joueur, leagues, masterytmp)
        mastery = [
            {
                "name":self.DB.get_champion_name_by_id(champ["championId"]),
                "level":champ["championLevel"],
                "points":champ["championPoints"],
            } for champ in masterytmp
        ]
        if leagues:
            msgLeagueSolo = ""
            msgLeagueFlex = ""
            for league in leagues:
                rankedIcon = self.DB.get_ranked_icon(translate_ranked[league["tier"]])
                winrate = int(round(league['wins'] / (league['wins']+league['losses']) * 100, 0))
                if "FLEX" in league["queueType"]:
                    msgLeagueFlex += f"{rankedIcon[1]} **{translate_ranked[league['tier']]} {league['rank']}**\n"
                    msgLeagueFlex += f">>> LP : {str(league['leaguePoints'])}\nVictoires : {str(league['wins'])}\nDéfaites : {str(league['losses'])}\nWinrate : {str(winrate)}%"
                elif "SOLO" in league["queueType"]:
                    msgLeagueSolo += f"{rankedIcon[1]} **{translate_ranked[league['tier']]} {league['rank']}**\n"
                    msgLeagueSolo += f">>> LP : {str(league['leaguePoints'])}\nVictoires : {str(league['wins'])}\nDéfaites : {str(league['losses'])}\nWinrate : {str(winrate)}%"
        else:
            msgLeagueSolo = "N/A"
            msgLeagueFlex = "N/A"
        msg_mastery = ">>> "
        for champ in mastery:
            msg_mastery += f"{champ['name']} {str(champ['points'])} points\n"
        embed.title = f"{joueur['name']}"
        embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/{self.DB.versionLol}/img/profileicon/{str(joueur['profileIconId'])}.png")
        embed.description = f">>> Niveau d'invocateur : **{str(joueur['summonerLevel'])}**"
        embed.add_field(name="Solo/Duo", value=msgLeagueSolo)
        embed.add_field(name="\u200b",value="\u200b")
        embed.add_field(name="Flex", value=msgLeagueFlex)
        embed.add_field(name="Maitrise",value=msg_mastery, inline=False)
        embed.add_field(name="Historique des matchs",value="10 parties récentes",inline=False)
        embed.set_footer(text="Version : "+self.DB.versionLol)
        
        await interaction.response.edit_message(embed=embed)