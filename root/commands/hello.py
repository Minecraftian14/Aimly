import typing
from discord.ext import commands
from discord import User, errors, DMChannel


class Greet(commands.Cog, name='Greet'):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return True


    @commands.command(
        name='greet',
        hidden=True,
    )
    async def purge(self, ctx):
        channel = ctx.message.channel
        await ctx.message.delete()
        await channel.send('o m g...')
        return True


def setup(client):
    client.add_cog(Greet(client))