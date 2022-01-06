import httpx
import json
import re
import uuid

from src.main import logger


class CreateThehive4Alert:
    def __init__(self, url, auth_type, api_key=None, username=None, password=None):
        self.url = f'{url}/api/alert'
        if 'password' in auth_type:
            pass    # To Do
        else:
            self.headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            }

    async def create_alert(self, graylog_event):
        alert_artifacts = []
        graylog_fields = graylog_event.event.fields

        ip_search_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        mail_search_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        for key, val in graylog_fields.items():
            if ip_search_pattern.search(val):
                alert_artifacts.append({"dataType": "ip", "data": graylog_fields[key]})
            elif mail_search_pattern.search(val):
                alert_artifacts.append({"dataType": "mail", "data": graylog_fields[key]})
            elif key == 'fqdn':
                alert_artifacts.append({"dataType": "fqdn", "data": graylog_fields[key]})
            elif key == 'url':
                alert_artifacts.append({"dataType": "url", "data": graylog_fields[key]})
            else:
                alert_artifacts.append({"dataType": "other", "data": graylog_fields[key]})

        alert_body = {
            'title': graylog_event.event_definition_title,
            'description': graylog_event.event_definition_description,
            'type': 'external',
            'source': 'Graylog Alert Gateway',
            'sourceRef': str(uuid.uuid4())[0:6],
            'severity': graylog_event.event.priority,
            'artifacts': alert_artifacts,
        }

        async with httpx.AsyncClient() as client:
            alert_creating = await client.post(
                self.url,
                data=json.dumps(alert_body),
                headers=self.headers
            )

        if alert_creating.status_code == 401:
            logger.logging(
                f'Unable to create alert by reason of authentication error. Status code: {alert_creating.status_code}',
                logger_level='ERROR',
                source='TheHive4',
            )
        if alert_creating.status_code == 404:
            logger.logging(
                f'Unable to create alert by reason of page not found. Status code: {alert_creating.status_code}',
                logger_level='ERROR',
                source='TheHive4'
            )
        if alert_creating.status_code == 403:
            logger.logging(
                f'Unable to create alert by reason of access forbidden. Status code: {alert_creating.status_code}',
                logger_level='ERROR',
                source='TheHive4'
            )
