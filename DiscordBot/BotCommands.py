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
                                  'DueDate:\t%s\n\t' \
                                  'URL    :\t%s\n```' % (
                                      word, courseName, assignment.name, dueDate, assignment.html_url
                                  )
                        await channel.send(message)
