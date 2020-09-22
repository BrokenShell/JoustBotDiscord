import os
import pickle

from Fortuna import shuffle
from discord.ext import commands
from joust.knights import Knight, joust, get_name, open_knight, save_knight


class Joust(commands.Cog):
    """ Joust: Created by Broken """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def story(self, ctx, *, background):
        """ Edit the background story of your Knight
        /story <your background story>
        """
        player = get_name(ctx.author)
        character = open_knight(player)
        character.background = background
        save_knight(character, player)

    @commands.command()
    async def create(self, ctx, *, name):
        """ Create your Knight """
        player = get_name(ctx.author)
        path = './characters/'
        file = f'{player}.joust'
        if file not in os.listdir(path):
            character = Knight(name=name)
            pickle.dump(character, open(path + file, 'wb'))
            await ctx.send(character)
            print(f'[!] Created {character.name} for {player}')
        else:
            await ctx.send('You must first `/delete` your current knight.')

    @commands.command()
    async def delete(self, ctx):
        """ Delete your Knight """
        player = get_name(ctx.author)
        try:
            character = pickle.load(open(f'./characters/{player}.joust', 'rb'))
            if character.rank < 10:
                os.remove(f'./characters/{player}.joust')
            else:
                await ctx.send('You do not have permission to delete this knight.')
        except FileNotFoundError:
            pass

    @commands.command()
    async def detail(self, ctx):
        """ Display your Knight's details """
        try:
            player = get_name(ctx.author)
            character = pickle.load(open(f'./characters/{player}.joust', 'rb'))
            await ctx.send(f"{get_name(ctx.author)}'s {character.title}:\n{character.details()}")
        except FileNotFoundError:
            pass

    @commands.command()
    async def list(self, ctx):
        """ View list of active Knights """
        names = []
        for file_name in os.listdir('./characters/'):
            if file_name.endswith('.joust'):
                character = pickle.load(open(f'./characters/{file_name}', 'rb'))
                names.append(f'{character.name}, Rank: {character.rank} {character.title}')
        await ctx.send('\n'.join(names))

    @commands.command()
    async def view(self, ctx, *, player=None):
        """ View a Knight's summary by name """
        if not player:
            player = get_name(ctx.author)
        try:
            character = pickle.load(open(f'./characters/{player}.joust', 'rb'))
            await ctx.send(character)
        except FileNotFoundError:
            pass

    @commands.command()
    async def equip(self, ctx, *, item):
        """ Equip an item from your War Chest by name """
        player = get_name(ctx.author)
        character = pickle.load(open(f'./characters/{player}.joust', 'rb'))
        character.equip(item)
        pickle.dump(character, open(f'./characters/{player}.joust', 'wb'))
        await ctx.send(f'{character.name} equips a new weapon: {character.weapon}')

    @commands.command()
    async def joust(self, ctx, *, opponent):
        """ Challenge an opponent to joust """
        player = get_name(ctx.author)
        attacker = pickle.load(open(f'./characters/{player}.joust', 'rb'))
        if attacker.gold >= 10:
            try:
                defender = pickle.load(open(f'./characters/{opponent}.joust', 'rb'))
                # print(f'[•] {attacker.name} Jousting {defender.name}')
                attacker.gold -= 10
                result = joust(attacker, defender)
                # pickle.dump(attacker, open(f'./characters/{player}.joust', 'wb'))
                # pickle.dump(defender, open(f'./characters/{opponent}.joust', 'wb'))
                # print(f'\t[-] {result}')
                await ctx.send(result)
            except FileNotFoundError:
                pass
        else:
            await ctx.send('You must have 10 gold to participate in the tournaments!')

    @commands.command()
    async def tournament(self, ctx):
        """ Single Elimination Jousting Tournament """
        knight_list = []
        for file_name in os.listdir('./characters/'):
            if file_name.endswith('.joust'):
                knight_list.append(pickle.load(open(f'./characters/{file_name}', 'rb')))
        shuffle(knight_list)
        pivot = len(knight_list) // 2
        bracket = zip(knight_list[:pivot], knight_list[pivot:])
        for pair in bracket:
            await ctx.send(joust(*pair))


def setup(bot):
    bot.add_cog(Joust(bot))
    print('[•] Joust Loaded')
