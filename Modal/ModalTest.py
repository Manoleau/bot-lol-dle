from typing import Optional
import discord
from discord.ui import Select, View, Button, Modal, TextInput
from discord.utils import MISSING

class ModalTest(Modal):
    def __init__(self, *, title: str = ..., timeout: float | None = None, custom_id: str = ...) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
    
    demande = TextInput(label="Ecrie un truc", style=discord.TextStyle.short, placeholder="zizi", default="", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(description=f"**{self.demande.label}**\n{self.demande}")
        embed.set_author(name=interaction.user,icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=embed)