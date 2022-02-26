from datetime import datetime


class Event:
    def __init__(self, title, startTime, endTime, location='5800 Bay Shore Rd, Sarasota, FL 34243'):
        startTime = convertAssignmentTime(startTime)
        endTime   = convertAssignmentTime(endTime)
        self.body = {
            'summary': title,
            'location': location,
            'description': 'Automated Event - David Castillo',
            'start': {
                'dateTime': startTime.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': endTime.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/New_York',
            },
            'reminders': {
                'useDefault': False,
                # 'overrides': [
                #     {'method': 'popup', 'minutes': 60},
                #     {'method': 'popup', 'minutes': 30},
                # ],
            },
        }


def convertAssignmentTime(assignmentTime):
    return datetime(year=int(assignmentTime[0:4]), month=int(assignmentTime[5:7]),
                    day=int(assignmentTime[8:10]), hour=int(assignmentTime[11:13]),
                    minute=int(assignmentTime[14:16]), second=int(assignmentTime[17:19]))
