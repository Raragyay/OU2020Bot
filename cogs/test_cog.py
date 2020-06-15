import random

from discord import Message, Reaction
from discord import Role
from discord.abc import User
from discord.ext import commands
from discord.ext.commands import Command, Cog, command, Bot, Context


class TestCog(Cog):

    def __init__(self, bot: Bot):
        self.a = 3
        self.bot = bot
        self.question_storage = []

    @command(name='test')
    @commands.has_role("Moderator")
    async def test(self, context: Context):
        await context.send(str(self.a))
        await context.send("test received! hi (:")

    @command(name="getcmd")
    @commands.has_role("Moderator")
    async def get_cmd(self, context: Context):
        for cmd in self.bot.commands:
            cmd: Command
            await context.send(cmd.name)

    @command(name="machsrand")
    @commands.has_role("Moderator")
    async def rand_mac_hs(self, context: Context, num: int):
        assert num <= 20, context.send("Too many people!")
        people = filter(lambda user: 695383484092645426 in map(lambda role: role.id, user.roles), context.guild.members)
        chosen_people = random.sample(list(people), num)
        await context.send("\n".join(str(person) for person in chosen_people))

    @command(name="rolecount")
    # @commands.has_any_role("Moderator", "Admin")
    async def role_count(self, context: Context, *roles: Role):
        num_of_people = sum(1 for user in context.guild.members if all(role in user.roles for role in roles))
        await context.send(f'There {"is" if num_of_people == 1 else "are"} {num_of_people} '
                           f'{"person" if num_of_people == 1 else "people"} with the '
                           f'{"role" if len(roles) == 1 else "roles"} {", ".join(map(str, roles))}.')

    @command(name="rolecounttest")
    @commands.has_any_role("Moderator", "Admin")
    async def role_count1(self, context: Context, role: Role):
        print(type(role))
        print(role)
        await context.send(role)
        # num_of_people = sum(1 for user in context.guild.members if role in user.roles)
        # await context.send(f'There {"is" if num_of_people == 1 else "are"} {num_of_people} '
        #                    f'{"person" if num_of_people == 1 else "people"} with the '
        #                    f'role {role}.')

    # @Cog.listener()
    # async def on_message(self, message: Message):
    #     if message.author.bot:
    #         return
    #     elif message.content == "amrit op" or message.content == "Amrit op":
    #         await message.channel.send("Amrit Bad")
    #
    # @Cog.listener()
    # async def on_message_delete(self, message: Message):
    #     if message.author.id == 549076734880776193:
    #         await message.channel.send("No more deleting letmein :rage:")
    #         await message.channel.send(">>> "+message.content)
    #
    # @Cog.listener()
    # async def on_message_edit(self, before: Message, after: Message):
    #     if before.author.id == 549076734880776193:
    #         await before.channel.send("No more editing either :flushed:")
    #         await before.channel.send(">>> "+before.content)
    #
    # @Cog.listener()
    # async def on_reaction_add(self, reaction: Reaction, user: User):
    #     if user.id == 644959900132442136:
    #         await reaction.message.channel.send("Stop reacting to everything Shawn this isnt instagram")


def setup(bot: Bot):
    bot.add_cog(TestCog(bot))
