import json
from collections import deque

from discord import Message, TextChannel, Role, utils
from discord.ext import commands
from discord.ext.commands import Cog, command, Context, Bot


def encode_deque(x):
    if isinstance(x, deque):
        return {"is_deque": True, "deque": list(x)}
    else:
        return (x)


# A function to encode deques in JSON.

def decode_deque(x):
    if "is_deque" in x:
        return deque(x["deque"])
    else:
        return x


# A function to decode deques from JSON to Python.

class AmaCog(Cog):
    def __init__(self):
        with open("saved_questions.json", "r") as read_file:
            self.question_data = json.load(read_file, object_hook=decode_deque)


    def save_questions(self):
        saved_questions = json.dumps(self.question_data, default=encode_deque)
        with open('saved_questions.json', 'w') as outfile:
            outfile.write(saved_questions)

    @commands.has_guild_permissions(manage_channels=True)
    @command(name="qachannel")
    # 'qachannel' command, to designate a channel as a Q&A channel and set a respective answerer role. This channel
    # will automatically delete and queue messages from non answerer roles, allowing a select number of users to type in
    # the channel and respond at their convenience with the 'nextquestion' command.
    async def qa_channel(self, context: Context, channel: TextChannel, role: Role):
        if channel.id in self.question_data:
            # Checking if the channel is linked to a question queue. If it is, then it is already a Q&A channel.
            await context.send(
                "This channel is already a Q&A channel. To remove a Q&A channel, use the ``qaremove`` command.")
        else:
            await context.send(
                "Channel ``" + str(channel) + "`` is now in Q&A format. The answerer role is ``" + role.name + "``.")
            self.question_data[str(channel.id)] = {"queue": deque(), "is_ready": False, "answer_role": str(role.id),
                                                   "channel_name": channel.name, "role_name": role.name}
            # 'question_data' is a dictionary where each key is the id of a Q&A channel, and each linked value is
            # another dictionary storing the corresponding question queue, answerer role id, a boolean indicating
            # whether the answerer is waiting for the next question, the name of the channel, and the name of the
            # answerer role.
            self.save_questions()

    @commands.has_guild_permissions(manage_channels=True)
    @command(name="qaremove")
    # 'qaremove' command, to cease a channel from being designated as a Q&A channel. The only argument is the channel.
    async def qa_remove(self, context: Context, channel: TextChannel):
        if str(channel.id) in self.question_data:
            del (self.question_data[str(channel.id)])
            await context.send("Channel ``" + str(channel) + "`` is no longer in Q&A format.")
            self.save_questions()
            # All the data corresponding to the removed Q&A channel is deleted.
        else:
            await context.send("Channel ``" + str(channel) + "`` was already not in Q&A format. To designate a channel "
                                                             "as Q&A, use the ``qachannel`` command.")
            # If the channel selected already wasn't a Q&A channel, the bot notifies the user.

    @Cog.listener()
    async def on_message(self, message: Message):
        channel = str(message.channel.id)
        if message.author.bot:
            return
        elif (channel in self.question_data) and not (
                utils.get(message.author.roles, id=int(self.question_data[channel]["answer_role"]))):
            self.question_data[channel]["queue"].append({"content": message.content, "author": message.author.mention})
            await message.delete()
            # If a user who is not a designated answerer or a bot types in a Q&A channel, their message will be removed
            # and added to the channel's queue. The queue also stores the string to mention the author of the message.
            if self.question_data[channel]["is_ready"]:
                current_message = self.question_data[channel]["queue"].popleft()
                self.question_data[channel]["is_ready"] = False
                self.save_questions()
                await message.channel.send(
                    "User " + current_message["author"] + " asks:\n" + ">>> " + current_message["content"])
            # If an answerer has previously used the 'nextquestion' command but there were no questions in the queue,
            # the bot remembers they were waiting and immediately sends the next question as soon as it is asked.

    @command(name="nextquestion")
    async def next_question(self, context: Context):
        channel = str(context.channel.id)
        if channel in self.question_data and (
                utils.get(context.author.roles, id=int(self.question_data[channel]["answer_role"]))):
            # This command only runs if being used by a designated answerer in a Q&A channel.
            await context.message.delete()
            if not self.question_data[channel]["queue"]:
                await context.send("No more questions are currently queued! The next question will automatically "
                                   "send. Check back later :)")
                self.question_data[channel]["is_ready"] = True
            # If the question queue for the relevant channel is empty, the bot will notify the answerer and send the
            # next question as soon as it is asked without requiring the command to be triggered again.
            else:
                current_message = self.question_data[channel]["queue"].popleft()
                await context.send(
                    "User " + current_message["author"] + " asks:\n" + ">>> " + current_message["content"])
            # If there are questions in the queue, the bot will send the oldest one and mention the user who asked the
            # question, and remove it from the queue.
            self.save_questions()


def setup(bot: Bot):
    bot.add_cog(AmaCog())
