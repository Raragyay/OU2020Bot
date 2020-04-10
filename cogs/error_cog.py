from discord.ext.commands import Cog, Bot, Context, CommandError, MissingRequiredArgument, Command, BadArgument


class ErrorCog(Cog):
    def __init__(self):
        pass

    @Cog.listener()
    async def on_command_error(self, context: Context, error: CommandError):
        if isinstance(error, MissingRequiredArgument):
            return await self.process_missing_required_argument(context)
        elif isinstance(error, BadArgument):
            return await self.process_bad_argument(context, error)
        print(type(error))
        print(error.args)
        print(error)

    @staticmethod
    async def process_missing_required_argument(context):
        await context.send_help(context.command)

    @staticmethod
    async def process_bad_argument(context, error):
        await context.send(str(error).replace("\"", "`"))


def setup(bot: Bot):
    bot.add_cog(ErrorCog())
