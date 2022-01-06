from pydantic import BaseModel
from typing import Optional, List


class AlertBody(BaseModel):
    id: str
    timestamp: str
    timestamp_processing: str
    timerange_start: Optional[str] = None
    timerange_end: Optional[str] = None
    streams: List[str] = None
    source_streams: List[str] = None
    message: str
    priority: int
    alert: str
    fields: Optional[dict] = None
    group_by_fields: Optional[dict] = None
    backlog: List[str] = None


class GraylogEventDefinition(BaseModel):
    event_definition_title: str
    event_definition_description: str
    event: Optional[AlertBody] = None
