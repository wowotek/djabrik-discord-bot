import asyncio
import discord

from .instagram.watcher import *
from .tasks import instagramChecker, cleanUpMessages

DCBOT = discord.Bot(intents=discord.Intents.all(), debug=True, command_prefix="$")

@DCBOT.event
async def on_ready():
    print(f"+ Done! {DCBOT.user} is Online!")
    instagramChecker.start(DCBOT.get_channel(1120447977115361441))

@DCBOT.slash_command(name="ping", description="pong! PING PONG !!!")
async def ping(ctx: discord.commands.context.ApplicationContext):
    await ctx.respond("Pong!")

@DCBOT.slash_command(name="test", description="test random things")
async def test(ctx: discord.commands.context.ApplicationContext, profile_ig: str):
    await ctx.respond("Ok!")