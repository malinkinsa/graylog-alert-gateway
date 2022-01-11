import json
import httpx

from src.main import config, logger

if 'enabled' in config.get('stream_resolver', 'status'):
    from src.main import stream_resolver


class SendToTelegram:
    def __init__(self, chat_id, token):
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.chat_id = chat_id
        self.token = token

    async def send_alert(self, graylog_event):

        url = f'https://api.telegram.org/bot{self.token}/sendMessage'

        if 'enabled' in config.get('stream_resolver', 'status'):
            source = []
            for n, streams in enumerate(graylog_event.event.source_streams):
                stream_id = await stream_resolver.stream_name_resolve(streams)
                source.append(stream_id['description'])

            telegram_payload = {
                'chat_id': f'{self.chat_id}',
                'text': f'Event title: {graylog_event.event_definition_title}\n'
                        f'Event description: {graylog_event.event_definition_description}\n'
                        f'Graylog stream: {str(*source)}\n'
                        f'Severity: {graylog_event.event.priority}\n'
                        f'Artifacts: {json.dumps(graylog_event.event.fields, sort_keys=True, indent=4)}'
            }
        else:
            telegram_payload = {
                'chat_id': f'{self.chat_id}',
                'text': f'Event title: {graylog_event.event_definition_title}\n'
                        f'Event description: {graylog_event.event_definition_description}\n'
                        f'Severity: {graylog_event.event.priority}\n'
                        f'Artifacts: {json.dumps(graylog_event.event.fields, sort_keys=True, indent=4)}'
            }

        async with httpx.AsyncClient() as client:
            alert_sending = await client.post(
                url,
                data=json.dumps(telegram_payload),
                headers=self.headers,
            )

        if alert_sending.status_code != 200:
            logger.logging(
                f'Unable to send alert. Status code: {alert_sending.status_code}',
                logger_level='ERROR',
                source='Telegram',
            )
