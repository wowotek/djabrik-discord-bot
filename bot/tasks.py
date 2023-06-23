import discord
from discord.ext import tasks

from .instagram import watcher
import asyncio


@tasks.loop(seconds=1)
async def cleanUpMessages(message: discord.Message):
    print("Hehe")
    # Check if its in #pendaftaran (1120154273007812609) channel, make it timeout
    if(message.channel.id == 1120154273007812609): # channel #pendaftaran
        await message.delete()

@tasks.loop(minutes=5)
async def instagramChecker(channel: discord.threads.Thread):
    if not await watcher.get_watch_status(): return

    asyncio.ensure_future(await watcher.TASK_watch())
    posts = await watcher.get_post_todos()
    if len(posts) == 0: return
    
    for post in posts:
        asyncio.ensure_future(channel.send("** **", embed=post), loop=asyncio.get_running_loop())