import discord
import os

from dotenv import load_dotenv
from collections import defaultdict

# Get Discord token from .env file
load_dotenv()
token = os.getenv("TOKEN")

client = discord.Client()  # Client

cats = defaultdict(int)    # Category dictionary for votes
voters = defaultdict(str)

running_poll = False       # Only 1 poll at a time
poll_name = ""


def get_indexes_of_string(s, find):
    return [n for (n, e) in enumerate(s) if e == find]


# Writing to terminal on start-up
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


# Listening for messages on discord
@client.event
async def on_message(message):
    global running_poll
    global poll_name

    if message.author == client.user:
        return

    if message.content == '!help':
        await message.channel.send(f"No, you gotta say pretty please")

    if message.content.startswith('!help pretty please'):
        await message.channel.send(f"To start a poll use: !poll [name of poll] [vote 1] [vote 2] .. [vote n].\n \
                                     You then write the thing you want to vote on. \
                                     When you are done type: !endpoll")

    if message.content == '!endpoll':
        running_poll = False
        await message.channel.send(f"The votes are in for {poll_name}!")
        for i, (v, k) in enumerate(sorted([(val, key) for (key, val) in cats.items()], reverse=True)):
            await message.channel.send(f"{i+1}. {k} with {v} " + ("vote" if v == 1 else "votes"))

    if message.content.startswith('!poll '):
        idx_1, idx_2 = 0, 0
        if running_poll == False:
            if '"' in message.content:
                idx_1, idx_2 = get_indexes_of_string(message.content, '"')
                poll_name = message.content[idx_1+1:idx_2]
                poll = message.content[idx_2+2:].split(' ')
                print(poll)
                for vote in poll:
                    cats[vote] = 0
            else:
                poll = message.content.split(' ')
                if len(poll) < 3:
                    await message.channel.send("Invalid poll, try again")
                    return
                poll_name = poll[1]
                for vote in poll[2:]:
                    cats[vote] = 0
            await message.channel.send(f"Starting poll: {poll_name}\nYou can vote for:\n")
            for i, key in enumerate(cats):
                await message.channel.send(f"{i+1}. {key}")
            running_poll = True
        else:
            await message.channel.send(f"A poll is already running. Use !endpoll to end it")

    if message.content in cats:
        if voters[message.author.id] != 1:
            cats[message.content] += 1
            voters[message.author.id] = 1
            await message.channel.send(f"[{message.content} : {cats[message.content]} " + ("vote]" if cats[message.content] == 1 else "votes]"))
        else:
            await message.channel.send(f"{message.author.name} already voted")

client.run(token)
