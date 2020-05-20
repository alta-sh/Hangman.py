# A hangman bot for discord written by alta
import hangState
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='hang!')
client.remove_command('help')

runningGames = []
commands = ["help", "play"]

def isInGame(authorID):
    for game in runningGames:
        if (game["author"] == authorID):
            return True
    return False

def endGame(authorID):
    for game in runningGames:
        if (game["author"] == authorID):
            del runningGames[game]

@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    # Check if the message sender is currently in a game:
    if (isInGame(message.author.id)):

        # check if they've sent a command
        if (message.content.startswith(client.command_prefix)):
            await message.channel.send(f"You can't use that command whilst in a game {message.author.name}...\n"+
                                        "If you would like to end the game type `end` 🤗")
            return

        # If they end the game
        if (message.content == "end"):
            await message.channel.send("Thanks for playing {0}!\nGame successfully ended...".format(message.author.mention))
            endGame(message.author.id)
        else:
            # process the message 
            await message.channel.send("You're in a game")

    await client.process_commands(message)



@client.command()
async def play(ctx):
    await ctx.send('Ok {0}, setting up the game now 👍'.format(ctx.message.author.mention))

    # Check if user isn't already in a game
    if(isInGame(ctx.message.author.id)):
        await ctx.send(f'Actually {ctx.message.author.name}, it looks like you\'re already in a game...' +
                        'type `end` to leave it.')
    else:
        # Add userID and guesses to runningGames
        runningGames.append({"author": ctx.message.author.id, "remainingGuesses": 0})


# Reading the token
with open('token.txt', 'r') as file:
    client.run(file.readline())
