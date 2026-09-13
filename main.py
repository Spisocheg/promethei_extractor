import os

from dotenv import load_dotenv

import parser


load_dotenv()

LOGIN = os.getenv('PROMETHEI_LOGIN')
PASSWORD = os.getenv('PROMETHEI_PASS')


if __name__ == '__main__':
    parser.parse(LOGIN, PASSWORD)
    # print(parser._get_dates_range())
