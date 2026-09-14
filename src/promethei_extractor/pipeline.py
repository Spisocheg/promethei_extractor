from . import parser, normalize
from .models import Event
from .settings import settings


def get_events() -> list[Event]:
    responses = parser.parse(settings.login, settings.password)
    events = normalize.normalize(responses)
    return events
