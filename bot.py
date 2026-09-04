import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive

# Bot sınıfını Slash komutlarını senkronize edecek şekilde ayarlıyoruz
class DMBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash komutları başarıyla senkronize edildi.")

bot = DMBot()

@bot.event
async def on_ready():
    print(f'{bot.user} aktif ve Slash (/) komutlarına hazır!')

# 1. KOMUT: TEK KİŞİYE GÖNDER
@bot.tree.command(name="dm_kisi", description="Belirtilen tek bir kullanıcıya DM atar.")
async def dm_kisi(interaction: discord.Interaction, kullanici: discord.User, mesaj: str):
    await interaction.response.defer(ephemeral=True) # Sadece komutu yazan görsün
    try:
        await kullanici.send(mesaj)
        await interaction.followup.send(f"✅ {kullanici.mention} adlı kişiye mesaj iletildi.")
    except discord.Forbidden:
        await interaction.followup.send(f"❌ {kullanici.mention} kişisine DM atılamıyor (Gizlilik ayarları kapalı).")
    except Exception as e:
        await interaction.followup.send(f"Bir hata oluştu: {e}")

# 2. KOMUT: HERKESE GÖNDER (Sadece Yöneticiler)
@bot.tree.command(name="dm_herkes", description="Sunucudaki tüm üyelere DM atar.")
@discord.app_commands.checks.has_permissions(administrator=True) # Güvenlik için sadece yetkililer
async def dm_herkes(interaction: discord.Interaction, mesaj: str):
    await interaction.response.defer(ephemeral=True)
    
    basarili = 0
    basarisiz = 0

    await interaction.followup.send("⏳ Herkese DM gönderimi başladı. Sunucu büyüklüğüne göre bu işlem biraz sürebilir...")

    for member in interaction.guild.members:
        if member.bot: # Botlara mesaj atmayı atla
            continue 
        
        try:
            await member.send(mesaj)
            basarili += 1
            await asyncio.sleep(1) # ÖNEMLİ: Discord'dan ban yememek için her mesaj arası 1 saniye bekle
        except discord.Forbidden:
            basarisiz += 1
        except Exception:
            basarisiz += 1

    await interaction.followup.send(f"✅ **Toplu DM İşlemi Bitti!**\nİletilen: `{basarili}` kişi\nİletilemeyen (DM'i kapalı olan): `{basarisiz}` kişi")

keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
