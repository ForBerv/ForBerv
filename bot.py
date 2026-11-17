import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def admin_only():
    return app_commands.checks.has_permissions(administrator=True)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"ForBerv جاهز: {bot.user} | تمت مزامنة {len(synced)} أمر")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.event
async def on_member_join(member):
    channel_id = os.getenv("WELCOME_CHANNEL_ID")
    if channel_id:
        channel = member.guild.get_channel(int(channel_id))
        if channel:
            await channel.send(f"ياهلا {member.mention} نورت السيرفر! 👑")

@bot.tree.command(name="مساعدة", description="عرض أوامر بوت ForBerv")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ForBerv | قائمة الأوامر",
        description=(
            "`/احصائيات` معلومات السيرفر\n"
            "`/تذكرة` فتح تذكرة دعم فني\n"
            "`/اغلاق` إغلاق التذكرة الحالية\n"
            "`/مسح` حذف عدد من الرسائل (للمشرفين)\n"
            "`/طرد` طرد عضو (للمشرفين)\n"
            "`/حظر` حظر عضو (للمشرفين)\n"
            "`/كتم` كتم عضو لمدة بالدقائق (للمشرفين)\n"
            "`/فك_كتم` إزالة الكتم (للمشرفين)\n"
            "`/ترحيب_تجربة` تجربة رسالة الترحيب"
        ),
        color=discord.Color.dark_grey()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="احصائيات", description="عرض إحصائيات السيرفر")
async def stats(interaction: discord.Interaction):
    g = interaction.guild
    embed = discord.Embed(title=f"إحصائيات {g.name}", color=discord.Color.dark_grey())
    embed.add_field(name="الأعضاء", value=str(g.member_count or "غير معروف"))
    embed.add_field(name="القنوات", value=str(len(g.channels)))
    embed.add_field(name="الرتب", value=str(len(g.roles)))
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="تذكرة", description="فتح تذكرة دعم فني خاصة")
async def ticket(interaction: discord.Interaction):
    guild = interaction.guild
    category = discord.utils.get(guild.categories, name="تذاكر ForBerv")
    if category is None:
        category = await guild.create_category("تذاكر ForBerv")
    existing = discord.utils.get(guild.text_channels, name=f"ticket-{interaction.user.id}")
    if existing:
        await interaction.response.send_message(f"عندك تذكرة مفتوحة بالفعل: {existing.mention}", ephemeral=True)
        return
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
    }
    channel = await guild.create_text_channel(
        name=f"ticket-{interaction.user.id}", category=category, overwrites=overwrites
    )
    await channel.send(f"{interaction.user.mention} أهلاً بك في دعم ForBerv 🎫\nاكتب مشكلتك، واستخدم `/اغلاق` عند الانتهاء.")
    await interaction.response.send_message(f"تم فتح تذكرتك: {channel.mention}", ephemeral=True)

@bot.tree.command(name="اغلاق", description="إغلاق التذكرة الحالية")
async def close_ticket(interaction: discord.Interaction):
    if not interaction.channel.name.startswith("ticket-"):
        await interaction.response.send_message("هذا الأمر يعمل داخل التذاكر فقط.", ephemeral=True)
        return
    await interaction.response.send_message("سيتم إغلاق التذكرة خلال 3 ثوانٍ.")
    await discord.utils.sleep_until(discord.utils.utcnow() + __import__("datetime").timedelta(seconds=3))
    await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")

@bot.tree.command(name="مسح", description="حذف رسائل من القناة")
@app_commands.describe(العدد="عدد الرسائل من 1 إلى 100")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, العدد: app_commands.Range[int, 1, 100]):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=العدد)
    await interaction.followup.send(f"تم حذف {len(deleted)} رسالة.", ephemeral=True)

@bot.tree.command(name="طرد", description="طرد عضو من السيرفر")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, العضو: discord.Member, السبب: str = "بدون سبب"):
    await العضو.kick(reason=السبب)
    await interaction.response.send_message(f"تم طرد {العضو.mention}. السبب: {السبب}")

@bot.tree.command(name="حظر", description="حظر عضو من السيرفر")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, العضو: discord.Member, السبب: str = "بدون سبب"):
    await العضو.ban(reason=السبب)
    await interaction.response.send_message(f"تم حظر {العضو.mention}. السبب: {السبب}")

@bot.tree.command(name="كتم", description="كتم عضو لمدة بالدقائق")
@app_commands.checks.has_permissions(moderate_members=True)
@app_commands.describe(الدقائق="مدة الكتم بالدقائق")
async def timeout(interaction: discord.Interaction, العضو: discord.Member, الدقائق: app_commands.Range[int, 1, 40320], السبب: str = "بدون سبب"):
    from datetime import timedelta
    await العضو.timeout(timedelta(minutes=الدقائق), reason=السبب)
    await interaction.response.send_message(f"تم كتم {العضو.mention} لمدة {الدقائق} دقيقة.")

@bot.tree.command(name="فك_كتم", description="إزالة الكتم عن عضو")
@app_commands.checks.has_permissions(moderate_members=True)
async def untimeout(interaction: discord.Interaction, العضو: discord.Member):
    await العضو.timeout(None)
    await interaction.response.send_message(f"تم فك الكتم عن {العضو.mention}.")

@bot.tree.command(name="ترحيب_تجربة", description="إرسال رسالة ترحيب تجريبية")
@app_commands.checks.has_permissions(administrator=True)
async def welcome_test(interaction: discord.Interaction):
    await interaction.response.send_message(f"ياهلا {interaction.user.mention} نورت السيرفر! 👑")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    msg = "ما عندك صلاحية تستخدم الأمر." if isinstance(error, app_commands.MissingPermissions) else "صار خطأ أثناء تنفيذ الأمر. تأكد من صلاحيات البوت."
    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)

if not TOKEN:
    raise RuntimeError("ضع DISCORD_TOKEN في ملف .env")
bot.run(TOKEN)
