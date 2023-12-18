
import nextcord, re, os.path, json
from nextcord.ext import commands, tasks

#Guild object to represent servers
class vcGuild:
    def __init__(self, guildid, newSessionID, textChannel):
        self.guildID = guildid
        self.newSession = newSessionID
        self.locked_voice_channels = []
        self.created_voice_channels = {}
        self.textChannel = textChannel
        self.Settings = {}
        #TODO Add working settings.

    def __del__(self):
        print(f"{self.guildid}'s autoVC object destroyed.")

#autoVoiceChannels Cog
class autoVoiceChannels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.VCGuilds = {}
        # Start the cleaner at cog load
        self.cleaner.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        #Read the pre-existing JSON
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        for file in os.listdir(f'{origin}/jsons/VCServers'):
            if 'json' in file:
                parts = file.split('-')
                with open(f'{origin}/jsons/VCServers/{file}') as json_file:
                    #self.database = self.update_dict(self.database, {parts[0] : json.load(json_file)})
                    #TODO: Load guilds from file
                    #print(json.load(json_file))
                    #self.VCGuilds.append(vcGuild(self, parts[0], ))
                    pass

    # Check and delete channels with less than 1 members every 5 mins
    @tasks.loop(minutes=5)
    async def cleaner(self):
        # Iterate through all created channels and clean them.
        for guildObjKey in self.VCGuilds:
            print("At guild " + str(guildObjKey))
            for channelKey in self.VCGuilds[guildObjKey].created_voice_channels:
                channel = await self.client.fetch_channel(self.VCGuilds[guildObjKey].created_voice_channels[channelKey])
                if len(channel.members) <  1:
                    await channel.delete()
                    self.VCGuilds[guildObjKey].created_voice_channels.pop(channelKey)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # Ignore mute/unmute events and Leave events
        if before.channel == after.channel or after.channel == None:
            return
        print("Made it past mute event check.")
        
        # Return guild object from self.VCGuilds
        # At the same time, discover if guild even has autoVC enabled.
        if member.guild.id in self.VCGuilds:
            guildObj = self.VCGuilds[member.guild.id]
        else:
            print("Guild not found.")
            return
        print("Made it past guild check.")

        # When member leaves a locked channel, update the user limit or remove channel
        for locked_channel in guildObj.locked_voice_channels:
            if before.channel.id == locked_channel:
                if len(before.channel.members) < 1:
                    guildObj.locked_voice_channels.remove(before.channel.id)
                await before.channel.edit(user_limit=len(before.channel.members))

        # TODO: TEST THIS

        for channelKey in self.VCGuilds[member.guild.id].created_voice_channels:
            if self.VCGuilds[member.guild.id].created_voice_channels[channelKey] in before.guild.channels:
                self.VCGuilds[member.guild.id].created_voice_channels.remove(channelKey)
        
        # THIS ^

        print("Made it past locked channels")
        if after.channel.id == guildObj.newSession:
            newChannelID = None
            for i in range(1, 6):
                if i not in guildObj.created_voice_channels:
                    newChannelID = i
                    break
            else:
                textChannel = nextcord.utils.get(await member.guild.fetch_channels(), id=guildObj.textChannel)
                await textChannel.send("There are currently 5 active sessions, please wait for old ones to be cleaned before creating a new session. \nIf you believe this to be in error, please report this to the support server.")
                return
            # Create channel and append to created_voice_channels
            channel_name = f"#{newChannelID} [General]"
            created_channel = await member.voice.channel.clone(name=channel_name, reason=None)
            guildObj.created_voice_channels[newChannelID] = created_channel.id

            # Move created channel to beginning and move member into it
            await created_channel.move(beginning=True, reason="Automatic")
            await member.move_to(created_channel)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def destroy(self, ctx, *, channel_name):
        channel_name = nextcord.utils.get(ctx.guild.voice_channels, name=channel_name)
        await channel_name.delete()
        self.VCGuilds[ctx.guild.id].created_voice_channels.pop(channel_name.id)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupVC(self, ctx, newSessionID):
        self.VCGuilds[ctx.guild.id] = vcGuild(ctx.guild.id, int(newSessionID), ctx.channel.id)
        await ctx.send("The Auto-Voice channels feature has been enabled in this discord!")

    @commands.command()
    async def limit(self, ctx, limiter):
        for channel in self.VCGuilds[ctx.guild.id].created_voice_channels:
            if self.VCGuilds[ctx.guild.id].created_voice_channels[channel] == ctx.message.author.voice.channel.id:
                break
        else:
            await ctx.send("Permanent Discord channels cannot be locked.")
            return
        if  limiter.lower() == 'none' or int(limiter) < 1:
            await ctx.message.author.voice.channel.edit(user_limit=0)
        else:
            limiter = int(limiter)
            await ctx.message.author.voice.channel.edit(user_limit=limiter)

    @commands.command()
    async def lock(self, ctx):
        # TODO: Lock function needs new way to determine if it's a permanent channel.
        authors_voice_channel = ctx.message.author.voice.channel
        if authors_voice_channel.id in self.VCGuilds[ctx.guild.id].locked_voice_channels:
            await ctx.send("Channel already locked.")
            return
        for channel in self.VCGuilds[ctx.guild.id].created_voice_channels:
            print("For iteration " + str(channel))
            if self.VCGuilds[ctx.guild.id].created_voice_channels[channel] == authors_voice_channel.id:
                print("About to break.")
                break
        else:
            await ctx.send("Permanent Discord channels cannot be locked.")
            return
        
        self.VCGuilds[ctx.guild.id].locked_voice_channels.append(authors_voice_channel.id)
        await authors_voice_channel.edit(user_limit=len(authors_voice_channel.members))

    @commands.command()
    async def unlock(self, ctx):
        authors_voice_channel = ctx.message.author.voice.channel
        if (authors_voice_channel.id in self.VCGuilds[ctx.guild.id].locked_voice_channels):
            self.VCGuilds[ctx.guild.id].locked_voice_channels.remove(authors_voice_channel.id)
            await authors_voice_channel.edit(user_limit=0)

    @commands.command(aliases=['ren', 'rn'])
    async def rename(self, ctx, *, new_name):
        authors_voice_channel = ctx.message.author.voice.channel
        for channel in self.VCGuilds[ctx.guild.id].created_voice_channels:
            if self.VCGuilds[ctx.guild.id].created_voice_channels[channel] == authors_voice_channel.id:
                break
        else:
            await ctx.send("Permanent Discord channels cannot be locked.")
            return
        if len(new_name) > 19:
            await ctx.send('New name is too long! Please limit it to 19 characters or less.')
            return
        number = int(re.search(r'\d+', authors_voice_channel.name).group())
        try:
            await authors_voice_channel.edit(name=f"#{number} [{new_name}]")
            await ctx.send(f"Channel renamed to #{number} [{new_name}]")
        except:
            await ctx.send('An error was encountered attempting to edit the channel name.')

        

def setup(client):
    client.add_cog(autoVoiceChannels(client))
