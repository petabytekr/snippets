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
    today = datetime.datetime.now(Seoul_tzinfo()).date()
    
    # 다음목요일로 조정, 금,토, 일경우 이전 목요일로 조정됨
    aligned = today - datetime.timedelta(days=(4-today.weekday())) # 다음 목요일로 맞춤

    return aligned


def date_for_retrieval():
    today = datetime.datetime.now(Seoul_tzinfo()).date()

    return today - datetime.timedelta(days=2-today.weekday())


