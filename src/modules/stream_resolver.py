import httpx


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

        return stream_resolving.json()
