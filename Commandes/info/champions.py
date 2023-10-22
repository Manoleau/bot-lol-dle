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
    @bot.tree.command(name="champions", description="Affiche tous les champions, si un item est séléctionné alors on affiche ")
    @app_commands.describe(lettre = "Une lettre ou un début de mot")
    async def champions(interaction: discord.Interaction, lettre:str):
        await interaction.response.defer()
        if bot.update:
            await interaction.followup.send("Mise à jour du bot en cours... veillez réessayer plus tard.")
        else:
            embed = discord.Embed()
            if lettre:
                lettre = lettre.upper()
                champions_info = bot.D.get_all_champions_in_list_start_with(lettre)
                if champions_info:
                    if len(champions_info) == 1:
                        champion = champions_info[0]
                        logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
                        embed.set_footer(text="Version : "+bot.versionAc, icon_url="attachment://"+assets["LoL"]["image"])
                        embed.set_author(name=champion["name"])
                        embed.set_thumbnail(url=champion["image"])
                        embed.description = champion["title"]
                        embed.set_image(url=champion["splash_art"])
                        roles = bot.D.get_roles_champion_by_id(champion["id"])
                        msg_roles = ""
                        for role in roles:
                            msg_roles += f"{role['name']}\n"
                        embed.add_field(name="Genre", value=champion["genre"])
                        embed.add_field(name="Ressource", value=champion["ressource"])
                        embed.add_field(name="Année de sortie", value=str(champion["annee_sortie"]))
                        embed.add_field(name="Role(s)", value=msg_roles)
                        embed.add_field(name="Portée", value=champion["porte"])
                        await interaction.followup.send(embed=embed, file=logo_lol)
                    else:
                        logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
                        embed.set_footer(text="Version : "+bot.versionAc, icon_url="attachment://"+assets["LoL"]["image"])
                        embed.set_author(name="Champions commençant par "+lettre)
                        msg = ""
                        nb_lettres = 0
                        for champion_info in champions_info:
                            emoji = bot.D.get_emoji(str(champion_info["id"]))
                            tmp = f"<:{emoji['nom_emoji']}:{emoji['id']}> {champion_info['name']}\n"
                            msg += tmp
                            nb_lettres += len(tmp)
                            if nb_lettres >= 950:
                                nb_lettres = 0
                                embed.add_field(name="\u200b", value=msg)
                                msg = ""
                        if msg != "":
                            embed.add_field(name="\u200b", value=msg)
                        await interaction.followup.send(embed=embed, file=logo_lol, view=bot.champView(bot.D,champions_info))
                else:
                    await interaction.followup.send("Aucun champion n'a été trouvé", ephemeral=True)

