import discord
from discord.ext import commands
from discord import app_commands
import time
assets = {
    "LoL" : {
        "name" : "LeagueLogo",
        "image-location": "assets/logo/LeagueLogo.png",
        "image" : "LeagueLogo.png"
    }
}
# from initBot import LeagueDleBot
def get(bot):
    @bot.tree.command(name="profile", description="Montre votre profile")
    async def profile(interaction: discord.Interaction, joueur:discord.User = None):
        await interaction.response.defer()
        if joueur:
            player = bot.D.get_joueur_by_id(joueur.id)
            autre = True
            if not player:
                bot.D.insert_joueur_in_db(joueur.id, joueur.name)
                player = bot.D.get_joueur_by_id(joueur.id)
        else:
            player = bot.D.get_joueur_by_id(interaction.user.id)
            autre = False
            if not player:
                bot.D.insert_joueur_in_db(interaction.user.id, interaction.user.name)
                player = bot.D.get_joueur_by_id(interaction.user.id)
        
        if player:
            embed = discord.Embed()
            timeAc = int(time.time())
            if autre:
                embed.title=f"Profile de {joueur.display_name}"
                bot.D.cursor.execute("SELECT COUNT(*) FROM JeuDle WHERE idGagnant = ?;", (joueur.id,))
                nombre_vic = bot.D.cursor.fetchone()[0]
                totaux_skins_joueur = bot.D.get_total_skins(joueur.id)
                totaux_chromas_joueur = bot.D.get_total_chromas(joueur.id)
                hourly = bot.D.get_joueur_hourly_by_id(joueur.id)
                daily = bot.D.get_joueur_daily_by_id(joueur.id)
                embed.set_thumbnail(url=joueur.display_avatar)
            else:
                embed.title=f"Profile de {interaction.user.display_name}"
                bot.D.cursor.execute("SELECT COUNT(*) FROM JeuDle WHERE idGagnant = ?;", (interaction.user.id,))
                nombre_vic = bot.D.cursor.fetchone()[0]
                totaux_skins_joueur = bot.D.get_total_skins(interaction.user.id)
                totaux_chromas_joueur = bot.D.get_total_chromas(interaction.user.id)
                hourly = bot.D.get_joueur_hourly_by_id(interaction.user.id)
                daily = bot.D.get_joueur_daily_by_id(interaction.user.id)
                embed.set_thumbnail(url=interaction.user.display_avatar)
            if hourly == 0 or hourly + 3600 <= timeAc:
                time_hourly = "Disponible"
            else:
                remaining_time_hourly = 3600 - (timeAc - hourly)
                hours, remainder = divmod(remaining_time_hourly, 3600)
                minutes, seconds = divmod(remainder, 60)
                if int(minutes) == 0:
                    time_hourly = "{:02d} seconds".format(int(seconds))
                else:
                    time_hourly = "{:02d}:{:02d} minutes".format(int(minutes), int(seconds))
            if daily == 0 or daily + 86400 <= timeAc:
                time_daily = "Disponible"
            else:
                remaining_time_daily = 86400 - (timeAc - daily)
                hours, remainder = divmod(remaining_time_daily, 3600)
                minutes, seconds = divmod(remainder, 60)
                if int(hours) == 0 and int(minutes) == 0:
                    time_daily = "{:02d} seconds".format(int(seconds))
                elif int(hours) == 0:
                    time_daily = "{:02d}:{:02d} minutes".format(int(minutes), int(seconds))
                else:
                    time_daily = "{:02d}:{:02d}:{:02d} heures".format(int(hours), int(minutes), int(seconds))
            
            # color_hex = "#D33528"
            # embed_color = int(color_hex[1:], 16)
            embed.color = discord.Colour(16777215)
            xpRequis = bot.D.get_level(player["niveau"]+1)["exp_requis"]
            msg = f">>> Niveau : **{str(player['niveau'])}**\nXp :  **{str(player['xp'])}**/{str(xpRequis)}\n"
            msg += f"Victoires : **{str(nombre_vic)}**\n"
            
            totaux_skins = bot.D.get_total_skins()
            
            totaux_chromas = bot.D.get_total_chromas()
            
            msg += f"Skins : **{str(totaux_skins_joueur)}**/{str(totaux_skins)}\n"
            msg += f"Chromas : **{str(totaux_chromas_joueur)}**/{str(totaux_chromas)}\n"
            msg += f"Daily : **{time_daily}**\n"
            msg += f"Hourly : **{time_hourly}**\n"
            embed.description = msg
            if not player["name_lol"]:
                msg =f"Non lié"
            else:
                msg =f"{player['name_lol']}"
            embed.add_field(name="Compte Lol", value=msg)
            await interaction.followup.send(embed=embed)
        else:
            if autre:
                embed = bot.create_embed_missing_joueur(joueur.display_name)
            else:
                embed = bot.create_embed_missing_joueur(interaction.user.display_name)
            await interaction.followup.send(embed=embed)
