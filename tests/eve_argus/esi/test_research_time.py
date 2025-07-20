from math import ceil

from eve_argus.industry import research_time


def test_research_times_3():
    research_time(10, 105)
    assert research_time(1, 105) == 105
    assert research_time(2, 105) == 250
    assert research_time(3, 105) == 595
