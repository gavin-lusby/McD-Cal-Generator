#import getEmail




def getShiftsAsStrings(emailAsArray, stringBeforeSchedule):
    hasShiftsStarted = False
    shifts = []
    for line in emailAsArray:
        if stringBeforeSchedule in line: # Checks if the w
            hasShiftsStarted = True
        # Searches for keyword day, to know that the schedule is still going(eg. Monday, Tuesday, Wednesday, etc)
        elif hasShiftsStarted == True and 'day' in line:
            shifts.append(line)
        elif hasShiftsStarted:
            break
    return shifts


"""Converts events in format of "Monday, June 7, 2021 11:00 AM - 5:30 PM, FF", (in that exact configuration), where the 
code at the end is the description and name, and where the first thing is the day of the week into list in format of 
(startDate, endDate, description) where description is the code at the end, and startDate and endDated are formated 
like this "YYYY-MM-DDThh:mm:ss-04:00", where Y = Year, M = Month, D = Day, T = the letter 'T', h = Hour, m = minute, 
s = second(assumed to be 00), and the part at the end is the time difference for eastern time"""
def getEventInfo(shift):
    shift_item = shift.split()

    unfMonth = shift_item[1]
    if unfMonth == "January":
        monthVar = "01"
    elif unfMonth == "February":
        monthVar = "02"
    elif unfMonth == "March":
        monthVar = "03"
    elif unfMonth == "April":
        monthVar = "04"
    elif unfMonth == "May":
        monthVar = "05"
    elif unfMonth == "June":
        monthVar = "06"
    elif unfMonth == "July":
        monthVar = "07"
    elif unfMonth == "August":
        monthVar = "08"
    elif unfMonth == "September":
        monthVar = "09"
    elif unfMonth == "October":
        monthVar = "10"
    elif unfMonth == "November":
        monthVar = "11"
    elif unfMonth == "December":
        monthVar = "12"

    unfDay = shift_item[2][:-1]
    if int(unfDay) < 10:
        dayVar = "0" + unfDay
    else:
        dayVar = unfDay

    yearVar = shift_item[3]

    startVar = toMilitaryTime(shift_item[4], shift_item[5])
    endVar = toMilitaryTime(shift_item[7], shift_item[8][:-1])

    # Sets end of shift time to 11:59PM if end time is later than start time, so the program doesnt get messed up by
    # programs that go overnight
    if (int(endVar[0:2]) < int(startVar[0:2])) or (
            (int(endVar[0:2]) == int(startVar[0:2])) and endVar[3:] < startVar[3:]):
        endVar = "23:59"

    description = shift_item[9]
    startDate = yearVar + "-" + monthVar + "-" + dayVar + "T" + startVar + ":00-04:00"
    endDate = yearVar + "-" + monthVar + "-" + dayVar + "T" + endVar + ":00-04:00"
    return (startDate, endDate, description)


def toMilitaryTime(time,ampm):

# time = "11:00", ampm = "AM" ---> "11:00"
# time = "11:00", ampm = "PM" ---> "23:00"

    unfHour = (time[:-3])
    if int(unfHour) < 10:
        unfHour = "0" + unfHour

    if unfHour == "12":
        if ampm == "AM":
            if time == "12:00":
                militaryTime = "23:59"
            else:
                militaryTime = "00" + time[-3:]
        else:
            militaryTime = time
    else:
        if ampm == "AM":
            militaryTime = unfHour + time[-3:]
        else:
            militaryTime = str((int(unfHour)+12)) + time[-3:]


    return militaryTime


def returnEventObjectList(emailAsArray, stringBeforeSchedule, eventLocation, originalEventName):


    shiftArray = getShiftsAsStrings(emailAsArray, stringBeforeSchedule)
    eventList = []
    for shift in shiftArray:
        eventInfoList = getEventInfo(shift)

        eventStartDate = eventInfoList[0]
        eventEndDate = eventInfoList[1]
        eventDescription = eventInfoList[2]

        # originalEventName has to be used so that each subsequent event doesn't add the description of itself to the name that will be used for the next event
        # (ex. for name "Shift" and description "Fries, Kitchen, Service", names will otherwise be:
        # Shift (Fries),
        # Shift (Fries) (Kitchen),
        # Shift (Fries) (Kitchen) (Service)
        eventName = originalEventName + " (" + eventDescription + ")"

        eventList.append({
        'summary': eventName,
        'location': eventLocation,
        'description': eventDescription,
        'start': {
            'dateTime': eventStartDate,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': eventEndDate,
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 120},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    })

    return eventList



