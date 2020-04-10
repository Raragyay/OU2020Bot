from typing import OrderedDict

import discord
from discord import Message, TextChannel
from discord.ext.commands import Command, Cog, command, Bot, Context


class TestCog(Cog):
    def __init__(self, bot: Bot):
        self.a = 3
        self.bot = bot

    @command(name='test')
    async def test(self, context: Context):
        await context.send(str(self.a))
        await context.send("test received! hi (:")

    @command(name="getcmd")
    async def get_cmd(self, context: Context):
        for command in self.bot.commands:
            command: Command
            await context.send(command.name)

    @command(name="restrict")
    async def restrict_command(self, context: Context, command_name: str, channel_name: TextChannel):
        await context.send(f"Got an order to restrict command {command_name}!")
        await context.send(f"We will try to restrict in the channel {channel_name.name}.")
        print(channel_name)
        command_to_restrict: Command = discord.utils.find(lambda cmd: cmd.name == command_name, self.bot.commands)
        if not command_to_restrict:
            await context.send(f"I couldn't find a command by the name {command_name}... :(")
            return
        await context.send(f"I am now going to restrict the command {command_to_restrict.name}...")
        k = "channel_restrictions"
        print(command_to_restrict.__dir__())
        if not hasattr(command_to_restrict,"channel_restrictions"):  # TODO move raw text out
            await context.send(f"Channel restrictions were not found for this channel. Creating new restrictions.")
            command_to_restrict.__setattr__("channel_restrictions", {channel_name.name})
        else:
            await context.send(f"Channel restrictions were found. Here are the previous restrictions: "
                               f"{getattr(command_to_restrict,k)}")
            command_to_restrict.__getattribute__("channel_restrictions").add(channel_name.name)
        print(command_to_restrict.__dir__())


def setup(bot: Bot):
    bot.add_cog(TestCog(bot))
