# A hangman bot for discord written by alta
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='hang!')
client.remove_command('help')

@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.command()
async def play(ctx):
    await ctx.send('Ok {0}, setting up the game now 👍'.format(ctx.message.author.mention))

# Reading the token
with open('token.txt', 'r') as file:
    client.run(file.readline())
