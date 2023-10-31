# tutBot.py
# This is a bot for my personal discord server.
# I use this as a way to continue my work with python,
# as well as create a fun environment for discord servers that I am a part of.

import os
import random
import discord
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
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f"{ctx.author.display_name}, you do not have the required role for this command.")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="question", help="This will give you a random question from a list of 4.")
async def random_question(ctx):
    # Returns a random question to the user.
    questions = ["What day is it?", "What is python?", "What is the meaning of life?", "Is there any more substance?"]
    response = random.choice(questions)
    await ctx.send(response)

@bot.command(name="roll", help="Simulates rolling dice.")
async def roll(ctx, number_of_dice: int = commands.parameter(description="Number of Dice"), number_of_sides: int = commands.parameter(description="Number of Sides")):
    # Roll a user decided number of dice with user decided number of sides.
    dice = [str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)]
    await ctx.send(", ".join(dice))

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


@bot.command(name="admin", help="A way to brag that you are an admin.")
@commands.has_role("admin") # Only run this command if user has selected role
async def admin_check(ctx):
    # Simply sends a message stating that this user is an admin.
    await ctx.send(f"{ctx.author.display_name} is an admin!")


bot.run(TOKEN)