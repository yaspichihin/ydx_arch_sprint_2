import asyncio
import datetime
import logging
from typing import Type

import uvicorn
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI, HTTPException, status

from config import cfg
from logging_config import LOG_LEVEL, logging
from schemas import EventResponse, MovieEvent, PaymentEvent, UserEvent


logger = logging.getLogger("main")
logger.setLevel(LOG_LEVEL)

app = FastAPI(title="EventsService")

event_response_msg = {
    "status": "success",
    "partition": 42,
    "offset": 42,
    "event": {
        "id": "movie-1-viewed",
        "type": "movie",
        "timestamp": "2023-01-15T14:30:00Z",
        "payload": {},
    },
}


async def produce_msg(logger, brokers, topic, value):
    """Отправляем событие в Kafka"""
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers=brokers,
            compression_type="gzip",
        )
        await producer.start()
        result = await producer.send_and_wait(topic, value)
        logger.info(f"Event sent to Kafka: {result}")
    finally:
        await producer.stop()


async def consume_msg(logger, brokers, topic):
    """Чтение события из Kafka"""
    try:
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=brokers,
            auto_offset_reset="earliest",
            group_id=f"temp-group-{datetime.datetime.now(datetime.UTC).timestamp()}",
            enable_auto_commit=True,
        )
        await consumer.start()
        msg = await asyncio.wait_for(consumer.getone(), timeout=2.0)
        logger.info(f"Event read from Kafka: {msg}")
        return msg
    finally:
        await consumer.stop()


@app.get(
    "/api/events/health",
    status_code=status.HTTP_200_OK,
    tags=["events"],
)
async def health_check():
    return {"status": True}


@app.post(
    "/api/events/movie",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["events"],
)
async def create_movie_event(event: MovieEvent):
    topic = "movie-events"
    value = event.model_dump_json().encode()
    try:
        await produce_msg(logger, cfg.kafka_brokers, topic, value)
        await consume_msg(logger, cfg.kafka_brokers, topic)
        return event_response_msg

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@app.post(
    "/api/events/user",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["events"],
)
async def create_user_event(event: UserEvent):
    topic = "user-events"
    value = event.model_dump_json().encode()
    try:
        await produce_msg(logger, cfg.kafka_brokers, topic, value)
        await consume_msg(logger, cfg.kafka_brokers, topic)
        return event_response_msg

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@app.post(
    "/api/events/payment",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["events"],
)
async def create_payment_event(event: PaymentEvent):
    topic = "payment-events"
    value = event.model_dump_json().encode()
    try:
        await produce_msg(logger, cfg.kafka_brokers, topic, value)
        await consume_msg(logger, cfg.kafka_brokers, topic)
        return event_response_msg

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082, reload=True)
