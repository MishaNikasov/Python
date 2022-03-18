from datetime import datetime


def format_date_by_pattern(date, pattern='%m/%d/%y %H:%M'):
    datetime.strftime(date, pattern)


def get_current_time():
    return datetime.now().strftime("%m/%d/%Y, %H:%M")


def get_current_time_in_millis():
    return datetime.now().timestamp() * 1000
