# tutBot.py
# This is a bot for my personal discord server.
# I use this as a way to continue my work with python,
# as well as create a fun environment for discord servers that I am a part of.

import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    questions = ["Do you know the muffinman?", "What is the meaning of life?", "Why is 42 the answer to everything?", "Did you bring your towel?"]

    if message.content.lower() == "question":
        response = random.choice(questions)
        await message.channel.send(response)
    else:
        print("Not for me!")

client.run(TOKEN)