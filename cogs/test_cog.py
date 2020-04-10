from typing import OrderedDict

import discord
from discord import Message, TextChannel, client, abc, Member
from discord.abc import User
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
        for cmd in self.bot.commands:
            cmd: Command
            await context.send(cmd.name)

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        elif message.content == "test input":
            await message.channel.send("test input")



def setup(bot: Bot):
    bot.add_cog(TestCog(bot))
