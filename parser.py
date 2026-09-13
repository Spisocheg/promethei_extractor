from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import httpx
from lxml import etree

import constants as const
from models import Date


def _get_dates_range() -> list[Date]:
    today = datetime.today().date()
    start_month = const.FIRST_SEM_MONTH_RANGE[0] \
        if today.month in const.FIRST_SEM_MONTH_RANGE else const.SECOND_SEM_MONTH_RANGE[0]
    start_date = date(year=today.year, month=start_month, day=1)

    dates_range = []
    for m in range(const.SEM_MONTH_DELTA):
        curr = start_date + relativedelta(months=m)
        dates_range.append(Date(month=curr.month, year=curr.year))

    return dates_range


def parse(login, password):
    with httpx.Client() as client:
        body = const.LOGIN_BODY.copy()
        body.update({'AuthLogin': login, 'AuthPassword': password})
        client.post(const.PROMETHEI_API_LOGIN_URL,
                    headers=const.LOGIN_HEADERS,
                    params=const.LOGIN_PARAMS,
                    data=body)
