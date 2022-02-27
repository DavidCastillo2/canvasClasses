import discord
from discord.ext import commands, tasks

from DiscordBot.BotCommands import classCommands


class MyBot(commands.Bot):

    def __init__(self, command_prefix="!", **options):
        super().__init__(command_prefix, **options)
        self.key = 'OTQ3Mjg5Nzg2ODU3NzA5NjA4.YhrGXA.q5Xquo9KrvYU8VBvOPYD5UD1qcM'
        # self.loadCogs()

    def begin(self):
        self.run(self.key)

    def loadCogs(self):
        self.add_cog(classCommands(self))

    async def on_ready(self):
        # Load stupid fucking cuckload opus library
        if discord.opus.is_loaded():
            self.loadCogs()
            print('Logged in as ' + self.user.name + "\n\n")
            return
        try:
            discord.opus._load_default()
            self.loadCogs()
            print('Logged in as ' + self.user.name + "\n\n")
            return
        except OSError:
            pass
            print('\n\nERROR\n\nLogged in as ' + self.user.name + "\n\n")



if __name__ == "__main__":
    b = MyBot(command_prefix="!")
    b.begin()


