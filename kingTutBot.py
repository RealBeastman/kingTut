# tutBot.py
# This is a bot for my personal discord server.
# I use this as a way to continue my work with python,
# as well as create a fun environment for discord servers that I am a part of.

import os
import json
import asyncio
import random
import discord
import urllib.request
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

description = "A bot by RealBeastman"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

@bot.event
async def on_command_error(ctx, error):
    # Displays error message when users do not have a required role inside the guild
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f"{ctx.author.display_name}, you do not have the required role for this command.")

@bot.event
async def on_ready():
    # Provides startup message to console
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="question", help="This will give you a random question from a list of 4.")
async def random_question(ctx):
    # Returns a random question to the user.
    questions = ["What day is it?", "What is python?", "What is the meaning of life?", "Is there any more substance?"]
    response = random.choice(questions)
    await ctx.send(response)

@bot.command(name="roll", help="Simulates rolling dice.")
async def roll(ctx, number_of_dice: int = commands.parameter(description="- Int: Number of Dice"), number_of_sides: int = commands.parameter(description=" - Int: Number of Sides")):
async def roll(ctx, number_of_dice: int = commands.parameter(description="Number of Dice"), number_of_sides: int = commands.parameter(description="Number of Sides")):
    # Roll a user decided number of dice with user decided number of sides.
    dice = [str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)]
    await ctx.send(", ".join(dice))

@bot.command(name="initiative", help='Rolls initiative for selected users.')
async def initiative(ctx, players: str = commands.parameter(description="- 'user1, user2, user3'")):
@bot.command(name="initiative", help="Rolls initiative for selected users.")
async def initiative(ctx, players: str = commands.parameter(description="Enter players separated by a commma and enclosed in quotes. 'User1, User2, User3'")):
    # Rolls standard DND initiative (20-sided die) for entered players.
    players_dict = {}
    players_list = list(players.split(", ")) # Converts command string into list for iterable functionality.

    for player in players_list: # Loops through the list to assign a rolled value to each player, then inserts player with assigned value into dictionary.
        rolled_value = random.randint(0, 20)
        players_dict[player] = rolled_value
       
    sorted_players_list = sorted(players_dict.items(), key = lambda x:x[1], reverse=True) # Sort the dictionary in descending order, converts to list in the process.
    sorted_players_dict = dict(sorted_players_list) # Convert back to dictionary.


    for player, roll in sorted_players_dict.items(): # Send the players and initiative rolls to channel.
        await ctx.send(f"{player} - {roll}")

@bot.command(name="dict", help="Enter a word, and the bot will output the definition. (!dict volume)")
async def dictionary(ctx, word: str = commands.parameter(description="Enter a word")):
    DICT_KEY = os.getenv("WEBSTERS_DICT_KEY")
    apiurl = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={DICT_KEY}'
    response = urllib.request.urlopen(apiurl)
    json_obj = json.load(response)
    definitions = json_obj[0]['shortdef']
    part = json_obj[0]['fl']
    num = 1

    await ctx.send(f"{word.capitalize()} ({part}):")

    for definition in definitions:
        await ctx.send(f"{num}. {definition}")
        num += 1

@bot.command(name="typing", help="Bot is typing.")
async def typing(ctx):
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.send("I was typing!")

@bot.command(name="nick", help="change nickname")
async def chnick(ctx, *, nick=None, member: discord.Member=None):
    if nick == None:
        nick = 'A cool nickname'
    try:
        if member:
            name_before = member.display_name
            await member.edit(nick=nick)
        else:
            member = ctx.message.author
            name_before = member.display_name
            await member.edit(nick=nick)
        await ctx.send(f"Changed {member.mention}'s nickname from {name_before} to {member.display_name}")
    except Exception as e:
        await ctx.send(str(e))

bot.run(TOKEN)
