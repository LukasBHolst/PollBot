import discord
import os

from dotenv import load_dotenv
from collections import defaultdict

# Get Discord token from .env file
load_dotenv()
token = os.getenv("TOKEN")

client = discord.Client()  # Client

cats = defaultdict(int)   # Category dictionary for votes

running_poll = False      # Only 1 poll at a time


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global running_poll

    if message.author == client.user:
        return

    if message.content == '!help':
        await message.channel.send(f"No, you gotta say pretty please")

    if message.content.startswith('!help pretty please'):
        await message.channel.send(f"To start a poll use: !poll [name of poll] [vote 1] [vote 2] .. [vote n].\n \
                                     When you are done type: !endpoll")

    if message.content == ('!endpoll'):
        running_poll = False
        await message.channel.send(f"The votes are in!")
        sorted([(val, key) for (key, val) in cats.items()], reverse=True))
        for i, (k, v) in enumerate(cats):
            await message.channel.send(f"{i+1}. {k} with {v} " + ("vote" if v == 1 else "votes"))

    if message.content.startswith('!poll '):
        if running_poll == False:
            poll=message.content.split(' ')
            if len(poll) < 3:
                await message.channel.send("Invalid poll, try again")
                return
            poll_name=poll[1]
            for vote in poll[2:]:
                cats[vote]=0
            await message.channel.send(f"Starting poll: {poll_name}")
            running_poll=True
        else:
            await message.channel.send(f"A poll is already running. Wait for it to finish or use !endpoll")

    if message.content in cats:
        cats[message.content] += 1
        await message.channel.send(f"[{message.content} : {cats[message.content]} " + ("vote]" if cats[message.content] == 1 else "votes]"))

client.run(token)
