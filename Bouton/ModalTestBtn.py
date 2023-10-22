import discord
from discord.ui import Select, View, Button
from Modal.ModalTest import ModalTest
class AfficheModal(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Afficher la Modal", style=discord.ButtonStyle.primary)
    async def afficheModalBtn(self, interaction:discord.Interaction, button:Button):
        await interaction.response.send_modal(ModalTest(title="Modal Test", custom_id="test"))