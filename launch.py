import uvicorn

from src.main import config


ip = config.get('launch_config', 'ip')
port = config.get('launch_config', 'port')

if __name__ == "__main__":
    uvicorn.run('src.main:app', host=ip, port=int(port))
