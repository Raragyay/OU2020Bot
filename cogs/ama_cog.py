from collections import deque

from discord import Message, TextChannel, Role, utils
from discord.ext import commands
from discord.ext.commands import Cog, command, Context, Bot, Command

class AmaCog(Cog):
    def __init__(self):
        self.linked_list = {}
        self.question_storage = {}

    @commands.has_any_role("Admin", "Moderator")
    @command(name="qachannel")
    # 'qachannel' command, to designate the channel as a Q&A channel. This channel will automatically delete and queue
    # messages from non answerer roles, allowing a select number of users to type in the channel and respond at their
    # convenience with the 'nextquestion' command.
    async def qa_channel(self, context: Context, channel: TextChannel):
        if channel in self.question_storage:
            # Checking if the channel is linked to a question queue. If it is, then it is already a Q&A channel.
            await context.send("This channel is already a Q&A channel. To remove a Q&A channel, use the ``qaremove`` command.")
        else:
            await context.send("Channel ``"+str(channel)+"`` is now in Q&A format.")
            self.question_storage[channel] = deque()
            # 'question_storage' is a dictionary where each key is a Q&A channel, and each linked value is the
            # corresponding question queue to that channel. Creating a Q&A channel adds another element.

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        elif (message.channel in self.question_storage) and (utils.get(message.author.roles, name = 'Answerer')) == None:
            # If a user who is not a designated answerer or a bot types in a Q&A channel, their message will be removed
            # and added to the channel's queue.
            self.question_storage[message.channel].append(message)
            await message.delete()

    @command(name="nextquestion")
    async def next_question(self, context: Context):
        if context.channel in self.question_storage and (utils.get(context.author.roles, name = 'Answerer')) != None:
            # This command only runs if being used by a designated answerer in a Q&A channel.
            await context.message.delete()
            if not self.question_storage[context.channel]:
                await context.send("No more questions are currently queued! Maybe check back later :)")
            else:
                current_message = self.question_storage[context.channel].popleft()
                await context.send(
                    "User " + current_message.author.mention + " asks:\n" + ">>> " + current_message.content)
                # If the question queue for the relevant channel is not empty, the bot sends the oldest message and
                # removes it from the queue. Otherwise, it will notify the answerer that the queue is empty.

def setup(bot: Bot):
    bot.add_cog(AmaCog())