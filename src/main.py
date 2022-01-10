import configparser

from fastapi import FastAPI
from os.path import abspath, dirname, join


config_file = join(abspath(dirname(__file__)), '../config.ini')
config = configparser.ConfigParser()
config.read(config_file)

app = FastAPI(
    root_path='/api/v1'
)

try:
    from src.modules.logging import Logging
    logger = Logging(
        logger_name=config.get('logger', 'name'),
        file_name=config.get('logger', 'file_name'),
    )

    if 'enabled' in config.get('stream_resolver', 'status') \
            and 'token' in config.get('stream_resolver', 'auth_type'):
        from src.modules.stream_resolver import Resolver
        stream_resolver = Resolver(
            graylog_url=config.get('stream_resolver', 'graylog_url'),
            auth_type=config.get('stream_resolver', 'auth_type'),
            token=config.get('stream_resolver', 'token'),
        )
    elif 'enabled' in config.get('stream_resolver', 'status') \
            and 'password' in config.get('stream_resolver', 'auth_type'):
        from src.modules.stream_resolver import Resolver
        stream_resolver = Resolver(
            graylog_url=config.get('stream_resolver', 'graylog_url'),
            auth_type=config.get('stream_resolver', 'auth_type'),
            login=config.get('stream_resolver', 'login'),
            password=config.get('stream_resolver', 'password'),
        )

    if 'TheHive4' in config.get('irp_platform', 'platform') \
            and 'api_key' in config.get('thehive4', 'auth_type'):
        from src.integrations.thehive4 import CreateThehive4Alert
        create_alert = CreateThehive4Alert(
            url=config.get("thehive4", "url"),
            auth_type=config.get('thehive4', 'auth_type'),
            api_key=config.get("thehive4", "api_key"),
        )
    elif 'TheHive4' in config.get('irp_platform', 'platform') \
            and 'password' in config.get('thehive4', 'auth_type'):
        from src.integrations.thehive4 import CreateThehive4Alert
        create_alert = CreateThehive4Alert(
            url=config.get("thehive4", "url"),
            auth_type=config.get('thehive4', 'auth_type'),
            login=config.get("thehive4", "login"),
            password=config.get("thehive4", "password"),
        )

except Exception as e:
    print(f'[!] Error on settings up global utils: {e}')

from src.routers import input
app.include_router(input.router)
