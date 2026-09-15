import sys
import argparse
from datetime import date

from pydantic import RootModel, ValidationError
from loguru import logger

from .pipeline import get_events
from .settings import settings, init_logger


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', action='store_true', help='Показывать debug-логи')
    args = arg_parser.parse_args()

    init_logger(level='DEBUG' if args.debug else 'INFO')

    try:
        _ = settings.login
    except ValidationError:
        logger.critical('Ошибка конфигурации. Проверьте логин и пароль пользователя Прометей и повторите попытку')
        sys.exit()

    events = get_events()
    logger.info(f'Всего получено {len(events)} Событий')

    path = settings.output_dir / f'Promethei Events {date.today()}.json'
    with open(path, 'w', encoding="utf-8") as file:
        dump = RootModel(events).model_dump_json(indent=4)
        file.write(dump)
        logger.success(f'Файл успешно записан: {path}')


if __name__ == '__main__':
    main()
