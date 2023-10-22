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
    @bot.tree.command(name="my-skin", description="montre la quantité de skin que vous avez")
    @app_commands.describe(rarity = "Rareté du skin")
    @app_commands.choices(rarity=[
        discord.app_commands.Choice(name="Normal", value="Normal"),
        discord.app_commands.Choice(name="Epique", value="Epique"),
        discord.app_commands.Choice(name="Hextech", value="Hextech"),
        discord.app_commands.Choice(name="Légendaire", value="Légendaire"),
        discord.app_commands.Choice(name="Ultime", value="Ultime")
    ])
    async def myskin(interaction: discord.Interaction, rarity:discord.app_commands.Choice[str] = None):
        await interaction.response.defer()
        if rarity:
            skins = bot.D.get_all_skins_of(interaction.user.id, rarity.value)
            rarete = bot.D.get_rarity(rarity.value)
            color_hex = rarete['couleur']
            embed_color = int(color_hex[1:], 16)
            if skins and len(skins) != 0:
                embed = discord.Embed(
                    color=embed_color,
                    title=f"Tous les skins {rarity.value} de {interaction.user.display_name}"
                )
                embed.set_thumbnail(url=rarete['image'])
                msg = ">>> "
                longueur = len(skins)
                i = 0
                while i < 15 and i < longueur:
                    if skins[i]['hasChroma']:
                        msg += f"{skins[i]['name']}, <:Chroma:1164661178883125339> :white_check_mark:\n"
                    else:
                        msg += f"{skins[i]['name']}, <:Chroma:1164661178883125339> :x:\n"
                    i += 1
                embed.description = msg
                nb_page = int(longueur/15)+1
                embed.set_footer(text=f"{1}/{nb_page}")
                await interaction.followup.send(embed=embed, view=bot.pageBtn(bot, embed, nb_page, interaction.user.display_name, skins, interaction.user.display_name))
            else:
                embed = discord.Embed(
                    color=embed_color,
                    title=f"{interaction.user.display_name} n'a pas de skin {rarity.value}",
                )
        else:
            skins = bot.D.get_all_skins_of(interaction.user.id)
            color_hex = "#ffffff"
            embed_color = int(color_hex[1:], 16)
            if skins and len(skins) != 0:
                embed = discord.Embed(
                    color=embed_color,
                    title=f"Tous les skins de {interaction.user.display_name}"
                )
                METTRE LE NOMBRE RESTANT DE SKIN
                rareteAc = skins[0]['rarity']
                longueur = len(skins)
                msg = f"{bot.D.get_rarity(rareteAc)['emoji']}\n"
                i = 0
                while i < 15 and i < longueur:
                    if skins[i]['rarity'] != rareteAc:
                        rareteAc = skins[i]['rarity']
                        msg += f"{bot.D.get_rarity(rareteAc)['emoji']}\n"
                    if skins[i]['hasChroma']:
                        msg += f"> {skins[i]['name']}, <:Chroma:1164661178883125339> :white_check_mark:\n"
                    else:
                        msg += f"> {skins[i]['name']}, <:Chroma:1164661178883125339> :x:\n"
                    i += 1
                embed.description = msg
                nb_page = int(longueur/15)+1
                embed.set_footer(text=f"{1}/{nb_page}")
                await interaction.followup.send(embed=embed, view=bot.pageBtn(bot, embed, nb_page, interaction.user.display_name, skins, interaction.user.display_name, rareteAc))
            else:
                embed = discord.Embed(
                    color=embed_color,
                    title=f"{interaction.user.display_name} n'a pas de skin.",
                )

        # else:
        #     await interaction.followup.send(f"{interaction.user.mention}, vous n'avez pas encore jouer.")
