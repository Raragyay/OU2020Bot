from typing import List, Type

from discord.ext.commands import Bot, Cog

from cogs.command_restrictions_cog import CommandRestrictionsCog
from cogs.error_cog import ErrorCog
from cogs.test_cog import TestCog


def retrieve_token():
    return open("token.txt", "r").read().strip()


def load_cogs(bot: Bot, cogs_to_add: List[Type[Cog]]):
    for cog in cogs_to_add:
        cog_extension: str = cog.__module__
        bot.load_extension(cog_extension)


command_prefix = "%"
cogs = [TestCog, CommandRestrictionsCog, ErrorCog]

client = Bot(command_prefix=command_prefix)
load_cogs(client, cogs)


@client.event
async def on_ready():
    print("ready")


client.run(retrieve_token())
