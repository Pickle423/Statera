import nextcord
from nextcord.ext import commands
intents = nextcord.Intents.default()
intents.members = True

#Moderation Cog
class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def cog_check(self, ctx):
        #Check if user has manage messages permissions
        return ctx.author.guild_permissions.manage_messages
    
    @nextcord.slash_command(name='clean',description="Cleans the number of messages specified.")
    @commands.has_permissions(administrator=True)
    async def clean(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.response.send_message("Messages have been removed!", delete_after=5)

def setup(client):
    client.add_cog(Moderation(client))