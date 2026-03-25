####################################################
#                                                  #
#    src/pfmsoft/snippets/datetime/date_range.py
#                                                  #
####################################################
# Created by: Chad Lowe                            #
# Created on: 2025-07-04T04:20:56-07:00            #
# Last Modified: 2025-07-04T04:22:03-07:00         #
# Source: https://github.com/DonalChilde/pfmsoft_snippets  #
####################################################

from collections.abc import Iterator
from datetime import date, timedelta


def date_range(start_date: date, end_date: date) -> Iterator[date]:
    """Generate a range of dates from start_date to end_date, inclusive.

    Args:
        start_date (date): The starting date.
        end_date (date): The ending date.

    Yields:
        date: Each date in the range from start_date to end_date.
    """
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def date_range_period(start_date: date, end_date: date, period: int) -> Iterator[date]:
    """Generate a range of dates from start_date to end_date, inclusive, with a specified period.

    Args:
        start_date (date): The starting date.
        end_date (date): The ending date.
        period (int): The number of days between each date in the range.

    Yields:
        date: Each date in the range from start_date to end_date with the specified period.
    """
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=period)


def date_range_days(start_date: date, days: int, past: bool = False) -> Iterator[date]:
    """Generate a range of dates starting from start_date for a specified number of days, inclusive.

    Args:
        start_date (date): The starting date.
        days (int): The number of days to generate.
        past (bool): True if date range counts backwards from start date. Default is False.

    Yields:
        date: Each date in the range starting from start_date for the specified number of days.
    """
    if past:
        day_range = range(0, days * -1, -1)
    else:
        day_range = range(0, days)
    for i in day_range:
        yield start_date + timedelta(days=i)
