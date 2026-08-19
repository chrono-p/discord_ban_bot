import discord
from discord.ext import commands
import os
from flask import Flask
import threading

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
        print(f"✅ 已登录为 {bot.user}")
        print(f"📡 正在监控 {len(bot.guilds)} 个服务器")

@bot.event
async def on_member_remove(member):
     try:
        await member.ban(reason="自动封禁：主动退出服务器")
        print(f"🔨 已封禁 {member.name}#{member.discriminator} (ID: {member.id})")
     except discord.Forbidden:
        print(f"权限不足，无法封禁 {member.name}")
     except discord.HTTPException as e:
        print(f"封禁失败: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def unban_user(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"已解封 {user.name}")
    except discord.NotFound:
        await ctx.send("未找到该用户或未被封禁")
    except discord.Forbidden:
        await ctx.send("权限不足")
            
app = Flask(__name__)

@app.route('/')
def hello():
        return "Bot is running!"

def run_web():
        app.run(host='0.0.0.0',port=10000)

threading.Thread(target=run_web).start()

bot.run(os.getenv("DISCORD_TOKEN"))
