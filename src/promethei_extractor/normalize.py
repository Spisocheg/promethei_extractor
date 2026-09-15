from datetime import datetime

from lxml.etree import _Element     # noqa : нужен только для типизации
from loguru import logger

from .models import Event, Course


def _extract_raw_events(responses: list) -> list[_Element]:
    not_filtered_events = []
    for resp in responses:
        not_filtered_events.extend(resp.xpath('//results/item'))

    raw_events = list(filter(
        lambda ev: ev.xpath('./eventType')[0].text == 'event', not_filtered_events
    ))

    if raw_events:
        logger.debug('Список Событий из респонсов получен')
    else:
        logger.debug('Список Событий из респонсов пустой. Возможен пустой выходной файл')

    return raw_events


def _transform_events2model(raw_events: list[_Element]) -> list[Event]:
    events = []
    for raw_e in raw_events:
        try:
            events.append(
                Event(
                    id_=raw_e.xpath('./elementId')[0].text.strip('{}'),
                    name=raw_e.xpath('./elementName')[0].text,
                    type_=int(raw_e.xpath('./eventSubType')[0].text),
                    date_start=datetime.strptime(raw_e.xpath('./eventDateBegin')[0].text, '%d.%m.%Y %H:%M').date(),
                    date_end=datetime.strptime(raw_e.xpath('./eventDateEnd')[0].text, '%d.%m.%Y %H:%M').date(),
                    course=Course(
                        id_=raw_e.xpath('./courseId')[0].text.strip('{}'),
                        name=raw_e.xpath('./courseName')[0].text
                    )
                )   # noqa: str_type заполняется до валидации декоратором модели
            )
        except AttributeError:
            pass
    return events


def _dedup_events(events: list[Event]) -> list[Event]:
    ids = set()
    filtered_e = []
    for ev in events:
        if ev.id_ not in ids:
            filtered_e.append(ev)
            ids.add(ev.id_)
    logger.debug('Список Событий очищен от дубликатов')
    return filtered_e


def normalize(responses: list[_Element]) -> list[Event]:
    raw_events = _extract_raw_events(responses)
    events = _transform_events2model(raw_events)
    return _dedup_events(events)
