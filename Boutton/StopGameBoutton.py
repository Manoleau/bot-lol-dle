import discord
from discord.ui import Select, View, Button
from Boutton.RejouerItemChampionBoutton import Rejouer
class StopGame(View):
    def __init__(self, DB, id_jeu:int, message_id:int, typeJeu:str, mot:str):
        super().__init__()
        self.DB = DB
        self.id_jeu = id_jeu
        self.message_id = message_id
        self.typeJeu = typeJeu
        self.mot = mot

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stopBtn(self, interaction:discord.Interaction, button:Button):
        message_indice = await interaction.channel.fetch_message(self.message_id)
        await message_indice.delete()
        self.DB.cursor.execute("SELECT difficulte FROM Jeu WHERE id = ?", (self.id_jeu,))
        difficulte= self.DB.cursor.fetchone()[0]
        self.DB.cursor.execute("DELETE FROM Jeu WHERE id = ?;", (self.id_jeu,))
        self.DB.conn.commit()
        embed = discord.Embed()
        embed.set_author(name="Fin de partie")
        if self.typeJeu == "item":
            embed.set_image(url=self.DB.get_item_image_by_name(self.mot))
            embed.description = "L'item était : "+self.mot
        elif self.typeJeu == "champion":
            embed.set_image(url=self.DB.get_champion_splash_by_name(self.mot))
            embed.description = "Le champion était : "+self.mot
        await interaction.channel.send(embed=embed, view=Rejouer(self.DB, self.typeJeu, difficulte))