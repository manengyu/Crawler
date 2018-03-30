# -*- coding: utf8 -*-
import datetime
import calendar


def get_day(type_date=u"today", count=0):
    now = datetime.datetime.now()
    today = datetime.date.today()
    if type_date == u"today":
        return today
    elif type_date == u"yesterday":
        return today - datetime.timedelta(days=1)
    elif type_date == u"next_day":
        return today + datetime.timedelta(days=1)
    elif type_date == u"monday":
        return today - datetime.timedelta(days=now.weekday())
    elif type_date == u"1st":
        return today - datetime.timedelta(days=now.day)
    else:
        return today - datetime.timedelta(days=count)
        
        
def get_date(start_date=None, intervals=0, end_date=None):
    start_date = datetime.datetime.strptime(start_date, u'%Y-%m-%d')
    if end_date is not None:
        intervals = (start_date - datetime.datetime.strptime(end_date, u'%Y-%m-%d')).days
    return (start_date + datetime.timedelta(days=intervals)).strftime(u'%Y-%m-%d'), -intervals


def get_datetime(start_date=None, intervals=0, end_date=None):
    start_date = datetime.datetime.strptime(start_date, u'%Y-%m-%d %H:%M:%S')
    if end_date is not None:
        intervals = start_date - datetime.datetime.strptime(end_date, u'%Y-%m-%d %H:%M:%S')
    return (start_date + intervals).strftime(u'%Y-%m-%d %H:%M:%S'), -intervals


def date_cycle(start_date, end_date):
    day_list = []
    start = datetime.datetime.strptime(start_date, u'%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, u'%Y-%m-%d')
    for i in range((end - start).days + 1):
        day = start + datetime.timedelta(days=i)
        day = day.strftime(u"%Y-%m-%d")
        day_list.append(day)
    return day_list


def lastmonth01(date):
    date = datetime.datetime.strptime(date, u'%Y-%m-%d')
    dayscount = datetime.timedelta(days=date.day)
    dayto = date - dayscount
    date_from = datetime.datetime(dayto.year, dayto.month, 1, 0, 0, 0)
    return date_from.strftime(u'%Y-%m-%d')


def weekend_or_monthend(date=u''):
    # weekend?
    weekday = datetime.datetime.strptime(date, u'%Y-%m-%d').weekday()
    is_weekend = True if weekday == 6 else False
    # monthend?
    monthrange = calendar.monthrange(int(date[0:4]), int(date[5:7]))
    monthend = date[0:8] + str(monthrange[1])
    is_monthend = True if monthend == date else False
    return is_weekend, is_monthend
