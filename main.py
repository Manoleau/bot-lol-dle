import settings
from initBot import LeagueDleBot

bot = LeagueDleBot()

if __name__ == "__main__":
    bot.run(settings.DISCORD_API_SECRET)