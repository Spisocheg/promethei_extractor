import sys
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import httpx
from lxml import etree
from lxml.etree import _Element     # noqa : нужен только для типизации
from loguru import logger

from . import constants as const
from .models import Date


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


def _get_sem_num() -> str:
    today = datetime.today().date()
    sem_num = '1' if today.month in const.FIRST_SEM_MONTH_RANGE else '2'
    return sem_num


def parse(login, password) -> list[_Element]:
    responses_by_months = []
    with httpx.Client() as client:
        body = const.LOGIN_BODY.copy()
        body.update({'AuthLogin': login, 'AuthPassword': password})
        client.post(const.PROMETHEI_API_LOGIN_URL,
                    params=const.LOGIN_PARAMS,
                    headers=const.LOGIN_HEADERS,
                    data=body)

        if not client.cookies or dict(client.cookies).get('AuthLock'):
            logger.critical('Cookies сессии нет. Остановка работы приложения. '
                            'Проверьте логин и пароль пользователя Прометей и повторите попытку')
            sys.exit()
        logger.info(f'Вход выполнен под аккаунтом {login}. Cookies сессии собраны')

        for d in _get_dates_range():
            ev_params = const.EVENTS_PARAMS.copy()
            ev_params.update({'year': str(d.year), 'month': str(d.month)})
            r = client.get(const.PROMETHEI_API_EVENTS_URL,
                           params=ev_params,
                           headers=const.EVENTS_HEADERS)

            serialized = etree.fromstring(r.content)
            responses_by_months.append(serialized)
            logger.debug(f'Получен запрос с датами {d.month} {d.year} и преобразован в xml')

    logger.info(f'Список Событий {_get_sem_num()}-го семестра собран')
    return responses_by_months
