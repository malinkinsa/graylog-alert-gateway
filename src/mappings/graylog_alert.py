from pydantic import BaseModel
from typing import Optional, List


class AlertBody(BaseModel):
    id: str
    timestamp: str
    timestamp_processing: str
    timerange_start: Optional[str] = ''
    timerange_end: Optional[str] = ''
    streams: List[str] = []
    source_streams: List[str] = []
    message: str
    priority: int
    alert: str
    fields: Optional[dict] = {}
    group_by_fields: Optional[dict] = {}
    backlog: List[str] = {}


class GraylogEventDefinition(BaseModel):
    event_definition_title: str
    event_definition_description: str
    event: Optional[AlertBody] = None
