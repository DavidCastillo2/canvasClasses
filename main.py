from Calendar.CalendarManager import CalendarManager
from Canvas.CanvasWrapper import CanvasWrapper

can = CanvasWrapper()
cm  = CalendarManager()


print("So it begins")
cs = can.getUpcomingAssignments()
for key, val in cs.items():
    if len(val) > 0:
        print(key, end='\n\t')
        for v in val:
            print(v.name, end='\n\t')
            print(v.due_at_date, end='\n\t')
        print()


cm.updateCalendar(can.getUpcomingAssignments())

