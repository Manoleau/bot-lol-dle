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
    @bot.tree.command(name="guess-item", description="Trouve l'item")
    @app_commands.describe(difficulte = "Quelle difficulté ?")
    @app_commands.choices(difficulte=[
        discord.app_commands.Choice(name="Facile", value="facile"),
        discord.app_commands.Choice(name="Difficile", value="difficile")
    ])
    async def guessitem(interaction: discord.Interaction, difficulte: discord.app_commands.Choice[str]):
        await interaction.response.defer()
        if bot.update:
            await interaction.followup.send("Mise à jour du bot en cours... veillez réessayer plus tard.")
        else:
            channelId = str(interaction.channel_id)
            guildId = str(interaction.guild_id)
            typeJeu = "item"
            res = bot.D.get_game_by_channel_and_guild(channelId, guildId, False)
            embed = discord.Embed()
            if res is None:
                embed.color = discord.Colour(0x425b8a)
                logo_lol = discord.File(assets["LoL"]["image-location"], filename=assets["LoL"]["image"])
                embed.set_footer(text="Version : "+bot.versionAc, icon_url="attachment://"+assets["LoL"]["image"])
                if difficulte.value == "facile":
                    item = bot.D.get_random_item()
                    mot = item["name"].replace("œ","oe")
                    embed.description = "*nom de l'item complet uniquement*"
                    embed.set_author(name="Quel est le nom de cet item ?")
                    embed.set_image(url=item["image"])
                else:
                    item = bot.D.get_random_item()
                    mot = item["name"].replace("œ","oe")
                    embed.add_field(name="Quel est l'item qui correspond a cette description ?", value=item["description"])
                bot.D.add_game(channelId, guildId, typeJeu, mot, difficulte.value)
                await interaction.followup.send(embed=embed, file=logo_lol)
                gameId = bot.D.get_game_id(channelId, guildId, False)
                await bot.D.timer_indice(interaction=interaction, gameId=gameId, typeJeu=typeJeu, channelId=channelId, guildId=guildId, mot=mot)
            else:
                embed.description = "Une partie est déjà en cours dans ce channel..."
                await interaction.followup.send(embed=embed)

