import nextcord, json, collections, os.path#, datetime, re
from collections.abc import Mapping
#from datetime import datetime
from nextcord.ext import commands
from typing import Optional
#autoSlot Cog
class autoSlot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.database = dict()

    @commands.Cog.listener()
    async def on_ready(self):
        #Read the pre-existing JSON
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        for file in os.listdir(f'{origin}/jsons/ASServers'):
            if 'json' in file:
                parts = file.split('-')
                with open(f'{origin}/jsons/ASServers/{file}') as json_file:
                    self.database = self.update_dict(self.database, {parts[0] : json.load(json_file)})

    @nextcord.slash_command(name='addmission',description="Admin Only, create missions.")
    @commands.has_permissions(administrator=True)
    async def addMission(self, ctx, mission_name: str, mission_timestamp: Optional[int] = nextcord.SlashOption(required=False)):
        await ctx.response.defer()
        if mission_timestamp == None:
            mission_timestamp = 1
        if str(ctx.guild_id) not in self.database:
            self.database.update({str(ctx.guild_id) : {'operations' : {}}})
        mission_id = None
        for i in range(1, 11):
            if str(i) not in self.database[str(ctx.guild_id)]['operations']:
                mission_id = str(i)
                break
        else:
            await ctx.followup.send("There are currently 10 active missions on ID's 1-10. Please delete old missions.")
            return
        # Make channel name that is compatible with discord's channel restrictions
        mission_name_converted = mission_name.replace(" ", "-").lower()


        # Warn user that mission name is converted for discord channel restrictions
        reply = ''
        if (mission_name != mission_name_converted):
            reply = "Your mission's channel will be renamed from {} to {} \n".format(mission_name, mission_name_converted)

        # Add mission to database
        self.database[str(ctx.guild_id)]['operations'].update({str(mission_id) : {'groups' : {}, 'assignments' : {}, 'channel_name' : mission_name_converted, 'name' : mission_name,'author' : ctx.user.id, 'mission_timestamp' : mission_timestamp} })
        self.saveData(str(ctx.guild_id))

        # Notify user
        await ctx.followup.send(reply + f"You have added a new mission. Your mission ID for {mission_name_converted} is: {mission_id}")

    @nextcord.slash_command(name='addslots',description="Admin Only, add slots to an existing mission.")
    @commands.has_permissions(administrator=True)
    async def addSlots(self, ctx, mission_id : str, *, slots):
        await ctx.response.defer()
        # Check if mission ID exists
        try:
            if mission_id not in self.database[str(ctx.guild_id)]['operations']:
                return await ctx.followup.send("There is no mission present in the database with this ID.")
        except:
            return await ctx.followup.send("A problem occured with the mission id.")

        # Parse slots into a list of the groups and a dictionary of all the slots
        group_list, group_dict = self.parseStringToGroups(slots)

        # Check parse was successful
        if group_list is False:
            return await ctx.followup.send("Your request did not match the required formatting, please check your input for issues.")

        # Save groups to database under specific mission id
        #self.database = self.updateDict(self.database, {'operations' : {mission_id : {'groups' : group_dict}}})
        self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'] = group_dict

        # Look for the roster_category and roster_channel
        roster_channel = None
        channel_name = self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']

        # Look for roster category. If it doesnt exist, create it
        roster_category = None
        for category in ctx.guild.categories:
            if category.name == 'statera-rosters':
                roster_category = category
                break

        # If no roster_category is found, create it
        if roster_category == None:
            overwrites = {
                    ctx.guild.default_role: nextcord.PermissionOverwrite(send_messages=False),
                    ctx.guild.me: nextcord.PermissionOverwrite(send_messages=True)
                    }
            roster_category = await ctx.guild.create_category('statera-rosters', overwrites=overwrites)

        # Once created, look for the mission channel. Otherwise, create it
        for channel in roster_category.channels:
            if channel.name == (f"{mission_id}-{channel_name}"):
                roster_channel = channel
                break

        # Post the roster
        # If channel doesnt exist, make the channel and post the first roster in it
        if roster_channel == None:
            roster_channel = await roster_category.create_text_channel(f'{mission_id}-{channel_name}')

        # Parse groups into an embed roster
        embed_roster_message = self.embedGroupsToRoster(ctx, mission_id, group_list)
        if embed_roster_message == None:
            #TODO: Move slotname checking to parseStringToGroups instead of embedGroupsToRoster
            self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'] = {}
            return await ctx.followup.send("Please limit the length of a slotname to 25, the number of slots in a single group to 20, and the number of groups to 10.")

        # If previous roster exists, edit it with the embed_roster_message
        if await roster_channel.history().get(author__id = self.client.user.id):
            previous_roster_message = await roster_channel.history().get(author__id = self.client.user.id)
            await previous_roster_message.edit(embed=embed_roster_message)
        # Else, just send the embed_roster_message
        else:
            await roster_channel.send(embed=embed_roster_message)

        self.saveData(str(ctx.guild_id))

        # Notify user
        await ctx.followup.send(f"You have added slots to {self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}.")

    @nextcord.slash_command(name='slot',description="Assign yourself to a slot, admins can assign others to a slot by mentioning them.")
    async def aslot(self, ctx, mission_id, slot_id, target: Optional[str] = nextcord.SlashOption(required=False)):
        await ctx.response.defer()
        # Check target user if they exist
        if target:
            # If author is not authorized, stop execution
            if ctx.user.guild_permissions.manage_messages != True:
                 return await ctx.followup.send('You do not have permission to assign others to a slot.')
            # Find and set ctx.user to target
            ctx.user = ctx.guild.get_member(int(target.translate({ord(i): None for i in '@<>'})))
            # Check if target user exists
            if ctx.user == None:
                await ctx.followup.send("Failed to find user.")

        # Check if mission exists
        if self.database[str(ctx.guild_id)]['operations'].get(mission_id) == None:
            return await ctx.followup.send(f"Mission ID {mission_id} not found.")

        # Pull list of groups and dictionary of roles
        group_list =[]
        slot_dict = {}
        for group in self.database[str(ctx.guild_id)]['operations'][mission_id]['groups']:
            group_list.append(group)
            slot_dict.update(self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'][group])

        # Check if slot exists
        if slot_dict.get(slot_id) == None:
            return await ctx.followup.send(f"Slot ID {slot_id} not found.")
        # Check if slot already has user
        if self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments'].get(slot_id):
            return await ctx.followup.send("Please remove the person from this slot before trying to claim it.")
        # Check if user already has a slot
        for slot in self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments']:
            if ctx.user.id == self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments'].get(slot):
                return await ctx.followup.send(f"You can only claim one slot at a time.")

        # Update database with new assignment
        #self.database = self.updateDict(self.database, {'operations' : {mission_id : {'assignments' : {slot_id : user.id}}}})
        self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments'][slot_id] = ctx.user.id


        # Check if roster_category exists, otherwise create it
        roster_category = None
        for category in ctx.guild.categories:
            if category.name == 'statera-rosters':
                roster_category = category
                break
        if roster_category == None:
            return await ctx.followup.send("No channel can be found for this mission can be found. Have roles been added yet?")

        # Edit embed 
        roster_channel = nextcord.utils.get(ctx.guild.channels, name=f"{mission_id}-{self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}", category=roster_category)
        message = await roster_channel.history().get(author__id = self.client.user.id)
        await message.edit(embed=self.embedGroupsToRoster(ctx, mission_id, group_list))
        self.saveData(str(ctx.guild_id))

        # Notify user
        await ctx.followup.send(f"You have taken slot {slot_id} in {self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}.")

    @nextcord.slash_command(name='rslot',description="Remove an assignment from a slot.")
    async def rslot(self, ctx, mission_id, slot_id):
        await ctx.response.defer()
        # Check if mission exists
        if self.database[str(ctx.guild_id)]['operations'].get(mission_id) == None:
            return await ctx.followup.send(f"Mission ID {mission_id} not found.")

        # Pull list of groups and dictionary of roles
        group_list =[]
        slot_dict = {}
        for group in self.database[str(ctx.guild_id)]['operations'][mission_id]['groups']:
            group_list.append(group)
            slot_dict.update(self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'][group])

        # Check if slot exists
        if slot_dict.get(slot_id) == None:
            return await ctx.followup.send("Slot not found.")

        # Delete user from database
        if self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments'].get(slot_id) != ctx.user.id:
            if ctx.user.guild_permissions.manage_messages != True:
                 return await ctx.followup.send('You do not have permission to remove others from a slot.')
        del self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments'][slot_id]

        # Check if roster_category exists, otherwise create it
        roster_category = None
        for category in ctx.guild.categories:
            if category.name == 'statera-rosters':
                roster_category = category
                break
        if roster_category == None:
            return await ctx.followup.send("No channel can be found for this mission can be found. Have roles been added yet?")

        # Edit embed 
        roster_channel = nextcord.utils.get(ctx.guild.channels, name=f"{mission_id}-{self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}", category=roster_category)
        message = await roster_channel.history().get(author__id = self.client.user.id)
        await message.edit(embed=self.embedGroupsToRoster(ctx, mission_id, group_list))
        self.saveData(str(ctx.guild_id))

        # Notify user
        await ctx.followup.send(f"You have removed target from slot {slot_id} in {self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}.")

    
    @nextcord.slash_command(name='rslotall',description="Admin Only. Remove all assignments from all slot.")
    @commands.has_permissions(administrator=True)
    async def rslotAll(self, ctx, mission_id):
        await ctx.response.defer()
        # Check if mission exists
        if self.database[str(ctx.guild_id)]['operations'].get(mission_id) == None:
            return await ctx.followup.send(f"Mission ID {mission_id} not found.")

        # Pull list of groups and dictionary of roles
        group_list =[]
        #slot_dict = {}
        for group in self.database[str(ctx.guild_id)]['operations'][mission_id]['groups']:
            group_list.append(group)
            #slot_dict.update(self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'][group])

        # Reset assignments to empty
        self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments'] = {}

        # Check if roster_category exists, otherwise create it
        roster_category = None
        for category in ctx.guild.categories:
            if category.name == 'statera-rosters':
                roster_category = category
                break
        if roster_category == None:
            return await ctx.followup.send("No channel can be found for this mission can be found. Have roles been added yet?")

        # Edit embed 
        roster_channel = nextcord.utils.get(ctx.guild.channels, name=f"{mission_id}-{self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}", category=roster_category)
        message = await roster_channel.history().get(author__id = self.client.user.id)
        await message.edit(embed=self.embedGroupsToRoster(ctx, mission_id, group_list))
        self.saveData(str(ctx.guild_id))

        # Notify user
        await ctx.followup.send(f"You removed all assignments from {self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}.")

    # Remove mission
    @nextcord.slash_command(name='deletemission',description="Admin only, delete a mission.")
    @commands.has_permissions(administrator=True)
    async def deleteMission(self, ctx, mission_id : str):
        await ctx.response.defer()
        # Check if mission exists
        if self.database[str(ctx.guild_id)]['operations'].get(mission_id) == None:
            return await ctx.followup.send(f"Mission ID {mission_id} not found.")

        # Check if roster_category exists, otherwise create it
        roster_category = None
        for category in ctx.guild.categories:
            if category.name == 'statera-rosters':
                roster_category = category
                break

        # Delete mission channel
        if roster_category:
            channel = nextcord.utils.get(ctx.guild.channels, name=f"{mission_id}-{self.database[str(ctx.guild_id)]['operations'][mission_id]['channel_name']}", category=roster_category)
            if channel:
                await channel.delete()
                await ctx.followup.send("Channel deleted.")
        # Remove mission channel in database
        del self.database[str(ctx.guild_id)]['operations'][mission_id]
        self.saveData(str(ctx.guild_id))

        # Notify user
        await ctx.followup.send(f"Mission removed!")

    @nextcord.slash_command(name='missions',description="List missions active in server.")
    async def missions(self, ctx):
        embed = nextcord.Embed(title=f"{str(ctx.guild.name)}'s Missions:", description=f"Called by: {ctx.user.name}")
        for mission in self.database[str(ctx.guild_id)]['operations']:
            embed.add_field(name=f"{mission}-{self.database[str(ctx.guild_id)]['operations'][mission]['name']}", value=f"By: {nextcord.utils.get(ctx.guild.members, id=self.database[str(ctx.guild_id)]['operations'][mission]['author'])}", inline=False)
        await ctx.response.send_message(embed=embed)

    # Dumps data to autoSlot.json
    def saveData(self, server):
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        with open(f'{origin}/jsons/ASServers/{server}-autoSlot.json', 'w') as f:
            json.dump(self.database[server], f)

    #Convert to produce embed, with fields acting as group. Character limit is 1024, so limit groups to be 500.
    def embedGroupsToRoster(self,ctx, mission_id, group_dict):
        slots = ""
        assignments = self.database[str(ctx.guild_id)]['operations'][mission_id]['assignments']
        if self.database[str(ctx.guild_id)]['operations'][mission_id]['mission_timestamp'] != 1:
            long_mission_timestamp = "<t:" + str(self.database[str(ctx.guild_id)]['operations'][mission_id]['mission_timestamp']) + ":F>" #nextcord.utils.format_dt(self.database[str(ctx.guild_id)]['operations'][mission_id]['mission_timestamp'], style="F")
            relative_mission_timestamp = "<t:" + str(self.database[str(ctx.guild_id)]['operations'][mission_id]['mission_timestamp']) + ":R>" #nextcord.utils.format_dt(self.database[str(ctx.guild_id)]['operations'][mission_id]['mission_timestamp'], style="R")
            slot_embed = nextcord.Embed(title=f"{self.database[str(ctx.guild_id)]['operations'][mission_id]['name']}", description=f"By: {ctx.guild.get_member(self.database[str(ctx.guild_id)]['operations'][mission_id]['author']).mention}\n {long_mission_timestamp}, {relative_mission_timestamp}\n Mission ID: {mission_id}", color=0x0E8643)
        else:
            slot_embed = nextcord.Embed(title=f"{self.database[str(ctx.guild_id)]['operations'][mission_id]['name']}", description=f"By: {ctx.guild.get_member(self.database[str(ctx.guild_id)]['operations'][mission_id]['author']).mention}\n Mission ID: {mission_id}", color=0x0E8643)
        
        if len(group_dict) > 10:
            return None
        for group in group_dict:
            slots = ""
            slot_dict = self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'][group]
            if len(slot_dict) > 20:
                return None
            for slot in slot_dict:
                if len(slot) > 25:
                    return None
                if assignments.get(slot) == None:
                    slots = slots + (f"{slot}: {self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'][group][slot]}\n")
                else:
                    slots = slots + (f"{slot}: {self.database[str(ctx.guild_id)]['operations'][mission_id]['groups'][group][slot]} - {ctx.guild.get_member(assignments.get(slot)).mention}\n")
            slot_embed.add_field(name=group, value=slots, inline=False)
        return slot_embed

    # Parse inputted slots into autoSlot format
    def parseStringToGroups(self,data):
        if ':' not in data:
            return False, False
        if data[-1] == ',':
            data = data.rstrip(data[-1])
            data = data + '.'
        elif data[-1] != '.':
            data = data + '.'
        data_list = data.split(" ")
        temp = ""
        group_list = []
        temp_list = []
        group_dict = {}
        for i in data_list:
            temp = temp + f'{i} '
            if ':' in i:
                temp = temp.rstrip(temp[-1])
                temp = temp.rstrip(temp[-1])
                group_list.append(temp)
                group_dict.update({temp : 'placeholder'})
                temp = ""
            if ',' in i:
                temp = temp.rstrip(temp[-1])
                temp = temp.rstrip(temp[-1])
                if temp != "":
                    temp_list.append(temp)
                    temp = ""
            if '.' in i:
                temp = temp.rstrip(temp[-1])
                temp = temp.rstrip(temp[-1])
                if temp != "":
                    temp_list.append(temp)
                    if len(group_list) > 0:
                        group_dict.update({group_list[len(group_list) - 1] : temp_list})
                    else:
                        group_dict.update({group_list[0] : temp_list})
                    temp = ""
                    temp_list = []
        group_alt = {}
        slots = {}
        slot_counter = 1
        for group in group_list:
            for slot in group_dict[group]:
                slots.update({str(slot_counter) : slot})
                slot_counter = slot_counter + 1
            group_alt.update({group : slots})
            slots = {}
        group_dict = group_alt
        return group_list, group_dict

    def update_dict(self, d, u):
        for k, v in u.items():
            if isinstance(v, Mapping):
                default = v.copy()
                default.clear()
                r = self.update_dict(d.get(k, default), v)
                d[k] = r
            else:
                d[k] = v
        return d

def setup(client):
    client.add_cog(autoSlot(client))