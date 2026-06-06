import pika
import time
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
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    time.sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='lab_queue', on_message_callback=callback)
print("Consumer waiting for messages...")
channel.start_consuming()
EOF