from dotenv import load_dotenv
from os import getenv, listdir

from .utilites import log
from cubot import Bot

log("INIT", "The bot is starting.")

# .env
log("INIT", "Config file is loading.")
load_dotenv()
TOKEN = getenv("TOKEN")

CUBOT = Bot()

log("INIT", "Commands are loading.")
for file in listdir("./cubot/cogs"):
    if file.endswith(".py"):
        cmd = f"cubot.cogs.{file[:-3]}"
        CUBOT.load_extension(cmd)
        log("INIT", f"{cmd} command loaded.")

CUBOT.run(TOKEN)