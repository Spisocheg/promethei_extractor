PROMETHEI_API_LOGIN_URL = "https://dot.mpei.ac.ru/close/auth.asp"
LOGIN_PARAMS = {'action': 'enter'}
LOGIN_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
LOGIN_BODY = {'ustatus': None, 'returl': None, 'AuthLogin': '', 'AuthPassword': ''}

PROMETHEI_API_EVENTS_URL = "https://dot.mpei.ac.ru/close/ajax.asp"
EVENTS_PARAMS = {'action': 'get_events_and_accesses', 'year': None, 'month': None}
EVENTS_HEADERS = {'Referer': 'https://dot.mpei.ac.ru/close/students/info.asp', 'X-Requested-With': 'XMLHttpRequest'}

FIRST_SEM_MONTH_RANGE = (9, 10, 11, 12, 1)
SECOND_SEM_MONTH_RANGE = (2, 3, 4, 5, 6)
SEM_MONTH_DELTA = 5
