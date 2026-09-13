import os

from dotenv import load_dotenv

import parser
import normalize


load_dotenv()

LOGIN = os.getenv('PROMETHEI_LOGIN')
PASSWORD = os.getenv('PROMETHEI_PASS')


if __name__ == '__main__':
    responses = parser.parse(LOGIN, PASSWORD)
    normalized = normalize.normalize(responses)
