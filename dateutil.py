# -*- coding: utf-8 -*-
import datetime

class Seoul_tzinfo(datetime.tzinfo):
    """Implementation of the Seoul timezone.
    
    Adapted from http://code.google.com/appengine/docs/python/datastore/typesandpropertyclasses.html
    """
    def utcoffset(self, dt):
        return datetime.timedelta(hours=+9) + self.dst(dt)

    def _FirstSunday(self, dt):
        """First Sunday on or after dt."""
        return dt + datetime.timedelta(days=(6-dt.weekday()))

    def dst(self, dt):
        """ 한국은 섬머타임 없으므로 계산 생략 (dst=daylight saving time)
        # 2 am on the second Sunday in March
        dst_start = self._FirstSunday(datetime.datetime(dt.year, 3, 8, 2))
        # 1 am on the first Sunday in November
        dst_end = self._FirstSunday(datetime.datetime(dt.year, 11, 1, 1))

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(hours=0)
        """
        return datetime.timedelta(hours=0)

    def tzname(self, dt):
        """
        if self.dst(dt) == datetime.timedelta(hours=0):
            return "KST"
        else:
            return "KDT"
        """
        return "KST"
        
def date_for_new_snippet():
    """Return next Monday, unless it is Monday (0) or Tuesday (1)"""
    today = datetime.datetime.now(Seoul_tzinfo()).date()
    
    """
    if (today.weekday() < 2):
        aligned = today - datetime.timedelta(days=today.weekday())
    else:
        aligned = today + datetime.timedelta(days=(7 - today.weekday()))
    """

    if (today.weekday() < 1): # 월 경우
        aligned = today - datetime.timedelta(days=today.weekday()) # 당일 월요일로 맞춤
    elif (today.weekday() < 3): # 월,화,수 경우
        aligned = today + datetime.timedelta(days=(3-today.weekday())) # 다음 목요일로 맞춤
    elif (today.weekday() < 4): # 목 경우
        aligned = today - datetime.timedelta(days=(3-today.weekday())) # 당일 목요일로 맞춤
    else: # 금, 토, 일 경우
        aligned = today + datetime.timedelta(days=(7-today.weekday())) # 다음주 월요일로 맞춤

    return aligned


def date_for_retrieval():
    """Always return the most recent Monday."""
    today = datetime.datetime.now(Seoul_tzinfo()).date()

    # return today - datetime.timedelta(days=today.weekday())

    if (today.weekday() < 1): # 월 경우
        aligned = today - datetime.timedelta(days=today.weekday()) # 당일 월요일로 맞춤
    elif (today.weekday() < 4): # 목 경우
        aligned = today - datetime.timedelta(days=(3-today.weekday())) # 당일 목요일로 맞춤
    else:
        aligned = today - datetime.timedelta(days=today.weekday()) # 월요일로 맞춤

    return aligned


