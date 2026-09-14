from datetime import date

from pydantic import RootModel

from .pipeline import get_events
from .settings import settings


def main():
    events = get_events()
    with open(settings.output_dir / f'Promethei Events {date.today()}.json', 'w', encoding="utf-8") as file:
        dump = RootModel(events).model_dump_json(indent=4)
        file.write(dump)


if __name__ == '__main__':
    main()
