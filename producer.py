from confluent_kafka import Producer
from faker import Faker
import json
import random
import time
import socket

fake = Faker()

actions = [
    "view_profile", "send_connection_request", "accept_connection",
    "like_post", "comment_post", "share_post", "follow_company"
]

conf = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

def generate_user_activity():
    return {
        "user_id": fake.uuid4(),
        "user_name": fake.name(),
        "action": random.choice(actions),
        "target_user": fake.name(),
        "timestamp": fake.date_time_this_year().isoformat(),
        "metadata": {
            "location": fake.city(),
            "device": random.choice(["mobile", "web", "tablet"]),
            "company": fake.company()
        }
    }
    
def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"✅ Record produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

topic = "user_activity"

print("🚀 Starting user-activity producer ...")
while True:
    event = generate_user_activity()
    producer.produce(
        topic=topic,
        key=event["user_id"],
        value=json.dumps(event),
        callback=delivery_report
    )
    producer.poll(0)
    time.sleep(random.uniform(0.5, 2))