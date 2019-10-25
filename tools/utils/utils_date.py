# -*- coding: utf-8 -*-


def format_for_file(date):
    return '%d%02d%02d_%02d%02d' % (date.year, date.month, date.day, date.hour, date.minute)
