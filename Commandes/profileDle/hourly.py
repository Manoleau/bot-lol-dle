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
    @bot.tree.command(name="hourly", description="Vous pouvez gagner des golds toutes les heures")
    async def hourly(interaction: discord.Interaction):
        await interaction.response.defer()
        timeAc = int(time.time())
        hourly = bot.D.get_joueur_hourly_by_id(interaction.user.id)
        if hourly == None:
            bot.D.insert_joueur_in_db(interaction.user.id, interaction.user.name)
            hourly = bot.D.get_joueur_hourly_by_id(interaction.user.id)
        if hourly != None:
            embed = discord.Embed()
            if hourly == 0 or hourly + 3600 <= timeAc:
                bot.D.hourly_use_by(interaction.user.id, timeAc)
                embed.color = discord.Colour.purple()
                embed.title = f":white_check_mark: Hourly récupéré"
                embed.description = f"**+130 {bot.getGoldsEmoji()}**"
            else:
                embed.color = discord.Colour.red()
                remaining_time_hourly = 3600 - (timeAc - hourly)
                hours, remainder = divmod(remaining_time_hourly, 3600)
                minutes, seconds = divmod(remainder, 60)
                if int(minutes) == 0:
                    time_hourly = "{:02d} seconds".format(int(seconds))
                else:
                    time_hourly = "{:02d}:{:02d} minutes".format(int(minutes), int(seconds))
                embed.title = f":x: Impossible de récupérer le hourly"
                embed.description = f"Réessayer dans **{time_hourly}**"
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"{interaction.user.mention}, vous n'avez pas encore jouer.")