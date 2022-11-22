import nextcord
from nextcord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
msg_id = 0
msg = ''
message = []
a = ''
b = ''
c = ''
d = ''
class reactForRoles(commands.Cog):

    def init (self, client):
        self.client = client

    @commands.command()
    async def roleReactMessage(self, context, nameOne, emojiOne, nameTwo, emojiTwo):
        global msgid
        global msg
        global message
        global a,b,c,d


        b = emojiOne

        d = emojiTwo

        nameOne = nameOne.replace('', ' ')
        nameTwo = nameTwo.replace('_', ' ')
        a = nameOne
        c = nameTwo
        await context.channel.purge(limit=1)



        embedMessage = nextcord.Embed(title="React For Roles.", description="React to get your discord role.", color=0x0E8643)
        embedMessage.add_field(name=f"{nameOne}", value=f"React with {emojiOne} for the {nameOne} role.")
        embedMessage.add_field(name=f"{nameTwo}", value=f"React with {emojiTwo} for the {nameTwo} role.", inline=False)
        embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")

        msg = await context.message.channel.send(embed=embedMessage)

        #emojiOne = context.guild.emojis[1]
        #emojiTwo = context.guild.emojis[0]
        #print(message)
        try:
            await msg.add_reaction(emojiOne)
            await msg.add_reaction(emojiTwo)
        except:
            await context.channel.purge(limit=1)
            await context.send('Please Use emojis from this discord')


        msg_id = msg.id
        #print(msg_id)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global msg_id
        global msg
        role = None
        global a,b,c,d
        #print(payload)
        message_id = payload.message_id
        if message_id == msg_id:

            guild_id = payload.guild_id
            guild = nextcord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            member = payload.member
            #print(b.name)
            #print(payload.emoji)
            #print(payload.emoji.name)
            eOne = payload.emoji
            #print(type(b))
            #print(type(eOne))
            if str(eOne) == b:
                #print('e1')
                role = nextcord.utils.get(guild.roles, name = a)
                await member.add_roles(role)
                role = None
                #print('added')
                #print(type(role))
                role = nextcord.utils.get(guild.roles, name = c)
                await member.remove_roles(role)
                role = None
                #print('removed')
                #print(role)



            if str(eOne) == d:
                #print('rfef')
                role = nextcord.utils.get(guild.roles, name = a)
                await member.remove_roles(role)
                role = None
                #print(role)
                role = nextcord.utils.get(guild.roles, name = c)
                await member.add_roles(role)
                role = None
                #print(role)

# !roleReactMessage Operative :seso: Combat_Service_Support :sesoafghan: 

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global msg_id
        global a,b,c,d
        message_id = payload.message_id

        if message_id == msg_id:
            guild_id = payload.guild_id
            guild = nextcord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
            member = nextcord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            eTwo = payload.emoji

            if str(eTwo) == b:
                role = nextcord.utils.get(guild.roles, name = a)

                await member.remove_roles(role)

            elif str(eTwo) == d:
                role = nextcord.utils.get(guild.roles, name = c)
                await member.remove_roles(role)


def setup(client):
    client.add_cog(reactForRoles(client))