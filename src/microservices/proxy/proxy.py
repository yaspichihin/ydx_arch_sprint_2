from typing import Dict
import httpx
from fastapi import Request, Response
from urllib.parse import urljoin

from logging_config import logging, LOG_LEVEL

logger = logging.getLogger('proxy')
logger.setLevel(LOG_LEVEL)

EXCLUDED_HEADERS = {'content-encoding', 'content-length', 'transfer-encoding', 'connection'}

def filter_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Удаляет заголовки, которые не стоит проксировать клиенту.
    """
    return {k: v for k, v in headers.items() if k.lower() not in EXCLUDED_HEADERS}

async def proxy_request(request: Request, target_url: str) -> Response:
    """
    Асинхронно пересылает HTTP-запрос к target_url, копируя метод, заголовки, параметры и тело.
    Возвращает ответ сервиса с фильтрацией служебных заголовков.
    """
    logger.info(f'Proxy request to {target_url}')

    method = request.method
    url = urljoin(target_url, request.url.path)
    if request.url.query:
        url = f"{url}?{request.url.query}"

    headers = dict(request.headers)
    headers.pop('host', None)
    params = dict(request.query_params)
    body = await request.body()

    async with httpx.AsyncClient(follow_redirects=False) as client:
        resp = await client.request(
            method=method,
            url=url,
            headers=headers,
            content=body,
            params=params
        )

    filtered_headers = filter_headers(resp.headers)
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=filtered_headers
    )
