"""
Class that encodes a TimeStamp within a video.
Useful for comparing TimeStamps together.
"""
import math

class TimeStamp:
    def __init__(self, hours = 0, minutes = 0, seconds = 0, miliseconds = 0):
        self.miliseconds = int(miliseconds%1000)
        carry = miliseconds//1000
        self.seconds = int(seconds%60 + carry)
        carry = seconds//60
        self.minutes = int(minutes%60 + carry)
        carry = minutes//60
        self.hours = int(hours + carry)
    
    def __gt__(self, other):
        hours_diff = int(self.hours >= other.hours) - int(self.hours <= other.hours)
        minutes_diff = int(self.minutes >= other.minutes) - int(self.minutes <= other.minutes)
        seconds_diff = int(self.seconds >= other.seconds) - int(self.seconds <= other.seconds)
        miliseconds_diff = int(self.miliseconds >= other.miliseconds) - int(self.miliseconds <= other.miliseconds)
        return (hours_diff*1000 + minutes_diff*100 + seconds_diff*10 + miliseconds_diff) > 0
    
    def __ge__(self, other):
        hours_diff = int(self.hours >= other.hours) - int(self.hours <= other.hours)
        minutes_diff = int(self.minutes >= other.minutes) - int(self.minutes <= other.minutes)
        seconds_diff = int(self.seconds >= other.seconds) - int(self.seconds <= other.seconds)
        miliseconds_diff = int(self.miliseconds >= other.miliseconds) - int(self.miliseconds <= other.miliseconds)
        return (hours_diff*1000 + minutes_diff*100 + seconds_diff*10 + miliseconds_diff) >= 0

    def __add__(self, other):
        if isinstance(other, int):
            other = TimeStamp(seconds=other)
        miliseconds = self.miliseconds + other.miliseconds
        carry = miliseconds//1000
        miliseconds -= 1000*carry

        seconds = self.seconds + other.seconds + carry
        carry = seconds//60
        seconds -= 60*carry

        minutes = self.minutes + other.minutes + carry
        carry = minutes//60
        minutes -= 60*carry

        hours = self.hours + other.hours + carry
        return TimeStamp(hours, minutes, seconds, miliseconds)

    def __str__(self):
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02},{self.miliseconds:03}"
    
    def __repr__(self):
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02},{self.miliseconds:03}"

    def from_string(timestamp_string):
        timestamp = timestamp_string.split(":")
        hours = int(timestamp[0])
        minutes = int(timestamp[1])
        timestamp = timestamp[2].split(",")
        seconds = int(timestamp[0])
        miliseconds = int(timestamp[1])
        return TimeStamp(hours, minutes, seconds, miliseconds)
    