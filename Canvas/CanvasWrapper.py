from datetime import datetime

from canvasapi import Canvas


class CanvasWrapper:
    def __init__(self):
        self.url = 'https://ncf.instructure.com/'
        self.token = '8190~qIYpK4cPuUptn1g1eBgXeZl4gEq3KrWLvIj7pWMoaLRtzzvEEN36ZgqX3WZmj1my'
        self.c = Canvas(self.url, self.token)
        self.usUser = self.c.get_current_user()
        return

    # This gets all the classes since the start of time for this user
    def _getClasses(self):
        return self.usUser.get_courses()


    def getUpcomingAssignments(self):
        classes = self._getClasses()
        retVal = {}
        now = datetime.now()
        for course in classes:
            assignments = course.get_assignments()
            retVal[course.name] = []
            for ass in assignments:
                if ass.due_at is None:
                    continue
                dueTime = datetime(year=int(ass.due_at[0:4]), month=int(ass.due_at[5:7]), day=int(ass.due_at[8:10]),
                                   hour=int(ass.due_at[11:13]), minute=int(ass.due_at[14:16]), second=int(ass.due_at[17:19]))
                if dueTime > now:
                    retVal[course.name].append(ass)
        return hardcodedFuckCanvas(retVal)


def hardcodedFuckCanvas(retVal):
    del retVal['CSCI4780: Computer Vision: 23520 (Spring 2022)']
    del retVal['CSCI3655: Introduction to Virtual Reality Systems: 23525 (Spring 2022)']
    return retVal
