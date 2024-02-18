import os
from kafka import KafkaProducer
from datetime import datetime
import json

kafka_broker = os.environ.get("KAFKA_BROKER_URL", "localhost:9093")
kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

producer = KafkaProducer(bootstrap_servers=[kafka_broker], value_serializer=lambda v: json.dumps(v).encode("utf-8"))
for i in range(5):
    producer.send(
        kafka_topic, {"sender": "buildingminds", "content": f"message {i}", "created_at": datetime.now().isoformat()}
    )
    print(f"message {i} sent to topic {kafka_topic}")
