from discord.ext import commands, tasks
import discord

from Canvas.CanvasManager import CanvasManager


async def shouldPost(assignment, channel):
    async for m in channel.history(limit=20):
        for e in m.embeds:
            if e.description.find(assignment.name) != -1:
                # Message has already been posted. Don't send again.
                return False
    return True


class classCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canvas = CanvasManager()
        self.checkClasses.start()

    @commands.command()
    async def delete(self, ctx):
        toDelete = []
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                async for m in channel.history(limit=20):
                    if m.author.bot:
                        toDelete.append(m)
        for m in toDelete:
            await m.delete()


    @tasks.loop(seconds=7200.0)
    async def checkClasses(self):
        upcoming, haventSeen = self.canvas.getUpcomingAssignments()
        for courseID in haventSeen.keys():
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

                        print("\tChannel Found!")
                        if not await shouldPost(assignment, channel):
                            print("\tMessage Already Exists. Not Posting")
                            return

                        dueDate = assignment.due_at.strftime('%m/%d/%Y\t%H:%M:%S')
                        embed = discord.Embed(
                            title='%s has a NEW assigment!' % word,
                            url=assignment.html_url,
                            description='```Course Title:\n\t%s\n\n\t'
                                        'Name   :\t%s\n\t'
                                        'DueDate:\t%s\n\t```' % (
                                            courseName.replace('\n', ''), assignment.name, dueDate
                                        ),
                            color=discord.Colour.gold()
                        )
                        await channel.send(embed=embed)

