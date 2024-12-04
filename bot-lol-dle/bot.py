import discord
from discord.ext import commands
import services.media as media_service
class Bot(commands.Bot):
    def __init__(self)-> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.commandes = None
    async def setup_hook(self) -> None:
        try:
            self.tree.clear_commands(guild=None)
            media_service.execute_get_commands()
            self.commandes = await self.tree.sync()
        except Exception as e:
            print(f"Erreur pendant l'enregistrement des commandes : {e}")

    async def on_ready(self) -> None:
        print('Le Bot ' + self.user.display_name + ' Est Prêt !')
        print(f"Synced {len(self.commandes)} command(s)")
