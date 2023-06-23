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

RULES = [
    "## Apa Itu 'Warga Bhumi' ?\n"
    "Warga bhumi adalah komunitas kumpulan orang orang yang aktif berkomunitas\n"
    "Di wilayah Bogor Kota, dan Kabupaten Bogor.\n\n",
    "## Peraturan Umum\n"
    "**1.** Dilarang berdiskusi segala sesuatu yang bersifat ilegal selama menjadi **Warga Bhumi**\n"
    "**2.** Dilarang melakukan pertengkaran, pembullian, ejekan kepada orang lain, serta diskusi yang bersifat Suku, Agama, Ras, dan Antargolongan\n"
    "**3.** Dilarang melakukan pengemisan, iklan, atau survey dalam bentuk apapun\n"
    "**4.** Dilarang melakukan transaksi apapun dalam bentuk, benda, dan/atau cara apapun\n"
    "**5.** Wajib membaca nama _channel_ dan topik pada _channel_ tersebut, dilarang membicarakan hal diluar topik yang disediakan\n"
    "**6.** Dilarang melakukan mention terhadap _**Pemilik**_, _**ComDev**_, _**Moderator**_ yang tidak bersifat darurat. Pelaporan dilakukan di <#1115218091551494164> dan pelaporan pelanggaran peraturan dan/atau hal ilegal pada <#1120071716501209148>\n"
    "**7.** calon member subkomunitas Warga Bhumi wajib membaca Peraturan dan Syarat pada forum dan topik subkomunitas tersebut\n"
    "**8.** Segala sesuatu yang terjadi didalam forum, biarkan tetap dalam forum, dilarang  membawa perihal tersebut diluar forum\n"
    "**9.** Segala sesuatu yang dilakukan anda sendiri, begitu juga implikasinya adalah tanggung jawab anda sendiri, segala kerugian yang terjadi, bukan tanggung jawab pihak pengelola **Warga Bhumi**\n"
    "**10.** Wajib mengerti seluruh tulisan, media gambar, media video yang tertulis didalam <#1118476800188756038>, jika ada yang tidak mengerti silahkan tanyakan pada forum Customer Service atau bicarakan pada Pengelola **Warga Bhumi** secara offline / langsung, sebelum menjadi member.\n"
    "**11.** Tidak ada pengecualian apapun pada segala sesuatu yang tertulis, dan tersirat pada channel <#1118476800188756038>, kecuali ada perubahan atau pengumuman dalam rentang waktu tertentu tentang perubahan atau pengecualian tersebut.\n",
    "**12.** Untuk melakukan registrasi, akan ditanya kode, maka gunakan kode ini: `<KODE_REGISTRASI>`\n",
    "**13.** Jaga sopan dan santun, serta jalani adab, nilai, dan norma yang sudah tertanam di dalam forum dan sub-komunitas.\n\n",
    
    "## Aturan Main Umum\n"
    "**1.** Baca segala sesuatu yang ada didalam channel <#1118476800188756038>, anda harus setuju dengan semua yang tertulis, dan tersirat.\n"
    "**2.** Pilih Roles yang anda inginkan sebagai fokus kegiatan anda, Roles ini akan membuka channel yang bersangkutan.\n"
    "**3.** Untuk bergabung pada sub-komunitas untuk menjadi Member ataupun Community Developer komunitas tersebut: \n"
    "  - untuk menjadi **Community Developer** / **ComDev** silahkan mendaftar di <#1120077393982406806>\n"
    "  - untuk menjadi **Member** Komunitas silahkan mendaftar di <#1120412792810393600>\n"
    "  - untuk menjadi **Peminat**, silahkan pilih peminatan di <#1120185281442746418>\n"
    "**4.** Wajib membaca pengumuman oleh Pihak pengelola pada channel <#1120400513159135353> pada topik Forum Umum\n",

    "## Kalau jadi Warga Bhumi trus apa ?\n"
    "- Setelah mendaftar menjadi Warga Bhumi, anda akan memiliki poin experience (XP)\n"
    "- XP tersebut bisa bertambah bisa juga berkurang sesuai dengan kontribusi yang anda berikan selama menjadi Warga Bhumi\n"
    "- XP akan bertambah sebanyak minimum **2** setiap 10 menit sekali dengan menjadi Warga Bhumi pasif\n"
    "- Segala bentuk kontribusi terkecil seperti _chatting_ terhitung pengumpulan point\n"
    "- _Chatting_ di forum umum memberikan point sejumlah **1**, sedangkan di forum komunitas, sebanyak **2**\n"
    "- Kehadiran di kafe, resto, dan tempat yang berafiliasi dengan komunitas Warga Bhumi memberikan point sebesar **50**\n"
    "- Kontribusi online komunitas memberikan Point XP terkecil minimum **75**\n",
    "- Kehadiran ke acara yang diadakan komunitas memberikan point:\n"
    "  - Absen sebagai **Peminat** memberikan point **125**\n"
    "  - Absen sebagai **Member** memberikan point **250**\n"
    "  - Absen sebagai **ComDev** memberikan point **280**\n"
    "- Menjadi kru penyelenggara acara yang diadakan komunitas, memberikan point minimum **2500**\n",
    "- Segala bentuk Larangan yang dilakukan akan terhitung pengurangan point\n",
    "- Point XP juga dapat berkurang jika ada user yang melaporkan anda menggunakan perintah `/laporkan level`. jumlah yang dikurangi ditentukan oleh:\n"
    "  - Hirarki, seperti Pemilik akan mengurangi point anda dengan jumlah yang lebih besar dibanding 'Warga'\n"
    "  - Level pelaporan yang dilakukan orang, `1`, `2`, `3`, `4`, `5`, dan `6` sebagai tertinggi, level `1` mengurangi point sebanyak **5** dan level `5` sebanyak **25**. `6` mengurangi point sebanyak **125**\n"
    "  - Level pelaporan akan dikalikan dengan hirarki orang pelapor, `warga`=**x1**, `moderator`=**x2**, `pemilik`=**x5**\n"

    "## Persetujuan dan Registrasi\n"
    "Jika anda setuju dengan seluruh yang tertulis,\n"
    "dan tersirat pada channel <#1118476800188756038> ini\n"
    "serta ingin menjadi **Warga Bhumi** silahkan\n"
    "Melanjutkan ke Channel <#1120154273007812609>\n"
]
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