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
    @bot.tree.command(name="niveau", description="Montre votre niveau")
    async def niveau(interaction: discord.Interaction):
        await interaction.response.defer()

        niv = bot.D.get_joueur_niv_by_id(interaction.user.id)
        if niv == None:
            bot.D.insert_joueur_in_db(interaction.user.id, interaction.user.name)
            niv = bot.D.get_joueur_gold_by_id(interaction.user.id)
        if niv != None:
            xp = bot.D.get_joueur_xp_by_id(interaction.user.id)
            xpRequis = bot.D.get_level(niv+1)["exp_requis"]
            embed = discord.Embed()
                # color_hex = "#D33528"
                # embed_color = int(color_hex[1:], 16)
            embed.color = discord.Colour.purple()
            embed.title = f"Niveau de {interaction.user.display_name}"
            embed.description = f"{bot.getLvlUpEmoji()} Niveau : **{niv}**\n{bot.getXpEmoji()} avant le prochain niveau : **{str(xpRequis-xp)}**"
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.set_image(url="https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/samira/skins/skin30/animatedsplash/samira_skin30_centered.webm")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"{interaction.user.mention}, vous n'avez pas encore jouer.")
