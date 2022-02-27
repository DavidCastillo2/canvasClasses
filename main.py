from Calendar.CalendarManager import CalendarManager
from Canvas.CanvasWrapper import CanvasWrapper
from DiscordBot.theBot import MyBot

testing = True


if not testing:
    b = MyBot(command_prefix="!")
    b.begin()


else:
    can = CanvasWrapper()
    cm  = CalendarManager()


    cs = can.getUpcomingAssignments()
    for key, val in cs.items():
        for v in val:
            for myKey, myVal in v.__dict__.items():
                print(myKey, end='\n\t')
                print(myVal)
            print()

# TODO
# Ask teachers hey, any reason the actual due date and the canvas due date are different?

