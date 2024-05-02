import nextcord
from nextcord.ext import commands
intents = nextcord.Intents.default()
intents.members = True

#Moderation Cog
class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name='clean',description="Cleans the number of messages specified.")
    async def clean(self, ctx, amount: int):
        if not ctx.user.guild_permissions.administrator:
            return await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
        await ctx.channel.purge(limit=amount)
        await ctx.response.send_message("Messages have been removed!", delete_after=5)

def setup(client):
    client.add_cog(Moderation(client))