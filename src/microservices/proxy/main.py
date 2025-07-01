import os
import random
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from proxy import proxy_request
from logging_config import logging, LOG_LEVEL


logger = logging.getLogger("main")
logger.setLevel(LOG_LEVEL)

class Config:
    def __init__(self):
        self.port = int(os.getenv('PORT', 8000))
        self.monolith_url = os.getenv('MONOLITH_URL', 'http://localhost:8080')
        self.movies_service_url = os.getenv('MOVIES_SERVICE_URL', 'http://localhost:8081')
        self.events_service_url = os.getenv('EVENTS_SERVICE_URL', 'http://localhost:8082')
        self.gradual_migration = os.getenv('GRADUAL_MIGRATION', 'false').lower() == 'true'
        self.movies_migration_percent = int(os.getenv('MOVIES_MIGRATION_PERCENT', 0))

app = FastAPI()
cfg = Config()

@app.get('/health')
async def handle_health():
    return JSONResponse({'status': True})

@app.api_route('/api/movies', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def movies_handler(request: Request):
    random.seed(time.time())
    if (
        cfg.gradual_migration and
        random.randint(0, 99) < cfg.movies_migration_percent
    ):
        logger.info(f'Request `{request.url.path}` was redirected to microservice')
        return await proxy_request(request, cfg.movies_service_url)
    else:
        logger.info(f'Request `{request.url.path}` was redirected to monolith')
        return await proxy_request(request, cfg.monolith_url)

@app.api_route('/api/users', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def users_handler(request: Request):
    random.seed(time.time())
    logger.info(f'Request `{request.url.path}` was redirected to monolith')
    return await proxy_request(request, cfg.monolith_url)

if __name__ == "__main__":
    logger.info(f'Starting proxy microservice on port {cfg.port}')
    uvicorn.run("main:app", host="0.0.0.0", port=cfg.port, reload=True)
