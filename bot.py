import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} aktif edildi ve DM atmaya hazır!')

@bot.command()
async def dm(ctx, user: discord.User, *, message: str):
    if ctx.author == bot.user:
        return
    try:
        await user.send(message)
        await ctx.send(f"✅ {user.name} kullanıcısına mesaj iletildi.")
    except discord.Forbidden:
        await ctx.send(f"❌ {user.name} kullanıcısına DM gönderilemiyor. (Gizlilik ayarları kapalı olabilir)")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")

# Render'ın port dinlemesi için web sunucusunu başlatıyoruz
keep_alive()

# Token'i kod içine yazmak yerine güvenlik için çevre değişkeninden çekiyoruz
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)