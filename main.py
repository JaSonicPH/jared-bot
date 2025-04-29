import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import helpers.ioi as ioi

load_dotenv()

def check(author):
    def inner_check(message): 
        if message.author != author:
            return False
        try: 
            int(message.content) 
            return True 
        except ValueError: 
            return False
    return inner_check








token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='dc.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv('PREFIX')+' ', intents = intents)
    
@bot.command()
async def ping(ctx):
    await ctx.send(ctx.latency)

@bot.command(brief="you know what this does. only jared can call this.")
async def resetDB(ctx):
    print("uh oh")
    if ctx.author.id != "663237980126707725": return
    await ctx.send("are you sure? pls send \"I AM WILLINGLY RESETTING THE DATA.\".")
    msg = await bot.wait_for('message', check=check(ctx.author), timeout=30)
    ioi.reset(msg)
    await ctx.send("reset!")
        
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    await bot.load_extension("cogs.ioi_cmds")
    await bot.start(os.getenv('DISCORD_TOKEN'))

import asyncio
asyncio.run(main())