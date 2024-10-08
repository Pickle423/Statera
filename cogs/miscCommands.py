import nextcord
from nextcord.ext import commands
import random
class miscCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Simple Ping Check
    @nextcord.slash_command(name='ping',description="Returns a rounded responsetime for the bot.")
    async def ping(self, ctx):
        await ctx.response.send_message(f'Pong! {round(self.client.latency * 1000)}ms')
 
    @nextcord.slash_command(name='8ball',description="Enter a question for the great 8ball.")
    async def _8ball(self, ctx, question: str):
        responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt', 'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', "Don't count on it.", 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        await ctx.response.send_message(f'Question: {question}\nAnswer: {random.choice(responses)}')

    #Calculate
    @nextcord.slash_command(name='calculate',description="Answers your simple math questions.")
    async def calculate(self, ctx, query_first, query_operator, query_second):
        query_first = int(query_first)
        query_second = int(query_second)
        if query_first > 9999999999 or query_second > 9999999999:
            await ctx.response.send_message("Request too high.")
        if (query_operator) == ('+'):
            await ctx.response.send_message(query_first + query_second)
        elif (query_operator) == ('-'):
            await ctx.response.send_message(query_first - query_second)
        elif (query_operator) == ('*'):
            await ctx.response.send_message(query_first * query_second)
        elif (query_operator) == ('/'):
            await ctx.response.send_message(query_first / query_second)
        else:
            ctx.send('Calculation failed, remember to use +, -, *, or /, as well as spacing out the request.')
    
            ''' Future-proofing this command. Python 3.10 has a match-case function that we will use when we switch to 3.10
            match query_operator:
                case '+':
                    await ctx.send(query_first + query_second)
                case '-':
                    await ctx.send(query_first - query_second)
                case '*':
                    await ctx.send(query_first * query_second)
                case '/':
                    await ctx.send(query_first / query_second)
                case _:
                    ctx.send('Calculation failed, remember to use +, -, *, or /, as well as spacing out the request.')
        '''

    @nextcord.slash_command(name='version',description="Provides version information for the bot.")
    async def version(self, context):
        mainEmbed = nextcord.Embed(title="Statera Version Notes", description="The Multi-Use Discord Bot", color=0x0E8643)
        mainEmbed.add_field(name="Changes:", value=f"autoVoiceChannels converted to slash commands.")
        mainEmbed.add_field(name="Version Code:", value="v1.0.0", inline=False)
        mainEmbed.add_field(name="Date Released:", value="May 1, 2024", inline=False)
        mainEmbed.set_footer(text="Statera written by Pickle423#0408 and Fletch#0617.")

        await context.response.send_message(embed=mainEmbed)

    @nextcord.slash_command(name='dice',description="Roll some dice!")
    async def sdice(self, ctx, max: int, num_dice: int=None, operator: str=None, operatornumber: int=1):
        await ctx.response.defer()
        if num_dice != None and num_dice > 10:
            await ctx.followup.send("Please limit the number of dice to 10.")
            return
        elif  max > 1000 or operatornumber > 1000:
            await ctx.followup.send("Please limit numbers to less than 1000.")
            return
        if  num_dice != None:
            whileloop = 0
            diceresults = []
            while whileloop < num_dice:
                whileloop = whileloop + 1
                if operator != None:
                    if operator == '*':
                        diceresults.append(random.randrange(1, max) * operatornumber)
                    elif operator == '+':
                        diceresults.append(random.randrange(1, max) + operatornumber)
                    elif operator == '-':
                        diceresults.append(random.randrange(1, max) - operatornumber)
                    elif operator == '/':
                        diceresults.append(random.randrange(1, max) / operatornumber)
                else:
                    diceresults.append(random.randrange(1, max))
            await ctx.followup.send(f"Rolled {num_dice}d{max} {diceresults}")
        elif operator == None:
            await ctx.followup.send(f"Rolled 1d{max} {random.randrange(1, max)}")
        elif operator == '*':
            await ctx.followup.send(f"Rolled 1d{max} {random.randrange(1, max) * operatornumber}")
        elif operator == '+':
            await ctx.followup.send(f"Rolled 1d{max} {random.randrange(1, max) + operatornumber}")
        elif operator == '-':
            await ctx.followup.send(f"Rolled 1d{max} {random.randrange(1, max) - operatornumber}")
        elif operator == '/':
            await ctx.followup.send(f"Rolled 1d{max} {random.randrange(1, max) / operatornumber}")

    # Likely would have had to be removed to get verified.
    '''
    @commands.command(aliases=["d", "rolldice", "roll"])
    async def dice(self, ctx, max: int, operator=None, *, operatornumber: int=None):
        if operator != None:
            try:
                dice=int(operator)
                operatorisdicecount = True
            except:
                operatorisdicecount = False
        else:
            operatorisdicecount = False
        try:
            if operatorisdicecount == True and operator > 10:
                await ctx.send("Please limit the number of dice to 10.")
                return
            elif  max > 1000 or operatornumber > 1000:
                await ctx.send("Please limit numbers to less than 1000.")
                return
        except:
            pass
        if operatorisdicecount == True:
            whileloop = 0
            diceresults = []
            while whileloop < dice:
                whileloop = whileloop + 1
                diceresults.append(random.randrange(1, max))
            await ctx.send(f"Rolled {operator}d{max} {diceresults}")
        elif operator == None:
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max)}")
        elif operator == '*':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) * operatornumber}")
        elif operator == '+':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) + operatornumber}")
        elif operator == '-':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) - operatornumber}")
        elif operator == '/':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) / operatornumber}")
    '''

def setup(client):
    client.add_cog(miscCommands(client))
