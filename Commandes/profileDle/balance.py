import discord
from discord.ext import commands
from discord import app_commands
assets = {
    "LoL" : {
        "name" : "LeagueLogo",
        "image-location": "assets/logo/LeagueLogo.png",
        "image" : "LeagueLogo.png"
    }
}
# from initBot import LeagueDleBot
def get(bot):
    @bot.tree.command(name="balance", description="Montre votre balance")
    async def balance(interaction: discord.Interaction):
        await interaction.response.defer()
        gold = bot.D.get_joueur_gold_by_id(interaction.user.id)
        if gold == None:
            bot.D.insert_joueur_in_db(interaction.user.id, interaction.user.name)
            gold = bot.D.get_joueur_gold_by_id(interaction.user.id)
        if gold != None:
            embed = discord.Embed()
            embed.color = discord.Colour.purple()
            embed.title = f"Balance de {interaction.user.display_name}"
            embed.description = f"{bot.getGoldsEmoji()} Golds : **{gold}**"
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"{interaction.user.mention}, vous n'avez pas encore jouer.")
