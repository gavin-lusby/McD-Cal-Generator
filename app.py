import getShifts
import getEmail
import gcalendar
from tkinter import *

desiredSender = 'mcd40367@ext.mcdonalds.com'
searchString = 'Here is your schedule for the week of'
location = '686 Appleby Line, Burlington, ON L7L 5P9, Canada'
name = 'McDonalds Shift'

eventList = getShifts.returnEventObjectList(getEmail.toStringArray(desiredSender), searchString, location, name)

for event in eventList:
    gcalendar.createEvent(event)
