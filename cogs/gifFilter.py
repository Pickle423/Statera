import nextcord
from nextcord.ext import commands
#gifFilter Cog
class gifFilter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            exception_channels = [nextcord.utils.get(message.guild.text_channels, name="voice-chat"),nextcord.utils.get(message.guild.text_channels, name="random"),nextcord.utils.get(message.guild.text_channels, name="bot-commands")]
            if message.channel not in exception_channels:
                not_allow = message.content
                if "https://tenor.com" in not_allow or "https://media.tenor.co" in not_allow or "https://c.tenor.com" in not_allow:
                    await message.delete()
        except:
            pass

def setup(client):
    client.add_cog(gifFilter(client))
