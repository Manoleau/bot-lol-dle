import discord
from discord.ext import commands
from discord import app_commands
import time
from datetime import datetime
assets = {
    "LoL" : {
        "name" : "LeagueLogo",
        "image-location": "assets/logo/LeagueLogo.png",
        "image" : "LeagueLogo.png"
    }
}
# from initBot import LeagueDleBot
def get(bot):
    @bot.tree.command(name="daily", description="Vous pouvez gagner des golds toutes les 24h")
    async def daily(interaction: discord.Interaction):
        await interaction.response.defer()
        timeAc = int(time.time())
        daily = bot.D.get_joueur_daily_by_id(interaction.user.id)
        if daily == None:
            bot.D.insert_joueur_in_db(interaction.user.id, interaction.user.name)
            daily = bot.D.get_joueur_daily_by_id(interaction.user.id)
        if daily != None:
            embed = discord.Embed()
            if daily == 0 or daily + 86400 <= timeAc:
                bot.D.daily_use_by(interaction.user.id, timeAc)
                embed.color = discord.Colour.purple()
                embed.title = f":white_check_mark: Daily récupéré"
                embed.description = f"**+3600 {bot.getGoldsEmoji()}**"
            else:
                embed.color = discord.Colour.red()
                remaining_time_daily = 86400 - (timeAc - daily)
                hours, remainder = divmod(remaining_time_daily, 3600)
                minutes, seconds = divmod(remainder, 60)
                if int(hours) == 0 and int(minutes) == 0:
                    time_daily = "{:02d} seconds".format(int(seconds))
                elif int(hours) == 0:
                    time_daily = "{:02d}:{:02d} minutes".format(int(minutes), int(seconds))
                else:
                    time_daily = "{:02d}:{:02d}:{:02d} heures".format(int(hours), int(minutes), int(seconds))
            
                embed.title = f":x: Impossible de récupérer le daily"
                embed.description = f"Réessayer dans **{time_daily}**"
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"{interaction.user.mention}, vous n'avez pas encore jouer.")