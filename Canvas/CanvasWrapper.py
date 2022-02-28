from datetime import datetime

from canvasapi import Canvas


class CanvasWrapper:
    def __init__(self):
        self.url = 'https://ncf.instructure.com/'
        self.token = '8190~qIYpK4cPuUptn1g1eBgXeZl4gEq3KrWLvIj7pWMoaLRtzzvEEN36ZgqX3WZmj1my'
        self.courses = {}
        self.c = Canvas(self.url, self.token)
        self.usUser = self.c.get_current_user()
        self._populateCourses()
        return


    # This gets all the classes since the start of time for this user
    def _getClasses(self):
        return self.usUser.get_courses()


    def _populateCourses(self):
        for c in self.usUser.get_courses():
            self.courses[c.id] = c


    def getUpcomingAssignments(self):
        classes = self._getClasses()
        retVal = {}
        now = datetime.now()
        for course in classes:
            assignments = course.get_assignments()
            retVal[course.id] = []
            for ass in assignments:
                if ass.due_at is None:
                    continue
                dueTime = datetime(year=int(ass.due_at[0:4]), month=int(ass.due_at[5:7]), day=int(ass.due_at[8:10]),
                                   hour=int(ass.due_at[11:13]), minute=int(ass.due_at[14:16]), second=int(ass.due_at[17:19]))
                if dueTime > now:
                    ass.due_at = dueTime
                    retVal[course.id].append(ass)
        return hardcodedFuckCanvas(retVal)


    def getCourseName(self, assignment):
        for courseID, course in self.courses.items():
            if courseID == assignment.course_id:
                return course.name
        return None

    def getCourseNameByID(self, iD):
        for courseID, course in self.courses.items():
            if courseID == iD:
                return course.name
        return None


def hardcodedFuckCanvas(retVal):
    toRemove = [6569, 6560]
    for c in toRemove:
        try:
            del retVal[c]
        except KeyError:
            pass
    return retVal
