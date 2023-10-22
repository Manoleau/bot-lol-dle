import discord
from discord.ui import Select, View, Button


class Page(View):
    def __init__(self, bot, embed: discord.Embed, nb_page, username, skins_list, interaUser, rareteAc = None):
        super().__init__()
        self.bot = bot
        self.page = 1
        self.embed = embed
        self.nb_page = nb_page
        self.username = username
        self.skins = skins_list
        self.interaUser = interaUser
        self.rareteAc = rareteAc
        if (self.nb_page == 1):
            self.children[1].disabled = True

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary, disabled=True)
    async def beforepage(self, interaction: discord.Interaction, button: Button):
        if (interaction.user.display_name == self.interaUser):
            if (self.page != 1):
                self.page -= 1
                long = 15 + (15 * (self.page - 1))
                if (self.page == 1):
                    min = 0
                else:
                    min = 15 * (self.page - 1)
                i = min
                if not self.rareteAc:
                    desc = ">>> "
                    while i < long and i < len(self.skins):
                        if self.skins[i]['hasChroma']:
                            desc += f"{self.skins[i]['name']}, <:Chroma:1164661178883125339> :white_check_mark:\n"
                        else:
                            desc += f"{self.skins[i]['name']}, <:Chroma:1164661178883125339> :x:\n"
                        i+= 1
                else:
                    if self.skins[i]['rarity'] == self.rareteAc:
                        desc = f"{self.bot.D.get_rarity(self.rareteAc)['emoji']}\n"
                    else:
                        desc = ""
                    while i < long and i < len(self.skins):
                        if self.skins[i]['rarity'] != self.rareteAc:
                            self.rareteAc = self.skins[i]['rarity']
                            desc += f"{self.bot.D.get_rarity(self.rareteAc)['emoji']}\n"
                        if self.skins[i]['hasChroma']:
                            desc += f"> {self.skins[i]['name']}, <:Chroma:1164661178883125339> :white_check_mark:\n"
                        else:
                            desc += f"> {self.skins[i]['name']}, <:Chroma:1164661178883125339> :x:\n"
                        i += 1
                self.embed.description = desc
                self.embed.set_footer(text=f"{self.page}/{self.nb_page}")
                button_after = self.children[1]
                button_after.disabled = False
                if (self.page == 1):
                    button.disabled = True
                await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def nextpage(self, interaction: discord.Interaction, button: Button):
        if (interaction.user.display_name == self.interaUser):
            if (self.page != self.nb_page):
                self.page += 1
                if (len(self.skins) < 10 * self.page):
                    long = len(self.skins) + (10 * (self.page - 1))
                else:
                    long = 15 + (15 * (self.page - 1))
                min = 15 * (self.page - 1)
                
                i = min
                if not self.rareteAc:
                    desc = ">>> "
                    while i < long and i < len(self.skins):
                        if self.skins[i]['hasChroma']:
                            desc += f"{self.skins[i]['name']}, <:Chroma:1164661178883125339> :white_check_mark:\n"
                        else:
                            desc += f"{self.skins[i]['name']}, <:Chroma:1164661178883125339> :x:\n"
                        i+= 1
                else:
                    if self.skins[i]['rarity'] == self.rareteAc:
                        desc = f"{self.bot.D.get_rarity(self.rareteAc)['emoji']}\n"
                    else:
                        desc = ""
                    while i < long and i < len(self.skins):
                        if self.skins[i]['rarity'] != self.rareteAc:
                            self.rareteAc = self.skins[i]['rarity']
                            desc += f"{self.bot.D.get_rarity(self.rareteAc)['emoji']}\n"
                        if self.skins[i]['hasChroma']:
                            desc += f"> {self.skins[i]['name']}, <:Chroma:1164661178883125339> :white_check_mark:\n"
                        else:
                            desc += f"> {self.skins[i]['name']}, <:Chroma:1164661178883125339> :x:\n"
                        i += 1
                self.embed.description = desc
                self.embed.set_footer(text=f"{self.page}/{self.nb_page}")
                button_before = self.children[0]
                button_before.disabled = False
                if (self.page == self.nb_page):
                    button.disabled = True
                await interaction.response.edit_message(embed=self.embed, view=self)