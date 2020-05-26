import json
from collections import deque

from discord import Message, TextChannel, Role, utils
from discord.ext import commands
from discord.ext.commands import Cog, command, Context, Bot, Command


class AmaCog(Cog):
    def __init__(self):
        with open("saved_questions.json", "r") as read_file:
            self.question_data = json.load(read_file)
            print(self.question_data)
        for each_channel in self.question_data:
            self.question_data[each_channel]["queue"] = deque(self.question_data[each_channel]["queue"])

        for each_channel in self.question_data:
            print(type(self.question_data[each_channel]["queue"]))
            print(type(self.question_data[each_channel]))

    def convert_deque(self, deque):
        return list(deque)

    def save_questions(self):
        saved_questions = json.dumps(self.question_data, default=self.convert_deque)
        with open('saved_questions.json', 'w') as outfile:
            outfile.write(saved_questions)

    @commands.has_guild_permissions(manage_channels=True)
    @command(name="qachannel")
    # 'qachannel' command, to designate a channel as a Q&A channel and set a respective answerer role. This channel
    # will automatically delete and queue messages from non answerer roles, allowing a select number of users to type in
    # the channel and respond at their convenience with the 'nextquestion' command.
    async def qa_channel(self, context: Context, channel: TextChannel, role: str):
        if channel.id in self.question_data:
            # Checking if the channel is linked to a question queue. If it is, then it is already a Q&A channel.
            await context.send(
                "This channel is already a Q&A channel. To remove a Q&A channel, use the ``qaremove`` command.")
        else:
            await context.send("Channel ``" + str(channel) + "`` is now in Q&A format.")
            self.question_data[channel.id] = {"queue": deque(), "is_ready": False, "answer_role": role}
            # 'question_data' is a dictionary where each key is the id of a Q&A channel, and each linked value is
            # another dictionary storing the corresponding question queue, answer role, and a boolean indicating whether
            # the answerer is waiting for the next question.

            self.save_questions()

    @Cog.listener()
    async def on_message(self, message: Message):
        channel = message.channel.id
        if message.author.bot:
            return
        elif (channel in self.question_data) and (
                utils.get(message.author.roles, name=self.question_data[channel]["answer_role"])) == None:
            self.question_data[channel]["queue"].append({"content": message.content, "author": message.author.mention})
            await message.delete()
            # If a user who is not a designated answerer or a bot types in a Q&A channel, their message will be removed
            # and added to the channel's queue. The queue also stores the string to mention the author of the message.
            if self.question_data[channel]["is_ready"]:
                current_message = self.question_data[channel]["queue"].popleft()
                self.save_questions()
                self.question_data[channel]["is_ready"] = False
                await message.channel.send(
                    "User " + current_message["author"] + " asks:\n" + ">>> " + current_message["content"])
            # If an answerer has previously used the 'nextquestion' command but there were no questions in the queue,
            # the bot remembers they were waiting and immediately sends the next question as soon as it is asked.

    @command(name="nextquestion")
    async def next_question(self, context: Context):
        channel = context.channel.id
        if channel in self.question_data and (utils.get(context.author.roles, name=self.question_data[channel]["answer_role"])) != None:
            # This command only runs if being used by a designated answerer in a Q&A channel.
            await context.message.delete()
            if not self.question_data[channel]["queue"]:
                await context.send("No more questions are currently queued! Maybe check back later :)")
                self.question_data[channel]["is_ready"] = True
            else:
                current_message = self.question_data[channel]["queue"].popleft()
                self.save_questions()
                await context.send(
                    "User " + current_message["author"] + " asks:\n" + ">>> " + current_message["content"])
                # If the question queue for the relevant channel is not empty, the bot sends the oldest message and
                # removes it from the queue. Otherwise, it will notify the answerer that the queue is empty, and send
                # the next question as soon as it is asked without requiring the command to be triggered again.


def setup(bot: Bot):
    bot.add_cog(AmaCog())
