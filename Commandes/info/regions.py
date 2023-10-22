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
    @bot.tree.command(name="region", description="Affiche tous les champions, si un item est séléctionné alors on affiche ")
    @app_commands.describe(nom = "Nom de la région")
    @app_commands.choices(nom=[
        discord.app_commands.Choice(name="Ionia", value="Ionia"),
        discord.app_commands.Choice(name="Bandle", value="Bandle"),
        discord.app_commands.Choice(name="Bilgewater", value="Bilgewater"),
        discord.app_commands.Choice(name="Demacia", value="Demacia"),
        discord.app_commands.Choice(name="Freljord", value="Freljord"),
        discord.app_commands.Choice(name="Ixtal", value="Ixtal"),
        discord.app_commands.Choice(name="Néant", value="Néant"),
        discord.app_commands.Choice(name="Noxus", value="Noxus"),
        discord.app_commands.Choice(name="Piltover", value="Piltover"),
        discord.app_commands.Choice(name="Shurima", value="Shurima"),
        discord.app_commands.Choice(name="Targon", value="Targon"),
        discord.app_commands.Choice(name="Zaun", value="Zaun"),
        discord.app_commands.Choice(name="Iles Obscures", value="Iles Obscures")
    ])
    async def region(interaction: discord.Interaction, nom: discord.app_commands.Choice[str] = None):
        await interaction.response.defer()
        if bot.update:
            await interaction.followup.send("Mise à jour du bot en cours... veillez réessayer plus tard.")
        else:
            embed = discord.Embed()
            if nom:
                region = bot.D.get_region_by_name(nom.value)
                if region:
                    embed.set_author(name=region["name"])
                    embed.set_thumbnail(url=region["logo"])
                    embed.set_image(url=region["splash"])
                    region["description"] = region["description"].replace("\n", "\n\n")
                    if len(region["description"]) >= 1024:
                        if "\n" in region["description"]:
                            espace = False
                            description = region["description"].split("\n")
                        else:
                            espace = True
                            description = region["description"].split(" ")
                        msg = ""
                        for partie_desc in description:
                            tmp = msg
                            if espace:
                                msg += partie_desc + " "
                            else:
                                msg += partie_desc + "\n"
                            if len(msg) >= 1024:
                                
                                embed.add_field(name="Histoire", value=tmp, inline=False)
                                if espace:
                                    msg = partie_desc + " "
                                else:
                                    msg = partie_desc + "\n"
                        embed.add_field(name="\u200b", value=msg, inline=False)

                    else:
                        embed.add_field(name="Histoire", value=region["description"], inline=False)
            else:
                msg = ""
                regions = bot.D.get_all_regions()
                for region in regions:
                    emoji = bot.D.get_emoji(str(region['id']))
                    msg += f"<:{emoji['nom_emoji']}:{emoji['id']}> {region['name']}\n"
                embed.add_field(name="Régions", value=msg)
            await interaction.followup.send(embed=embed)

