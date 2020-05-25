import json
from collections import deque

from discord import Message, TextChannel, Role, utils
from discord.ext import commands
from discord.ext.commands import Cog, command, Context, Bot, Command

class AmaCog(Cog):
    def __init__(self):
        self.question_storage = {}
        self.ready_for_next_question = {}

    #def save_questions(self):
        #json_text = json.dumps(self.question_storage)
        #with open('data.txt', 'w') as write_to_file:
            #json.dump(json_text, write_to_file)

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
            self.ready_for_next_question[channel] = False
            # 'ready_For_next_question' is a dictionary where each key is a Q&A channel, and each linked value indicates
            # whether or not an answerer is waiting for another question to be sent. Creating a Q&A channel adds
            # another element.
            #self.save_questions()

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        elif (message.channel in self.question_storage) and (utils.get(message.author.roles, name = 'Answerer')) == None:
            self.question_storage[message.channel].append(message)
            await message.delete()
            # If a user who is not a designated answerer or a bot types in a Q&A channel, their message will be removed
            # and added to the channel's queue.
            if self.ready_for_next_question[message.channel]:
                current_message = self.question_storage[message.channel].popleft()
                #self.save_questions()
                self.ready_for_next_question[message.channel] = False
                await message.channel.send(
                    "User " + current_message.author.mention + " asks:\n" + ">>> " + current_message.content)
            # If an answerer has previously used the 'nextquestion' command but there were no questions in the queue,
            # the bot remembers they were waiting and immediately sends the next question as soon as it is asked.

    @command(name="nextquestion")
    async def next_question(self, context: Context):
        if context.channel in self.question_storage and (utils.get(context.author.roles, name = 'Answerer')) != None:
            # This command only runs if being used by a designated answerer in a Q&A channel.
            await context.message.delete()
            if not self.question_storage[context.channel]:
                await context.send("No more questions are currently queued! Maybe check back later :)")
                self.ready_for_next_question[context.channel] = True
            else:
                current_message = self.question_storage[context.channel].popleft()
                #self.save_questions()
                await context.send(
                    "User " + current_message.author.mention + " asks:\n" + ">>> " + current_message.content)
                # If the question queue for the relevant channel is not empty, the bot sends the oldest message and
                # removes it from the queue. Otherwise, it will notify the answerer that the queue is empty, and send
                # the next question as soon as it is asked without requiring the command to be triggered again.

def setup(bot: Bot):
    bot.add_cog(AmaCog())