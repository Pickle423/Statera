# bot.py
import nextcord, os, logging
from dotenv import load_dotenv
from nextcord.ext import commands, tasks
intents = nextcord.Intents.default()
intents.members = True

# is a .env file inside the folder to leave the token for the bot outside the git
load_dotenv()

# Debug Helpers
## Logging
## logging.basicConfig(level=logging.INFO)

# bot commands have a prefix so all messages that start with the prefix will trigger the bot commands
client = commands.Bot(command_prefix='?', intents=intents, help_command = None, case_insensitive=True)

# when the bot is initialized it will print has connected to the terminal
@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")

#Cogs Loader
@client.command()
async def load(ctx, extension):
    if ctx.message.author.id != 267469338557153300:
        return
    client.load_extension(f'cogs.{extension}')
    print(f"Successfully loaded cogs.{extension}")

@client.command()
async def unload(ctx, extension):
        if ctx.message.author.id != 267469338557153300:
            return
        client.unload_extension(f'cogs.{extension}')
        print(f"Successfully unloaded cogs.{extension}")

@client.command()
async def reload(ctx, extension):
        if ctx.message.author.id != 267469338557153300:
            return
        if extension == "all" or extension == "All":
            for filename in os.listdir('./cogs'):
                try:
                    if filename.endswith('.py'):
                        client.reload_extension(f'cogs.{filename[:-3]}')
                        print(f"Successfully reloaded cogs.{filename[:-3]}")
                except:
                    print(f"WARNING: Failed to load cogs.{filename[:-3]}")
            print("Reload complete.")    
        else:
            client.reload_extension(f'cogs.{extension}')
            print(f"Successfully reloaded cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if "ignore" in filename:
            pass
        else:
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f"""WARNING: Failed to load cogs.{filename[:-3]}. Error is defined below:\n{e}""")

client.run(os.getenv("discord_token"))