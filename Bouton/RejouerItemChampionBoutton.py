import discord
from discord.ui import Select, View, Button

class Rejouer(View):
    def __init__(self, bot, mode:str, difficulte:str):
        super().__init__()
        self.bot = bot
        self.DB = bot.D
        self.mode = mode
        self.difficulte = difficulte
        self.assets = {
                    "LoL" : {
                        "name" : "LeagueLogo",
                        "image-location": "assets/logo/LeagueLogo.png",
                        "image" : "LeagueLogo.png"
                    }
                }


    @discord.ui.button(label="Rejouer", style=discord.ButtonStyle.green)
    async def rejouerBtn(self, interaction:discord.Interaction, button:Button):
        await interaction.response.defer()
    
        channelId = str(interaction.channel_id)
        guildId = str(interaction.guild_id)
        typeJeu = self.mode
        
        res = self.DB.get_game_by_channel_and_guild(channelId, guildId, False)

        embed = discord.Embed()
        
        if res is None:
            embed.color = discord.Colour(0x425b8a)
            logo_lol = discord.File(self.assets["LoL"]["image-location"], filename=self.assets["LoL"]["image"])
            embed.set_footer(text="Version : "+self.bot.versionAc, icon_url="attachment://"+self.assets["LoL"]["image"])
            if self.difficulte == "facile":
                if typeJeu == "champion":
                    champion = self.DB.get_random_champion()
                    mot = champion["name"]
                    embed.set_author(name="Qui est ce champion ?")
                    embed.set_image(url=champion["image"])
                elif typeJeu == "item":
                    item = self.DB.get_random_item()
                    mot = item["name"].replace("œ","oe")
                    embed.description = "*nom de l'item complet uniquement*"
                    embed.set_author(name="Quel est le nom de cet item ?")
                    embed.set_image(url=item["image"])
            else:
                if typeJeu == "champion":
                    champion = self.DB.get_random_champion()
                    mot = champion["name"]
                    embed.add_field(name="Quel est le champion qui a ce titre ?", value="\u200b\n**"+champion["title"]+"**\n\u200b")
                elif typeJeu == "item":
                    item = self.DB.get_random_item()
                    mot = item["name"].replace("œ","oe")
                    embed.add_field(name="Quel est l'item qui correspond a cette description ?", value=item["description"])
            self.DB.add_game(channelId, guildId, typeJeu, mot, self.difficulte)
            await interaction.followup.send(embed=embed, file=logo_lol)
            gameId = self.DB.get_game_id(channelId, guildId, False)
            await self.DB.timer_indice(interaction=interaction, gameId=gameId, typeJeu=typeJeu, channelId=channelId, guildId=guildId, mot=mot)
            
        else:
            embed.description = "Une partie est déjà en cours dans de channel..."
            await interaction.followup.send(embed=embed)