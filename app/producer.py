import pika
import time
import random
import os

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue='lab_queue', durable=True)

print("Producer started — sending messages every 2s")
while True:
    message = f"event_{random.randint(1000, 9999)}"
    channel.basic_publish(
        exchange='',
        routing_key='lab_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f" [x] Sent: {message}")
    time.sleep(2)
EOF