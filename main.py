import os
import pathlib
from datetime import date

from dotenv import load_dotenv
from pydantic import RootModel

from promethei_extractor import parser, normalize

root = pathlib.Path(__file__).parent


load_dotenv()

LOGIN = os.getenv('PROMETHEI_LOGIN')
PASSWORD = os.getenv('PROMETHEI_PASS')


if __name__ == '__main__':
    responses = parser.parse(LOGIN, PASSWORD)
    events = normalize.normalize(responses)
    with open(root / f'Promethei Events {date.today()}.json', 'w', encoding="utf-8") as file:
        dump = RootModel(events).model_dump_json(indent=4)
        file.write(dump)
