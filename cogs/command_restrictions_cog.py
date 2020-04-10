import discord
from discord import Guild, TextChannel
from discord.ext.commands import Cog, Bot, Context, command, Command


class CommandRestrictionsCog(Cog):
    COMMAND_RESTRICTION_NAME = "command-restriction"

    def __init__(self, bot: Bot):
        self.bot = bot
        self.retrieve_restrictions()

    def retrieve_restrictions(self):
        # TODO database
        pass

    @command(name="restrict")
    async def restrict_command(self, context: Context, command_name: str, channel_to_restrict: TextChannel):
        command_to_restrict: Command = discord.utils.find(lambda cmd: cmd.name == command_name, self.bot.commands)
        if not command_to_restrict:
            await context.send(f"The command `{command_name}` does not exist.")
            return

        if not hasattr(command_to_restrict, self.COMMAND_RESTRICTION_NAME):
            print(f"Adding new attribute for command {command_name}")
            command_to_restrict.__setattr__(self.COMMAND_RESTRICTION_NAME, {channel_to_restrict})
            command_to_restrict.add_check(self.verify_channel_restrictions)
        else:
            print(f"Adding new channel {channel_to_restrict.name} to attr")
            command_to_restrict.__getattribute__(self.COMMAND_RESTRICTION_NAME).add(channel_to_restrict)
        print(context.guild.text_channels)
        print(channel_to_restrict)

    @staticmethod
    def verify_channel_restrictions(context: Context):
        return not hasattr(context.command, CommandRestrictionsCog.COMMAND_RESTRICTION_NAME) or \
               context.channel not in getattr(context.command, CommandRestrictionsCog.COMMAND_RESTRICTION_NAME)


def setup(bot: Bot):
    bot.add_cog(CommandRestrictionsCog(bot))
