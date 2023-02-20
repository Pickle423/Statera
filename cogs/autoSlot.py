import nextcord, sys, datetime, json, collections, os.path
from nextcord.ext import commands

global database
database = {}
#autoSlot Cog
class autoSlot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
     
    @commands.Cog.listener()
    async def on_ready(self):
        #Read the pre-existing JSON
        global database
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        for file in os.listdir(f'{origin}/jsons/ASServers'):
            if 'json' in file:
                parts = file.split('-')
                with open(f'{origin}/jsons/ASServers/{file}') as json_file:
                    database = update_dict(database, {parts[0] : json.load(json_file)})

    @commands.command(name = "addMission", help = "Adds a new mission with given name. Use quotations for multi-word names")
    @commands.has_permissions(administrator=True)
    async def addMission(self, ctx, mission: str, date: str = "", time: str = ""):
        global database
        if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to create a mission')
                return
        #Make channel name that is compatible with discord's channel restrctions
        c = nameconvert(mission)
        missionoriginal = mission
        if (mission != c):
            await ctx.send("{} Your mission's channel will be renamed from {} to {}".format(ctx.author.mention, mission, c))
            mission = c
        if str(ctx.guild.id) not in database:
            database.update({str(ctx.guild.id) : {'operations' : {}}})
        mission_id = None
        for i in range(1, 11):
            if str(i) not in database[str(ctx.guild.id)]['operations']:
                mission_id = str(i)
                break
        else:
            await ctx.send("There are currently 10 active missions on ID's 1-10. Please delete old missions.")
            return
        database[str(ctx.guild.id)]['operations'].update({mission_id : {'groups' : {},'assignments' : {}, 'channelname' : mission, 'name' : missionoriginal,'author' : ctx.author.id,'date' : date,'time' : time} })

        send_message = "{} Your mission ID for {} is: {}".format(ctx.author.mention, mission, mission_id)
        await ctx.send(send_message)
        saveData(str(ctx.guild.id))

    @commands.command(name = "addslots")
    @commands.has_permissions(administrator=True)
    async def addSlots(self, ctx, id, *, slots):
        global database
        if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to add slots to a mission.')
                return
        try:
            if id not in database[str(ctx.guild.id)]['operations']:
                await ctx.send("There is no mission present in the database with this ID.")
                return
        except:
            await ctx.send("A problem occured with the mission id.")
            return
        grouplist, groupdict = parser(slots)
        if grouplist == False:
            await ctx.send("Your request did not match the required formatting, please check your input for issues.")
            return
        backup = database[str(ctx.guild.id)]['operations'][id]['groups']
        database = update_dict(database, {str(ctx.guild.id) : {'operations' : {id : {'groups' : groupdict}}}})
        server = ctx.guild
        categories = server.categories
        missionscategory = None
        missionchannel = None
        cname = database[str(ctx.guild.id)]['operations'][id]['channelname']
        for c in categories:
            if c.name == 'statera-missions':
                missionscategory = c
                break
        if missionscategory == None:
            missionscategory = await server.create_category('statera-missions')
        else:
            for c in missionscategory.channels:
                if c.name == (f"{id}-{cname}"):
                    missionchannel = c
                    break
        if missionchannel == None:
            missionchannel = await missionscategory.create_text_channel(f'{id}-{cname}')
            message = preparemessage(ctx, id, grouplist)
            if message == None:
                database[str(ctx.guild.id)]['operations'][id]['groups'] = {}
                await ctx.send("Please limit the length of a slotname to 25, the number of slots in a single group to 20, and the number of groups to 10.")
                return
            await missionchannel.send(embed=message)
        else:
            message = preparemessage(ctx, id, grouplist)
            if message == None:
                database[str(ctx.guild.id)]['operations'][id]['groups'] = backup
                await ctx.send("Please limit the length of a slotname to 25, the number of slots in a single group to 20, and the number of groups to 10.")
                return
            if await missionchannel.history().get(author__id = self.client.user.id) != None:
                m = await missionchannel.history().get(author__id = self.client.user.id)
            else:
                await missionchannel.send('TEMP')
                m = await missionchannel.history().get(author__id = self.client.user.id)
            '''
            if len(message) > 2000:
                print(message)
                print(len(message))
                database[str(ctx.guild.id)]['operations'][id]['groups'] = backup
                await ctx.send("The requested mission would surpass the Discord character limit, or leave no room for roles to be selected.")
                return
            '''
            await m.edit(embed=message)
        saveData(str(ctx.guild.id))

    @commands.command(aliases=['takeslot', 'claimslot', 'cslot', 'tslot', 'slot','assignslot'])
    async def aslot(self, ctx, missionid, slotid, target=None):
        global database
        user = ctx.author
        if target != None:
            if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to remove the slot of someone other than yourself.')
                return
            user = ctx.guild.get_member(int(target.translate({ord(i): None for i in '@<>'})))
            if user == None:
                await ctx.send("Failed to find user.")         
        if database[str(ctx.guild.id)]['operations'].get(missionid) == None:
            await ctx.send(f"MissionID of {missionid} not found.")
            return
        grouplist = []
        slotdict = {}
        for group in database[str(ctx.guild.id)]['operations'][missionid]['groups']:
            grouplist.append(group)
        for group in grouplist:
            slotdict.update(database[str(ctx.guild.id)]['operations'][missionid]['groups'][group])
        if slotdict.get(slotid) == None:
            await ctx.send("Slot not found.")
            return
        if database[str(ctx.guild.id)]['operations'][missionid]['assignments'].get(slotid) != None:
            await ctx.send("Please remove the person from this slot before trying to claim it.")
        #Update method we were using to avoid this broke for some reason so now we have this.
        database = update_dict(database, {str(ctx.guild.id) : {'operations' : {missionid : {'assignments' : {slotid : user.id}}}}})
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'statera-missions':
                missionscategory = c
                break
        if missionscategory == None:
            await ctx.send("No channel can be found for this mission can be found. Have roles been added yet?")
            return
        channel = nextcord.utils.get(ctx.guild.channels, name=f"{missionid}-{database[str(ctx.guild.id)]['operations'][missionid]['channelname']}", category=missionscategory)
        m = await channel.history().get(author__id = self.client.user.id)
        await m.edit(embed=preparemessage(ctx, missionid, grouplist))
        saveData(str(ctx.guild.id))

    @commands.command(aliases=['deslot','removeslot'])
    async def rslot(self, ctx, missionid, slotid):
        global database
        if database[str(ctx.guild.id)]['operations'].get(missionid) == None:
            await ctx.send(f"MissionID of {missionid} not found.")
            return    
        grouplist = []
        slotdict = {}
        for group in database[str(ctx.guild.id)]['operations'][missionid]['groups']:
            grouplist.append(group)
        for group in grouplist:
            slotdict.update(database[str(ctx.guild.id)]['operations'][missionid]['groups'][group])
        if slotdict.get(slotid) == None:
            await ctx.send("Slot not found.")
            return
        if database[str(ctx.guild.id)]['operations'][missionid]['assignments'].get(slotid) != ctx.author.id:
            if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to remove the slot of someone other than yourself.')
                return
        del database[str(ctx.guild.id)]['operations'][missionid]['assignments'][slotid]
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'statera-missions':
                missionscategory = c
                break
        if missionscategory == None:
            await ctx.send("No channel can be found for this mission can be found. Have roles been added yet?")
            return
        channel = nextcord.utils.get(ctx.guild.channels, name=f"{missionid}-{database[str(ctx.guild.id)]['operations'][missionid]['channelname']}", category=missionscategory)
        m = await channel.history().get(author__id = self.client.user.id)
        await m.edit(embed=preparemessage(ctx, missionid, grouplist))
        saveData(str(ctx.guild.id))

    @commands.command(aliases=['delmission', 'delmis', 'rmmission', 'removemission'])
    @commands.has_permissions(administrator=True)
    async def deletemission(self, ctx, id):
        global database
        if database[str(ctx.guild.id)]['operations'].get(id) == None:
            await ctx.send("No mission found with that ID.")
            return
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'statera-missions':
                missionscategory = c
                break
        if missionscategory != None:
            channel = nextcord.utils.get(ctx.guild.channels, name=f"{id}-{database[str(ctx.guild.id)]['operations'][id]['channelname']}", category=missionscategory)
            if channel != None:
                await channel.delete()
                await ctx.send("Channel deleted.")
        del database[str(ctx.guild.id)]['operations'][id]
        await ctx.send(f"{ctx.author.mention}Mission removed!")
        saveData(str(ctx.guild.id))

#Centralized function for saving data.
def saveData(server):
    origin = os.path.abspath('')
    origin = origin.replace('\\', "/")
    with open(f'{origin}/jsons/ASServers/{server}-autoSlot.json', 'w') as f:
        json.dump(database[server], f)

def preparemessage(ctx, id, grouplist):
    #Convert to produce embed, with fields acting as group. Character limit is 1024, so limit groups to be 500.
    slots = ""
    assignments = database[str(ctx.guild.id)]['operations'][id]['assignments']
    slotEmbed = nextcord.Embed(title=f"{database[str(ctx.guild.id)]['operations'][id]['name']}", description=f"By: {ctx.guild.get_member(database[str(ctx.guild.id)]['operations'][id]['author']).mention} \n {database[str(ctx.guild.id)]['operations'][id]['date']}, {database[str(ctx.guild.id)]['operations'][id]['time']}", color=0x0E8643)
    if len(grouplist) > 10:
        return None
    for group in grouplist:
        slots = ""
        slotdict = database[str(ctx.guild.id)]['operations'][id]['groups'][group]
        if len(slotdict) > 20:
            return None
        for slot in slotdict:
            if len(slot) > 25:
                return None
            if assignments.get(slot) == None:
                slots = slots + (f"{slot}: {database[str(ctx.guild.id)]['operations'][id]['groups'][group][slot]}\n")
            else:
                slots = slots + (f"{slot}: {database[str(ctx.guild.id)]['operations'][id]['groups'][group][slot]} - {ctx.guild.get_member(assignments.get(slot)).mention}\n")
        slotEmbed.add_field(name=group, value=slots, inline=False)
    '''
    for group in grouplist:
        slots = slots + (f"\n**{group}:**\n")
        slotdict = database[str(ctx.guild.id)]['operations'][id]['groups'][group]
        for slot in slotdict:
            if assignments.get(slot) == None:
                slots = slots + (f"{slot}: {database[str(ctx.guild.id)]['operations'][id]['groups'][group][slot]}\n")
            else:
                slots = slots + (f"{slot}: {database[str(ctx.guild.id)]['operations'][id]['groups'][group][slot]} - {ctx.guild.get_member(assignments.get(slot)).mention}\n")
    message = f"{database[str(ctx.guild.id)]['operations'][id]['name']} \n By: {ctx.guild.get_member(database[str(ctx.guild.id)]['operations'][id]['author']).mention} \n {database[str(ctx.guild.id)]['operations'][id]['date']}, {database[str(ctx.guild.id)]['operations'][id]['time']} \n {slots}"
    return message
    '''
    return slotEmbed

def parser(data):
    if ':' not in data:
        return False, False
    if data[-1] == ',':
        data = data.rstrip(data[-1])
        data = data + '.'
    elif data[-1] != '.':
        data = data + '.'
    datalist = data.split(" ")
    temp = ""
    grouplist = []
    templist = []
    groupdict = {}
    for i in datalist:
        temp = temp + f'{i} '
        if ':' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            grouplist.append(temp)
            groupdict.update({temp : 'placeholder'})
            temp = ""
        if ',' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            if temp != "":
                templist.append(temp)
                temp = ""
        if '.' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            if temp != "":
                templist.append(temp)
                if len(grouplist) > 0:
                    groupdict.update({grouplist[len(grouplist) - 1] : templist})
                else:
                    groupdict.update({grouplist[0] : templist})
                temp = ""
                templist = []
    groupalt = {}
    slots = {}
    slotcounter = 1
    for group in grouplist:
        for slot in groupdict[group]:
            slots.update({str(slotcounter) : slot})
            slotcounter = slotcounter + 1
        groupalt.update({group : slots})
        slots = {}
    groupdict = groupalt
    '''
    if temp != "":
        temp = temp.rstrip(temp[-1])
        roledict.update({temp : grouplist[len(grouplist) - 1]})
        temp = ""
        '''
    return grouplist, groupdict

def update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            default = v.copy()
            default.clear()
            r = update_dict(d.get(k, default), v)
            d[k] = r
        else:
            d[k] = v
    return d

def nameconvert(name):
    return name.replace(" ", "-").lower()

def setup(client):
    client.add_cog(autoSlot(client))
