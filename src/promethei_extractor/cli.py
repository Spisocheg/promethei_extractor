import sys
import argparse
from datetime import date

from pydantic import RootModel
from loguru import logger

from .exceptions import (
    ConfigurationError,
    AuthenticationError,
    PrometheiApiError,
    MalformedResponseError,
    OutputWriteError,
)
from .pipeline import get_events
from .settings import settings, init_logger


def _write_events(events, path):
    try:
        with open(path, 'w', encoding="utf-8") as file:
            dump = RootModel(events).model_dump_json(indent=4)
            file.write(dump)
    except OSError as e:
        raise OutputWriteError(f'Не удалось записать файл: {path}') from e


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', action='store_true', help='Показывать debug-логи')
    args = arg_parser.parse_args()

    logger.enable('promethei_extractor')
    init_logger(level='DEBUG' if args.debug else 'INFO')

    try:
        _ = settings.login
    except ConfigurationError:
        logger.critical('Ошибка конфигурации. Проверьте логин и пароль пользователя Прометей и повторите попытку')
        sys.exit(1)

    try:
        events = get_events()
        logger.info(f'Всего получено {len(events)} Событий')

        path = settings.output_dir / f'Promethei Events {date.today()}.json'
        _write_events(events, path)
        logger.success(f'Файл успешно записан: {path}')
    except AuthenticationError:
        logger.critical('Не удалось авторизоваться в Прометее. Проверьте логин и пароль и повторите попытку')
        sys.exit(1)
    except (PrometheiApiError, MalformedResponseError, OutputWriteError) as e:
        logger.critical(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
