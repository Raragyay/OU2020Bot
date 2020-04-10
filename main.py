from typing import List, Type

from discord.ext import commands
from discord.ext.commands import Bot, command, Context, Cog

from client import OU2020Bot
from cogs.test_cog import TestCog


def retrieve_token():
    return open("token.txt", "r").read().strip()


def load_cogs(bot: Bot, cogs_to_add: List[Type[Cog]]):
    for cog in cogs_to_add:
        cog_extension = cog.__module__
        bot.load_extension(cog_extension)


command_prefix = "$"
cogs = [TestCog]

client = Bot(command_prefix=command_prefix)
load_cogs(client, cogs)
#
#
# @commands.has_role("Moderator")
# @client.command(name='test')
# async def test(context: Context):
#     await context.send("test received! hi (:")
# client = OU2020Bot(command_prefix)
client.run(retrieve_token())
