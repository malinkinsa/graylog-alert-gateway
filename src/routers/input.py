from fastapi import APIRouter

from src.mappings.graylog_alert import GraylogEventDefinition
from src.main import create_alert


router = APIRouter(
    prefix='/input',
    responses={404: {"description": "Not found"}},
)


@router.post('/')
async def catcher(graylog_event: GraylogEventDefinition):
    await create_alert.create_alert(graylog_event)
    return graylog_event
