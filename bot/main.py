import os
import dotenv
dotenv.load_dotenv()

import asyncio
import uvloop
uvloop.install()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import discord

from .client import DCBOT
from .instagram import watcher


@DCBOT.slash_command(name="peraturan", description="Kasih tau gue dan yang lain aturan server ini tuh gimana sih?!")
async def show_rules(ctx: discord.commands.context.ApplicationContext):
    if(len(ctx.author.roles) == 1):
        await ctx.respond("Anda tidak memiliki izin untuk menggunakan perintah ini", ephemeral=True)
        return
    
    await ctx.respond("Oke Siap Tuan, berikut peraturan server ini. silahkan dibaca", ephemeral=True)
    [await ctx.send(i) for i in RULES]

@DCBOT.slash_command(name="daftar", description="Mendaftar sebagai **Warga Bhumi**")
async def register(ctx: discord.commands.context.ApplicationContext):
    if(ctx.channel.id != 1120154273007812609):
        await ctx.respond("Pendaftaran **Warga Bhumi** hanya dapat dilakukan di channel <#1120154273007812609>", ephemeral=True)
        return
    
    if(len(ctx.author.roles) != 1):
        await ctx.respond("Anda sudah terdaftar, tidak perlu mendaftar ulang!\n\nJika anda ngeyel, silahkan ulangi pendaftaran dengan cara\nkeluar dari server lalu join ulang", ephemeral=True)
        return

instagram_news_watch = DCBOT.create_group(name="atur_berita_instagram", description="Tambah / Kurangi sumber berita instagram")
@instagram_news_watch.command()
async def tambahkan(ctx: discord.commands.context.ApplicationContext, profile_id: str):
    CHANNEL = DCBOT.get_channel(1120418725603069962)

    async def __cb(embeds: list[discord.Embed]):
        print("Sending Embeds")
        for i in embeds:
            await ctx.send("| Incoming News !", embed=i)

    status = watcher.add_to_watch_list(profile_id, __cb)
    if status:
        await ctx.respond(f"<@{ctx.author.id}> set ig `@{profile_id}` to News Watch list\nthis will be posted at <#1120447977115361441>")
    else:
        await ctx.respond(f"Instagram @{profile_id} already being watched", ephemeral=True)

@instagram_news_watch.command()
async def hapus(ctx: discord.commands.context.ApplicationContext, profile_id: str):
    status = watcher.remove_from_watch_list(profile_id)
    if status:
        await ctx.respond(f"Instagram @{profile_id} has been removed from watch list", ephemeral=True)
    else:
        await ctx.respond(f"Instagram @{profile_id} doesn't exist in watch list", ephemeral=True)

def run():
    DCBOT.run(os.getenv("DISCORD_TOKEN"))