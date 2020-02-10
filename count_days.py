#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime as dt

def count_days(dead_day):
    """倒计时天数"""
    return dead_day - dt.today()

if __name__ == "__main__":
    last_day = dt(2020,2,16)
    print(count_days(last_day))