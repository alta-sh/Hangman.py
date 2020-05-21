# A hangman bot for discord written by alta
import hangState
import random
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='hang!')
client.remove_command('help')

# Reading in nounlist
nounList = []
with open("nouns.txt", "r") as f:
    for word in f:
        nounList.append(word)

runningGames = []
commands = ["help", "play", "guess"]

# Checks if the user is in a game (if the author.id is in runningGames)
def isInGame(authorID):
    for game in runningGames:
        if (game["author"] == authorID):
            return True
    return False

# Deletes the authors dict in runningGames
def endGame(authorID):
    for game in runningGames:
        if (game["author"] == authorID):
            del runningGames[runningGames.index(game)]


def getAuthorIndex(authorID):
    for game in runningGames:
        if (game["author"] == authorID):
            return runningGames.index(game)

@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    message.content = message.content.lower()

    # Check if the message sender is currently in a game:
    if (isInGame(message.author.id)):

        if (not message.content.startswith("hang!guess")):
            # check if they've sent a command
            if (message.content.startswith(client.command_prefix)):
                await message.channel.send(f"You can't use that command whilst in a game {message.author.name}...\n"+
                                            "If you would like to end the game type `end` 🤗")
                return

            # If they end the game
            if (message.content == "end"):
                await message.channel.send(f"Thanks for playing {message.author.mention}!\nGame successfully ended...")
                endGame(message.author.id)

            # If they enter a word without writing hang!guess first
            elif (len(message.content) > 1):
                await message.channel.send(f"{message.author.mention} please only enter 1 character at a time!\n"+
                                            "If you would like to guess the word use the command \n`hang!guess {your guess}`\n"+
                                            "Or if you would like to quit the game write `end`")

            else: # process the message as a character guess 
                await message.channel.send("You guessed a character...")

    await client.process_commands(message)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Here are some commands for hangman.py", color=0x3be264)
    embed.add_field(name="hang!play", value="Starts a new game of hangman", inline=False)
    embed.add_field(name="hang!guess {your guess}", value="Guesses the word whilst in a game", inline=False)
    embed.add_field(name="hang!prefix {new prefix}", value="changes the prefix for commands...", inline=False)
    embed.add_field(name="end (whilst in a game)", value="Type 'end' when in a game to end the game", inline=False)
    embed.set_footer(text="This bot was written by alta#0001")
    await ctx.channel.send(embed=embed)

@client.command()
async def play(ctx):
    await ctx.send('Ok {0}, setting up the game now 👍'.format(ctx.message.author.mention))

    # Check if user isn't already in a game
    if(isInGame(ctx.message.author.id)):
        await ctx.send(f'Actually {ctx.message.author.name}, it looks like you\'re already in a game...' +
                        'type `end` to leave it.')
    else:
        # Add userID, guesses and a random word to runningGames
        randWord = nounList[random.randint(1, len(nounList))]
        runningGames.append({"author": ctx.message.author.id, "remainingGuesses": 5, "word": randWord})


@client.command()
async def guess(ctx, arg='null'):
    if (arg == 'null'):
        await ctx.send("Incorrect usage. Try: `hang!guess {your guess}`")
        return

    # Check if they're in a game when using the command
    if (isInGame(ctx.message.author.id)):
        # Check if the guess is correct
        authorIndex = getAuthorIndex(ctx.message.author.id)
        if (arg == runningGames[authorIndex]["word"]):
            await ctx.send(f"Well done {ctx.message.author.mention}! You guessed the word!") 
            endGame(ctx.message.author.id)
            return
        else: # If they get it wrong
            # Subtract their remaining guesses
            if (runningGames[authorIndex]["remainingGuesses"] != 1):
                runningGames[authorIndex]["remainingGuesses"] -= 1
                await ctx.send(f"Unlucky {ctx.message.author.mention}, that's not the word..."+
                            f"\nYou have {runningGames[authorIndex]['remainingGuesses']} guesses left.")
            else:
                await ctx.send(f"You're all out of guesses {ctx.message.author.mention}! Better luck next time...")
                endGame(ctx.message.author.id)
    else: # If they use the command while not in a game
        await ctx.send(f"You can only use this command whilst in a Hangman game {ctx.message.author.mention}.\n"+
                        "Type `hang!play` to get started...")

# Reading the token
with open('token.txt', 'r') as file:
    client.run(file.readline())
