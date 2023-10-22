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
def get(bot):
    @bot.tree.command(name="items", description="Affiche tous les items, si un item est séléctionné alors on affiche les stats")
    @app_commands.describe(item = "Nom de l'item")
    @app_commands.describe(lettre = "Une lettre")
    async def items(interaction: discord.Interaction, item: str = None, lettre:str = None):
        await interaction.response.defer()
        if bot.update:
            await interaction.followup.send("Mise à jour du bot en cours... veillez réessayer plus tard.")
        else:
            embed = discord.Embed()
            if item:
                item_info = bot.D.get_item_by_name(item)
                if item_info:
                    logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
                    embed.set_footer(text="Version : "+bot.versionAc, icon_url="attachment://"+assets["LoL"]["image"])
                    embed.set_thumbnail(url=item_info["image"])
                    embed.set_author(name=item)
                    embed.add_field(name="Description/Stats", value=item_info["description"],inline=False)
                    await interaction.followup.send(embed=embed, file=logo_lol)
                else:
                    embed = bot.create_embed_missing_item(item)
                    lettre = item[0].upper()
                    embed.description += "\nFaites /items lettre: "+lettre
                    await interaction.followup.send(embed=embed)            
            elif lettre:
                lettre = lettre.upper()
                items_info = bot.D.get_all_items_in_list_start_with(lettre)
                if items_info:
                    logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
                    embed.set_footer(text="Version : "+bot.versionAc, icon_url="attachment://"+assets["LoL"]["image"])
                    embed.set_author(name="Items commençant par "+lettre)
                    msg = ""
                    nb_lettres = 0
                    for item_info in items_info:
                        emoji = bot.D.get_emoji(str(item_info["id"]))
                        tmp = f"<:{emoji['nom_emoji']}:{emoji['id']}> {item_info['name']}\n"
                        msg += tmp
                        nb_lettres += len(tmp)
                        if nb_lettres >= 950:
                            nb_lettres = 0
                            embed.add_field(name="\u200b", value=msg)
                            msg = ""
                    if msg != "":
                        embed.add_field(name="\u200b", value=msg)
                    await interaction.followup.send(embed=embed, file=logo_lol)
                else:
                    await interaction.followup.send("Veillez entrer une lettre correct !")
            else:
                await interaction.followup.send(content="Veillez entrer une lettre ou un nom d'item !")

