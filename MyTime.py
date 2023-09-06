import time
from datetime import datetime


# Turn the word of month to number, like: Jan -> 1
def turnMonthToNumber(month):
    monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return monthList.index(month) + 1


# Handle all the time information
class Time:
    def __init__(self, information):
        self.time = information
        timeList = information.split()
        self.week = timeList[0][:len(timeList[0])-1]
        self.day = timeList[1]
        self.month = timeList[2]
        self.year = timeList[3]
        self.specificTime = timeList[4]
        specific_time_list = self.specificTime.split(':')
        self.hour = specific_time_list[0]
        self.minute = specific_time_list[1]
        self.second = specific_time_list[2]
        if self.second[-2:] == "\r":
            self.second = self.second[:-2]

    # Compare two time, if self is younger or equal, return true
    def compare(self, anotherTime):
        first_time = datetime(int(self.year), turnMonthToNumber(self.month), int(self.day), int(self.hour), int(self.minute), int(self.second))
        second_time = datetime(int(anotherTime.year), turnMonthToNumber(anotherTime.month), int(anotherTime.day), int(anotherTime.hour), int(anotherTime.minute), int(anotherTime.second))
        return first_time >= second_time


# Handle the access time
# Reference: https://www.freecodecamp.org/chinese/news/how-to-get-the-current-time-in-python-with-datetime/
# https://cloud.tencent.com/developer/article/1961983
class AccessTime(Time):
    time = None

    def __init__(self):
        accessDate_and_time = datetime.now()
        self.now_time = accessDate_and_time.strftime('%a, %d %b %y %H:%M:%S GMT')
        self.calculable_time = time.time()
        super().__init__(self.now_time[:len(self.now_time)-4])

    # Return the access time as a string
    def getAccessTime(self):
        return self.time
