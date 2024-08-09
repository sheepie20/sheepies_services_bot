import pathlib, os, discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

BASE_DIR = pathlib.Path(__file__).parent.parent
COGS_DIR = BASE_DIR / "cogs"

PREFIX = "t!"
INTENTS = discord.Intents.all()