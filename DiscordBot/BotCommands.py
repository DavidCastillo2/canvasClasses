from discord.ext import commands, tasks

from Canvas.CanvasManager import CanvasManager


class classCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canvas = CanvasManager()
        self.checkClasses.start()


    @tasks.loop(seconds=600.0)
    async def checkClasses(self):
        upcoming, haventSeen = self.canvas.getUpcomingAssignments()
        for courseID in haventSeen.keys():
            print(len(haventSeen))
            for ass in haventSeen[courseID]:
                courseName = self.canvas.getCourseName(ass)
                await self.postNewAssignment(courseName, ass)


    async def postNewAssignment(self, courseName, assignment):
        print("Posting New Assignment")
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                channelFirstWord = channel.name.split('-')[0]
                for word in courseName.lower().split(' '):
                    if word.find(channelFirstWord) != -1:
                        print("Channel Found!")
                        dueDate = assignment.due_at.strftime('%m/%d/%Y\t%H:%M:%S')
                        message = '```%s has a NEW assigment!\n\t' \
                                  'Course Title:\t%s\n\n\t' \
                                  'Name   :\t%s\n\t' \
                                  'DueDate:\t%s\n```' % (
                                      word, courseName, assignment.name, dueDate
                                  )
                        await channel.send(message)


'''
    @commands.command()
    async def Arbi(self, ctx):
        arbiData = self.driver.getArbi()
        if arbiData is None:
            await ctx.send("```Current Arbitration data is still being parsed, check back later u lil bitch muffin```")
        else:
            retVal = "```Current Arbitration Information" + '\n__________________________________________\n\n'
            retVal = retVal + "Node: " + arbiData['node']
            retVal = retVal + "\nEnemy Type: " + arbiData['enemy']
            retVal = retVal + "\nType: " + arbiData['type'] + "\n"
            alert = self.arbi.getAlert()
            if alert is None:
                retVal += "Alert Level: NONE"
            else:
                retVal += "Alert Level: " + alert
            retVal += "```"
            await ctx.send(retVal)

    @commands.command()
    async def arbi(self, ctx):
        await self.Arbi(ctx)

    @commands.command()
    async def commands(self, ctx):
        helptext = "```"
        for command in self.commands:
            helptext += f"{command}\n"
        helptext += "\nType !help command for more info on a command"
        helptext += "```"
        await ctx.send(helptext)
'''