import os

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='/')
bot.description = "DM Bot: Playing Joust"


@bot.event
async def on_ready():
    print(f'[•] Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game('Joust'))
    print(f'[•] {bot.description}')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=999):
    await ctx.channel.purge(limit=amount+1)


bot.load_extension('cogs.Dice')
bot.load_extension('cogs.Joust')
bot.run(os.getenv('TOKEN'))
