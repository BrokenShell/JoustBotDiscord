import os
from bot import bot

bot.load_extension('cogs.Dice')
bot.load_extension('cogs.Joust')
bot.run(os.getenv('TOKEN'))
