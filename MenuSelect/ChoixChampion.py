
from typing import Any
import discord
from discord.ui import View, Select, select
assets = {
    "LoL" : {
        "name" : "League of Legends",
        "image-location": "assets/logo/League-of-Legends.png",
        "image" : "League-of-Legends.png"
    }
}

class ChampSelect(Select):
    def __init__(self, db, liste_champions:list) -> None:
        super().__init__(placeholder="Choisissez un champion", options=[discord.SelectOption(label=champion["name"], value=champion["name"]) for champion in liste_champions])
        self.db = db
        self.champion_name = None
        self.message = None

    async def callback(self, interaction: discord.Interaction) -> Any:
            self.champion_name = self.values[0]
            champion_info = self.db.get_champion_by_name(self.champion_name)
            print(champion_info)

            embed = discord.Embed()
            embed.set_footer(text="Version : "+self.db.versionLol, icon_url="attachment://"+assets["LoL"]["image"])
            embed.set_author(name=self.champion_name)
            embed.set_thumbnail(url=champion_info["image"])
            embed.description = champion_info["title"]
            embed.set_image(url=champion_info["splash_art"])
            roles = self.db.get_roles_champion_by_id(champion_info["id"])
            msg_roles = ""
            for role in roles:
                msg_roles += f"{role['name']}\n"
            embed.add_field(name="Genre", value=champion_info["genre"])
            embed.add_field(name="Ressource", value=champion_info["ressource"])
            embed.add_field(name="Année de sortie", value=str(champion_info["annee_sortie"]))
            embed.add_field(name="Role(s)", value=msg_roles)
            embed.add_field(name="Portée", value=champion_info["porte"])
            await interaction.response.edit_message(embed=embed)

class ChampView(View):
    ""
    def __init__(self, db, liste_champions:list):
        super().__init__()
        self.add_item(ChampSelect(db, liste_champions))

        
