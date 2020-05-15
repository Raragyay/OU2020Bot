import random
from typing import OrderedDict

import discord
from discord import Message, Role, TextChannel, utils
from discord.ext import commands
from discord.ext.commands import Command, Cog, command, Bot, Context, check


class TestCog(Cog):
    def __init__(self, bot: Bot):
        self.a = 3
        self.bot = bot

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


def setup(bot: Bot):
    bot.add_cog(TestCog(bot))
