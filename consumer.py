from confluent_kafka import Consumer, KafkaException
import json
conf = {
    'bootstrap.servers': 'kafka:9092', 
    'group.id': 'activity-monitor', 
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
topic = "user_activity"

consumer.subscribe([topic])

print("Listening for user activity events... \n")

try: 
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None: 
            continue
        if msg.error():
            raise KafkaException(msg.error())
        
        event = json.loads(msg.value().decode('utf-8'))
        print(f"User: {event['user_name']} ({event['user_id']})")
        print(f"Action: {event['action']} on ({event['target_user']})")
        print(f"🌍 From: {event['metadata']['location']} | Device: {event['metadata']['device']}")
        print(f"🏢 Company: {event['metadata']['company']}")
        print(f"🕒 Timestamp: {event['timestamp']}")
        print("-" * 60)
except KeyboardInterrupt:
    print("\n Stopping consumer...")
finally:
    consumer.close()