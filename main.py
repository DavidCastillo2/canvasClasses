from Calendar.CalendarManager import CalendarManager
from Canvas.CanvasWrapper import CanvasWrapper
from DiscordBot.theBot import MyBot

testing = False


if not testing:
    b = MyBot(command_prefix="!")
    b.begin()


else:
    can = CanvasWrapper()
    cm  = CalendarManager()


    cs = can.getUpcomingAssignments()
    for key, val in cs.items():
        for v in val:
            valsToPrint = ['created_at', 'updated_at', 'html_url', 'unlock_at']
            print(v.name, end='\n\t')
            for i in range(len(valsToPrint)):
                value = getattr(v, valsToPrint[i])
                print(str(i+1) + ')\t' + valsToPrint[i] + '\n\t\t' + str(value), end='\n\t')

            if len(valsToPrint) == 0:
                for myKey, myVal in v.__dict__.items():
                    # valsToPrint = [myVal.created_at, myVal.updated_at]
                    valsToPrint = [myVal]
                    print(myKey, end='\n\t')
                    print(myVal)
            print()

# TODO
# Ask teachers hey, any reason the actual due date and the canvas due date are different?

