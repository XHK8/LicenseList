import disnake
from disnake.ext import commands
import os
import importlib

token = "MTI2ODg5Mjk5MzAxNzA5MDE4OA.Gho32W._OzbYmRhcHc5okdn-Dct2nZLHKvn7OLbjiNdYo" # 봇토큰
intents = disnake.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    activity = disnake.Game(name="XHK8샵 노예")
    await bot.change_presence(status=disnake.Status.idle, activity=activity)
    print("Bot is ready!")

# 명령어 로드 함수
def load_commands():
    base_path = "commands"
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file).replace("/", ".").replace("\\", ".")[:-3]
                module = importlib.import_module(module_path)
                if hasattr(module, "setup"):
                    module.setup(bot)

# 명령어 로드
load_commands()


bot.run(token)