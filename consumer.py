import logging
from kafka import KafkaConsumer, KafkaProducer
import json
import time
import threading
from collections import defaultdict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("consumer.log"),
        logging.StreamHandler()
    ]
)

# Dictionary to keep track of the count of messages per app_version
app_version_count = defaultdict(int)

# Function to categorize devices
def categorize_device(device_type):
    mobile_devices = ['android', 'ios']
    tablet_devices = ['ipad']
    desktop_devices = ['windows', 'macos', 'linux']
    if device_type.lower() in mobile_devices:
        return 'Mobile'
    elif device_type.lower() in tablet_devices:
        return 'Tablet'
    elif device_type.lower() in desktop_devices:
        return 'Desktop'
    else:
        return 'Unknown'

# Function to check for anomalies
def check_anomalies(data):
    # Example: Flag if there are multiple logins from different locations in a short period
    # Here, we just add a dummy check
    if data.get('locale') in ['RU', 'VA', 'MO']:
        return True
    return False

def process_data(data):
    try:
        # Filter: Only process messages where device_type is 'android'
        if data.get('device_type') != 'android':
            return None

        # Transformation: Add a new field indicating the processing timestamp
        data['processed_timestamp'] = time.time()

        # Transformation: Add human-readable processed time
        data['processed_time_human_readable'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(data['processed_timestamp'])
        )

        # Device Categorization
        data['device_category'] = categorize_device(data['device_type'])

        # Check for anomalies
        data['anomaly'] = check_anomalies(data)

        # Aggregation: Count messages per app_version
        app_version_count[data['app_version']] += 1

        return data
    except Exception as e:
        logging.error(f"Error processing data: {e}")
        return None

def consume_and_process():
    consumer = KafkaConsumer(
        'user-login',
        bootstrap_servers='localhost:29092',
        auto_offset_reset='earliest',
        group_id='consumer-group-1',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    producer = KafkaProducer(
        bootstrap_servers='localhost:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    logging.info("Listening to 'user-login' topic...")
    for message in consumer:
        try:
            data = message.value
            logging.info(f"Consumed: {data}")
            processed_data = process_data(data)
            if processed_data:
                producer.send('processed-user-login', processed_data)
                logging.info(f"Produced: {processed_data}")
            else:
                logging.info("Skipped processing due to filter conditions or error")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e} - Data: {message.value}")
        except Exception as e:
            logging.error(f"General error: {e} - Data: {message.value}")

def view_processed_data():
    consumer = KafkaConsumer(
        'processed-user-login',
        bootstrap_servers='localhost:29092',
        auto_offset_reset='earliest',
        group_id='viewer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    logging.info("Listening to 'processed-user-login' topic...")
    for message in consumer:
        data = message.value
        logging.info(f"Processed Data: {data}")

def log_aggregations():
    while True:
        time.sleep(60)  # Log every 60 seconds
        logging.info(f"Aggregations - Message count per app_version: {dict(app_version_count)}")

if __name__ == "__main__":
    # Run consume_and_process in a separate thread
    threading.Thread(target=consume_and_process).start()

    # Run log_aggregations in a separate thread
    threading.Thread(target=log_aggregations).start()

    # Run view_processed_data in the main thread
    view_processed_data()
