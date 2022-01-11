from fastapi import APIRouter

from src.mappings.graylog_alert import GraylogEventDefinition
from src.main import telegram


router = APIRouter(
    prefix='/telegram',
    responses={404: {"description": "Not found"}},
)


@router.post('/')
async def catcher(graylog_event: GraylogEventDefinition):
    await telegram.send_alert(graylog_event)
    return graylog_event