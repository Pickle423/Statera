import nextcord, os, json
from nextcord.ext import commands

#welcomeMessage Cog
class WelcomeMessage(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        if f"{member.guild.id}-welcome.json" in os.listdir(f'{origin}/jsons/WMServers'):
            with open(f'{origin}/jsons/WMServers/{member.guild.id}-welcome.json') as json_file:
                guilddata = json.load(json_file)
        else:
            return
        channel = self.client.get_channel(guilddata['channel'])
        message = guilddata['message']
        try:
            namespace = {'mention' : member.mention, 'username' : member.name, 'server' : member.guild.name}
            message = message.format(**namespace)
        except:
            return
        print(message)
        await channel.send(message)


    @nextcord.slash_command(name='welcome',description="Set's the server's welcome message.")
    @commands.has_permissions(administrator=True)
    async def setMessage(self, ctx, channel: str, message: str):
        await ctx.response.defer()
        guilddata = dict()
        try:
            intc = int(channel)
            channel = nextcord.utils.get(ctx.guild.text_channels, id=intc)
        except:       
            channel = nextcord.utils.get(ctx.guild.text_channels, name=channel)
        if channel == None:
            return ctx.followup.send("Failed to find named channel, try an ID.")
        #Try the formatting done at time of use to make sure unauthorized keys aren't in place.
        try:
            namespace = {'mention' : 'test', 'username' : 'test', 'server' : 'test'}
            message.format(**namespace)
        except:
            return ctx.followup.send('Unauthorized keys used, you are limited to mention, username, and server.')
        guilddata['channel'] = channel.id
        guilddata['message'] = message
        self.saveData(ctx.guild.id, guilddata)
        await ctx.followup.send("Message successfully set.")

    # Dumps data to json
    def saveData(self, server, data):
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        with open(f'{origin}/jsons/WMServers/{server}-welcome.json', 'w') as f:
            json.dump(data, f)
    
def setup(client):
    client.add_cog(WelcomeMessage(client))