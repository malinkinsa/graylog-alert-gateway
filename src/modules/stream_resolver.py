import httpx

from src.main import logger


class Resolver:
    def __init__(self, graylog_url, auth_type, token=None, login=None, password=None):
        self.graylog = graylog_url
        self.header = {
            'Accept': 'application/json',
        }

        if 'token' in auth_type:
            self.auth = (token, 'token')
        else:
            pass    # ToDo

    async def stream_name_resolve(self, stream_id):
        api = f'{self.graylog}/api/streams/{stream_id}'

        async with httpx.AsyncClient() as client:
            stream_resolving = await client.get(
                api,
                headers=self.header,
                auth=self.auth
            )

        if stream_resolving.status_code != 200:
            logger.logging(
                f'Unable to resolve stream uid to name. Answer {stream_resolving.status_code}',
                logger_level='ERROR',
                source='stream_resolver',
            )
            return {'description': 'AlertGateway'}
        else:
            return stream_resolving.json()
