# Real-Time Streaming Data Pipeline

## Project Overview

This project sets up a real-time streaming data pipeline using Kafka and Docker. The pipeline ingests streaming data, processes it with advanced transformations, and stores the processed data in a new Kafka topic. The script also allows viewing the processed data.

### Prerequisites

- Docker
- Docker Compose
- Python
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

      * Kafka handles messages in batches, which improves throughput and reduces latency. This means multiple messages can be processed together, reducing the overhead associated with processing each message individually.

2. **Asynchronous Processing**:

      * The consumer and producer operations are asynchronous, ensuring non-blocking data processing. This allows the system to handle high-throughput data streams without being slowed down by synchronous operations.


### Scalability

1. **Kafka Consumer Groups**:

      * Multiple consumers can be part of a consumer group, allowing for parallel processing of messages and load distribution. This ensures that as the data load increases, more consumer instances can be added to handle the load.

2. **Horizontal Scaling**:

      * Kafka brokers and consumers can be scaled horizontally to handle increased load without performance degradation. This means we can add more brokers and consumers to your Kafka cluster to distribute the load more evenly and handle more data.


### Fault Tolerance

1. **Kafka Replication**:

      * Kafka topics can be configured with replication to ensure data availability even if a broker fails. This ensures that the data is not lost and can be recovered from another broker if one goes down.

2. **Error Handling**:

      * The script includes error handling for JSON decoding and general processing errors, logging detailed error messages for debugging. This ensures that any issues during message processing are logged and can be addressed without crashing the entire system.

3. **Docker Containers**:

      * Docker ensures that each component runs in an isolated environment, reducing the impact of failures and simplifying recovery. This isolation also ensures consistent environments across different stages of development and deployment.


## Conclusion

This real-time streaming data pipeline leverages Kafka and Docker to efficiently ingest, process, and store data. The design ensures scalability through Kafka's consumer groups and horizontal scaling, while fault tolerance is achieved through Kafka's replication and robust error handling in the script.

By following the setup instructions, you can deploy and run the pipeline, and use the logging information to monitor its performance and troubleshoot any issues that arise.




# ADDITIONAL QUESTIONS

## 1. How would you deploy this application in production?
   Deploying this application in production involves several steps to ensure reliability, scalability, and maintainability. Here's a high-level approach:

1. **Containerization**:

      * Ensure that all components (Kafka, Zookeeper, Consumer, Producer) are containerized using Docker.

2. **Orchestration**:

      * Use a container orchestration platform like Kubernetes to manage and scale the containers. Kubernetes provides automated deployment, scaling, and management of containerized applications.
Create Kubernetes manifests (YAML files) for deploying Kafka, Zookeeper, and the application services.

3. **Cloud Infrastructure**:

      * Deploy the application on a cloud platform like AWS, GCP, or Azure, which provides managed Kubernetes services (e.g., EKS, GKE, AKS).
Use managed Kafka services like AWS MSK, Confluent Cloud, or GCP Pub/Sub to offload the operational overhead of managing Kafka clusters.

4. **CI/CD Pipeline**:

      * Set up a CI/CD pipeline using tools like Jenkins, GitHub Actions, or GitLab CI to automate the build, test, and deployment process.
Ensure that every commit to the repository triggers the pipeline, running tests and deploying to a staging environment before production.

5. **Monitoring and Logging**:

      * Integrate monitoring tools like Prometheus and Grafana to monitor the health and performance of the Kafka cluster and application services.
Use centralized logging systems like ELK Stack (Elasticsearch, Logstash, Kibana) or EFK Stack (Elasticsearch, Fluentd, Kibana) to aggregate and analyze logs.


6. **Security**:

      * Implement security best practices such as securing communication channels with TLS, setting up authentication and authorization for Kafka using SASL and ACLs, and securing access to the Kubernetes cluster.


## 2. What other components would you want to add to make this production ready?
   To make the application production-ready, additional components and enhancements would be necessary:

1. **Data Persistence**:

      * Use a distributed, fault-tolerant storage system (e.g., HDFS, S3) for storing processed data to ensure durability and accessibility.

2. **Backup and Disaster Recovery**:

      * Implement backup strategies for Kafka data and application state to ensure quick recovery in case of failures.

3. **Configuration Management**:

      * Use tools like Helm or Kustomize for managing Kubernetes configurations and deployments.

4. **Service Mesh**:

      * Integrate a service mesh like Istio for managing microservices communication, traffic management, and security policies.

5. **Alerting**:

      * Set up alerting mechanisms using tools like Alertmanager to notify the operations team of any issues or anomalies in the system.

6. **Auto-Scaling**:

      * Configure auto-scaling policies for the Kafka cluster and application services to automatically scale based on the load and resource utilization.

7. **Schema Registry**:

      * Use a schema registry (e.g., Confluent Schema Registry) to manage and enforce data schemas, ensuring compatibility and consistency of messages.

8. **API Gateway**:

      * Implement an API gateway to manage and secure API calls, handle load balancing, and provide a single entry point for external consumers.


## 3. How can this application scale with a growing dataset?
   Scaling this application to handle a growing dataset involves both horizontal and vertical scaling strategies:

1. **Horizontal Scaling**:

      * **Kafka Brokers**: Add more Kafka brokers to the cluster to distribute the load and increase the capacity for handling more messages.
      * **Consumers**: Increase the number of consumer instances and use Kafka consumer groups to parallelize message processing. This allows multiple consumers to process messages from the same topic concurrently.
      * **Producers**: Scale the producers to handle higher data ingestion rates.

2. **Partitioning**:

      * Increase the number of partitions for Kafka topics to enable more parallelism. More partitions allow more consumers to read from the topic concurrently.

3. *Data Sharding*:

      * Implement data sharding strategies to split large datasets into smaller, manageable chunks. This can be done at the Kafka topic level by partitioning or at the application level by dividing the dataset into smaller logical segments.

4. *Auto-Scaling*:

      * Configure auto-scaling policies for the Kafka cluster and application services to dynamically adjust the number of instances based on the workload and resource utilization.

5. *Load Balancing*:

      * Use load balancers to distribute incoming requests across multiple producer and consumer instances to prevent any single instance from becoming a bottleneck.

6. *Optimizing Resource Usage*:

      * Monitor resource usage (CPU, memory, disk I/O) and optimize the application configuration and resource allocation to ensure efficient utilization.

7. *Data Retention Policies*:

      * Implement data retention policies in Kafka to manage the lifecycle of messages. Configure Kafka to automatically delete old messages based on time or size to prevent the cluster from being overwhelmed by old data.

8. *Caching*:

      * Use caching mechanisms (e.g., Redis, Memcached) to reduce the load on Kafka and application services by storing frequently accessed data in memory.

By following these strategies and incorporating the necessary components, the application can efficiently scale to handle a growing dataset while maintaining high performance and reliability.
