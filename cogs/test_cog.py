from typing import OrderedDict, List

import discord
from discord import Message, TextChannel, client, abc, Member, Reaction
from discord.abc import User
from discord.ext.commands import Command, Cog, command, Bot, Context


class TestCog(Cog):

    def __init__(self, bot: Bot):
        self.a = 3
        self.bot = bot
        self.question_storage = []

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
        elif message.content == "amrit op" or message.content == "Amrit op":
            await message.channel.send("Amrit Bad")

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if message.author.id == 549076734880776193:
            await message.channel.send("No more deleting letmein :rage:")
            await message.channel.send(">>> "+message.content)

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if before.author.id == 549076734880776193:
            await before.channel.send("No more editing either :flushed:")
            await before.channel.send(">>> "+before.content)

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: User):
        if user.id == 644959900132442136:
            await reaction.message.channel.send("Stop reacting to everything Shawn this isnt instagram")





def setup(bot: Bot):
    bot.add_cog(TestCog(bot))