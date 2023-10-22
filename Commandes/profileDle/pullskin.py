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
    @bot.tree.command(name="pull-skin", description="Pull un skin, coût : 50 golds")
    @app_commands.describe(mode = "mode du pull")
    @app_commands.choices(mode=[
        discord.app_commands.Choice(name="Single", value=1),
        discord.app_commands.Choice(name="Ten", value=10)
    ])
    async def pullskin(interaction: discord.Interaction, mode: discord.app_commands.Choice[int]):
        await interaction.response.defer()
        gold = bot.D.get_joueur_gold_by_id(interaction.user.id)
        if gold == None:
            bot.D.insert_joueur_in_db(interaction.user.id, interaction.user.name)
            gold = bot.D.get_joueur_gold_by_id(interaction.user.id)
        if gold != None:
            if mode.value * 50 <= gold:
                if mode.value == 1:
                    skin = bot.D.tirage_skin(interaction.user.id, mode.value, mode.value*50)[0]
                    if skin:
                        if skin[0] == 1:
                            bot.D.cursor.execute("INSERT INTO JoueurSkins VALUES(?, ?, ?, 1)", (interaction.user.id,skin[2]["id"], skin[1]))
                        else:
                            bot.D.cursor.execute("UPDATE JoueurSkins SET quantite = ? WHERE joueurId = ? AND id_thing = ?;",(skin[0], interaction.user.id, skin[2]["id"]))
                        bot.D.conn.commit()
                        color_hex = skin[3]['couleur']
                        embed_color = int(color_hex[1:], 16)
                        embed = discord.Embed(
                            title="Résultat du tirage",
                            description= skin[2]["name"],
                            color=discord.Colour(embed_color)
                        )
                        embed.set_thumbnail(url=skin[3]['image'])
                        embed.set_image(url=skin[2]["splashPath"])
                    else:
                        embed = discord.Embed(
                            title=":x:",
                            description= "vous avez atteint le nombre maximum de pull",
                        )
                else:
                    best = 1
                    best_skin = None
                    skins = bot.D.tirage_skin(interaction.user.id, mode.value, mode.value*50)
                    if skins:
                        msg = ">>> "
                        for skin in skins:
                            if best >= skin[3]['proba']:
                                best = skin[3]['proba']
                                best_skin = skin
                            if skin[0] == 1:
                                bot.D.cursor.execute("INSERT INTO JoueurSkins VALUES(?, ?, ?, 1)", (interaction.user.id,skin[2]["id"], skin[1]))
                            else:
                                bot.D.cursor.execute("UPDATE JoueurSkins SET quantite = ? WHERE joueurId = ? AND id_thing = ?;",(skin[0], interaction.user.id, skin[2]["id"]))
                            bot.D.conn.commit()
                            msg += f"{skin[3]['emoji']} {skin[2]['name']}\n"
                        
                        color_hex = best_skin[3]['couleur']
                        embed_color = int(color_hex[1:], 16)
                        embed = discord.Embed(
                            title="Résultat du tirage",
                            description= msg,
                            color=discord.Colour(embed_color)
                        )
                        embed.set_image(url=best_skin[2]["splashPath"])
                    else:
                        embed = discord.Embed(
                            title=":x:",
                            description= "vous avez atteint le nombre maximum de pull",
                        )
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f":x: {bot.getGoldsEmoji()} golds insuffisant",
                    description= f"**{str(gold)}**/{str(mode.value * 50)}",
                )
                await interaction.followup.send(embed=embed)
