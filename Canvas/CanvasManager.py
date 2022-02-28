import time
from datetime import datetime

from Calendar.CalendarManager import CalendarManager
from Canvas.CanvasWrapper import CanvasWrapper


class CanvasManager:
    def __init__(self):
        self.can = CanvasWrapper()
        self.cm  = CalendarManager()
        self.seen = {}
        self.lastChecked = None
        self.checkIntervalHrs = 2
        return


    def updateGoogleCalendar(self, assignments):
        newAsses = {}
        for courseID, assList in assignments.items():
            newAsses[self.getCourseNameByID(courseID)] = assList

        self.cm.updateCalendar(newAsses)
        return

    # This also updates Google Calendar. Probably should separate
    def getUpcomingAssignments(self, clean=True):
        if self.lastChecked is None or (self.lastChecked - time.time_ns()) / 1000000000 / 60 / 60 > self.checkIntervalHrs:
            self.lastChecked = time.time_ns()
            upcoming = self.can.getUpcomingAssignments()
            unSeen = self._getUnseenAssignments(upcoming)
            if len(unSeen) > 0:
                return upcoming, sortIntoCourses(unSeen)
        return self.removePastAssignments(), {}


    # uses self.seen and removes all assignments that have already past
    def removePastAssignments(self):
        retVal = {}
        now = datetime.now()
        for courseID in self.seen.keys():
            for ass in self.seen[courseID].values():
                if ass.due_at is None:
                    continue
                dueTime = ass.due_at
                if dueTime > now:
                    try:
                        retVal[courseID]
                    except KeyError:
                        retVal[courseID] = {}
                    retVal[courseID][ass.name] = ass
        return retVal


    # Warning, this just compares using Assignment Name, nothing smart
    def _getUnseenAssignments(self, courseAssignments):
        # ass = self.getUpcomingAssignments()
        retVal = []
        for courseID, assignments in courseAssignments.items():
            for a in assignments:
                try:
                    self.seen[a.course_id]
                except KeyError:
                    self.seen[a.course_id] = {}
                try:
                    self.seen[a.course_id][a.name]
                except KeyError:
                    self.seen[a.course_id][a.name] = a
                    retVal.append(a)
        return retVal


    def getUpcomingForClass(self, name):
        assignments = self.getUpcomingAssignments()[0]
        retVal = []
        for courseID in assignments.keys():
            for assName, ass in assignments[courseID]:
                if self.can.getCourseName(assignments[courseID][assName]).lower().find(name.lower()) != -1:
                    retVal.append(ass)
        return retVal


    def getCourseName(self, assignment):
        return self.can.getCourseName(assignment)

    def getCourseNameByID(self, iD):
        return self.can.getCourseNameByID(iD)


def sortIntoCourses(assignments):
    retVal = {}
    for ass in assignments:
        try:
            retVal[ass.course_id].append(ass)
        except KeyError:
            retVal[ass.course_id] = [ass]
    return retVal



