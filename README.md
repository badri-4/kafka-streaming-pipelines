# Real-Time Streaming Data Pipeline

## Project Overview

This project sets up a real-time streaming data pipeline using Kafka and Docker. The pipeline ingests streaming data, processes it with advanced transformations, and stores the processed data in a new Kafka topic. The script also allows viewing the processed data.

### Prerequisites

- Docker
- Docker Compose
- Python (version 3.6 or higher)
- Kafka-Python library

### Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/kafka-streaming-pipelines.git
   cd kafka-streaming-pipelines

2. **Install Python Dependencies:**:

   ```bash
   pip install -r requirements.txt

3. **Run Docker Compose:**:

   ```bash
   docker-compose up -d

4. **Create Kafka Topics**:

     ```bash
   docker exec kafka-streaming-pipelines-kafka-1 kafka-topics --create --topic user-login --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1
   docker exec kafka-streaming-pipelines-kafka-1 kafka-topics --create --topic processed-user-login --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1

5. **Verify Kafka Topics:**:

    ```bash
   docker exec kafka-streaming-pipelines-kafka-1 kafka-topics --list --bootstrap-server localhost:29092

6. **Run the Combined Consumer and Viewer Script:**:

   ```bash
   python consumer.py

## Design Choices:

### Components

1. **Kafka**: Used as the messaging system for real-time data streaming.

      * **Zookeeper**: Manages and coordinates the Kafka brokers.

      * **Kafka Broker**: Handles the data streams and stores them in topics.

2. **Docker**: Provides a consistent environment for running Kafka and other components.
   
      * **Docker Compose**: Simplifies the setup of multi-container Docker applications, ensuring all components start with a single command.

3. **Python**: Used for implementing the Kafka consumer and producer logic.

      * **kafka-python**: A library for working with Kafka in Python, providing the necessary interfaces for consuming and producing messages.


### Data Flow

1. **Data Generation**:

      * A data generator produces messages and sends them to the user-login Kafka topic. This simulates real-time user login events.

2. **Kafka Consumer**:

      * The consumer script listens to the user-login topic, processes each message by applying transformations, filtering, and aggregations, and then sends the processed messages to the processed-user-login Kafka topic.

3. **Kafka Producer**:

      * The producer within the consumer script sends the processed messages to the processed-user-login topic for further use.

4. **Viewing Processed Data**:

      * The script includes functionality to consume and print messages from the processed-user-login topic, allowing for real-time monitoring of the processed data.



### Processing Details

1. **Filtering**:

      * Only processes messages where **'device_type'** is **'android'**, ignoring others.

2. **Transformations**:

      * Adds a **'processed_timestamp'** field to each message.
      * Converts the timestamp to a human-readable format.

3. **Categorization**:

      * Categorizes devices into **'Mobile'**, **'Tablet'**, or **'Desktop'** based on the **'device_type'** field.


4. **Anomaly Detection**:

      * Flags anomalies based on certain conditions (e.g., if the **'locale'** field is in a list of suspicious locales).


5. **Aggregation**:

      * Counts messages per **'app_version'** and logs this information every 60 seconds.


## Ensuring Efficiency, Scalability, and Fault Tolerance


### Efficiency

1. **Batch Processing**:

      * Kafka handles messages in batches, which improves throughput and reduces latency.

2. **Asynchronous Processing**:

      * The consumer and producer operations are asynchronous, ensuring non-blocking data processing.

### Scalability

1. **Kafka Consumer Groups**:

      * Multiple consumers can be part of a consumer group, allowing for parallel processing of messages and load distribution.

2. **Horizontal Scaling**:

      * Kafka brokers and consumers can be scaled horizontally to handle increased load without performance degradation.


### Fault Tolerance

1. **Kafka Replication**:

      * Kafka topics can be configured with replication to ensure data availability even if a broker fails.

2. **Error Handling**:

      * The script includes error handling for JSON decoding and general processing errors, logging detailed error messages for debugging.

3. **Docker Containers**:

      * Docker ensures that each component runs in an isolated environment, reducing the impact of failures and simplifying recovery.


## Conclusion

This real-time streaming data pipeline leverages Kafka and Docker to efficiently ingest, process, and store data. The design ensures scalability through Kafka's consumer groups and horizontal scaling, while fault tolerance is achieved through Kafka's replication and robust error handling in the script.

By following the setup instructions, you can deploy and run the pipeline, and use the logging information to monitor its performance and troubleshoot any issues that arise.




# ADDITIONAL QUESTIONS

### 1.How would you deploy this application in production?

