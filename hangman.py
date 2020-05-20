# A hangman bot for discord written by alta
import hangState
import discord
from discord.ext import commands

runningGames = []

client = commands.Bot(command_prefix='hang!')
client.remove_command('help')

def isInGame(authorID):
    if (authorID in runningGames):
        return True
    return False

@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if (isInGame(message.author.id)):

        if (message.content == "end"):
            await message.channel.send("Thanks for playing {0}!\nGame successfully ended...".format(message.author.mention))
            runningGames.remove(message.author.id)
        else:
            await message.channel.send("You're in a game...")


    await client.process_commands(message)

@client.command()
async def play(ctx):
    await ctx.send('Ok {0}, setting up the game now 👍'.format(ctx.message.author.mention))
    # The user id of the current player
    runningGames.append(ctx.message.author.id)


# Reading the token
with open('token.txt', 'r') as file:
    client.run(file.readline())
