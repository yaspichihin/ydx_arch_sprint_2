import os


class Config:
    def __init__(self):
        self.port = int(os.getenv("PORT", 8082))
        self.kafka_brokers = os.getenv("KAFKA_BROKERS", "127.0.0.1:9092")

cfg = Config() 
