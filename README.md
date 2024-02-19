# Senior DevOps Engineer Technical Challenge


## Scenario
The product the engineering team is working on will use an event-driven architecture based on kafka and you are responsible for the infrastructure. The backend team has 2 microservices: `consumer` and `producer` which consist of a python application that reads and writes messages to kafka. The team has asked you to set up a kafka cluster and deploy the microservices to it.
The system should be able to handle a large volume of data and ensure high availability.


## Challenge Overview

## Instructions

1. Kafka Cluster:

- Set up an Apache Kafka cluster with at least two brokers.
- Define a topic called `posts` and propose a partition and replication strategy. Explain your reasoning.
- Your setup should also help the backend developers to test their python application locally.

$${\color{lightgreen}Solution : 1. Kafka Cluster}$$
- Researched about this and used the Bitnami's kafka helm chart to deploy the kafka cluster with 3 nodes, of which all act in the `controller+broker` roles in the Raft algorithm(without zookeeper). Refer to the kafka specific values in `helm-app/values.yaml`.
- Raft Algorithm is selected as it best suited to bring up high availability and fault-tolerance by possibly rewamp the cluster and recover the metadata by switching the master through election in case of master failure.
- In perspective of scalability, this template is so friendly to include more nodes, can be `controller+broker`, `controller` or `broker` role, provided if you move to `controller`/ `broker`, you need to migrate all existing `controller+broker` nodes to either `controller`/ `broker` and viceversa.
- Additionally pod disruption budget is maintained with `maxUnavailable` set to 1 to make sure consistency across kubernetes node replacements and other housekeeping activities.
- Topic provisioning is done using kafka provisioner component, we create the `posts` topic with partition set to 3 and replication factor 3 to ensure better distribution of the data along all the broker nodes in the cluster.
- How to Deploy the solution.
```
git clone https://github.com/jpadmin/buildingminds-task.git
cd buildingminds-task/helm-app
helm dependencies build
kubectl create ns kafka
helm install buildingminds-kafka ./ -n kafka
```

2. Containerization & Deployment:
- The python applications have an initial docker container, make some improvements to it using best practices for containerization.
- Deploy the applications to your Kubernetes cluster.

$${\color{lightgreen}Solution : 2. Containerization And Deployment}$$
- Changes for the Dockerfiles has been added to producer and consumer application files with best practices steps by including the frequently changing part of the application towards end of the dockerfile, there by bring meaningful layers in the docker images and increased reusability of layers across the two application. Also the application layer has been taken away from the root or privileged access part of the container to an application user. This however can also be controlled by setting the required capabilities in the kubernetes layer, however this approach is taken to restrict this to docker/container layer.
- Also the necessary templates has been added to the `helm-app/templates` folder to add this layer to our kubernetes application.
- How to Deploy the solution with consumer and producer application.
```
#Build the docker image with new changes we made
cd buildingminds-task/producer
docker build -t johnpaulkj/kafka-producer:latest .
docker push johnpaulkj/kafka-producer:latest

cd buildingminds-task/consumer
docker build -t johnpaulkj/kafka-consumer:latest .
docker push johnpaulkj/kafka-consumer:latest

#Ensure producer and consumer values are in helm values file and templates are there in templates folder
helm upgrade buildingminds-kafka ./ -n kafka

#Verify the producer logs
kubectl logs -n kafka bm-app-producer-6kdnq          
Defaulted container "bm-app-producer" out of: bm-app-producer, init-container (init)
message 0 sent to topic posts
message 1 sent to topic posts
message 2 sent to topic posts
message 3 sent to topic posts
message 4 sent to topic posts

# Though the messages are not recieved in consumer
kubectl logs -n kafka bm-app-consumer-9b547b5b9-p8v8n
Defaulted container "bm-app-consumer" out of: bm-app-consumer, init-container (init)
Listening for messages on topic 'posts'...
```

3. IaC:
- Set your infrastructure as code using best practices. Think of how would you upgrade the kafka version, add more brokers, manage topics, etc.

$${\color{lightgreen}Solution : 3. IaC}$$
- For this I have created a custom helm values file, which will upgrade our existing cluster to 3.5 and also create another topic with name update. See the helm infrastructure values file `helm-app/upgrade.yaml`.
- How to deploy our solution
```
cd buildingminds-task/helm-app
helm upgrade buildingminds-kafka ./ -n kafka -f upgrade.yaml
```
- Wait for the rollout is complete, now we can verify the changes.
```
# Verify the kafka version from the broker
kubectl exec -it buildingminds-kafka-controller-0 bash -n kafka
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.
Defaulted container "kafka" out of: kafka, kafka-init (init) 
I have no name!@buildingminds-kafka-controller-0:/$ kafka-topics.sh --version
3.5.2
I have no name!@buildingminds-kafka-controller-0:/$

# We can also list the topics to confirm we have a topic named 'update'
I have no name!@busybox2:/$ kafka-topics.sh --bootstrap-server buildingminds-kafka.kafka.svc.cluster.local:9092 --list
__consumer_offsets
posts
update
I have no name!@busybox2:/$
```

4. Observability (Optional):
- Set up (or explain how to set) monitoring and alerting for your Kafka cluster.

$${\color{lightgreen}Solution : 4. Observability}$$
- For enabling Observability, we can make use of the kafka exporter that comes by default with chart, to enable this we can run:
```
cd buildingminds-task/helm-app
helm upgrade buildingminds-kafka ./ -n kafka -f upgrade.yaml --set 'kafka.metrics.kafka.enabled=true'
```
- After adding the exporter pod along with the cluster with previous, we will get buildingminds-kafka-metrics service in kubernetes with the metrics url in buildingminds-kafka-metrics.kafka.svc.cluster.local:9308/metrics

- From this URL, we can add a scrapping job in prometheus with this metrics url and after obtaining kafka metrics in prometheus and necessary alerts can be created by setting up the PromQL thresholds and create alerts to our endpoint devices like Slack / OpsGenie / PagerDuty with the help of alertmanager tool packed with prometheus.

Notes:
- We recommend you to use minikube, but you can also use kind, aks, or any other provider of your choice.
- Ask questions if something is unclear, we are here to help :)
- It is okay to make some assumptions but document and communicate them.
- Your focus should not be on the python application, but on its infrastructure.

## Evaluation Criteria:
- Containerization and deployment
- Automation degree of the infrastructure
- Correct configuration of Kafka
- Accounting for availability, scalability, and fault tolerance

## Deliverables:
- Code
- Documentation
- Showcase your work in a live demo

$${\color{lightgreen}Verification : Message Passing}$$

At Producer
```
I have no name!@busybox2:/$ kafka-console-producer.sh  --bootstrap-server buildingminds-kafka.kafka.svc.cluster.local:9092 --topic posts
>hi
>welcome to building minds test
>bye
>I have no name!@busybox2:/$
```

At Consumer
```
I have no name!@busybox2:/$ kafka-console-consumer.sh --bootstrap-server buildingminds-kafka.kafka.svc.cluster.local:9092 --topic posts --from-beginning
hi
welcome to building minds test
bye
^CProcessed a total of 3 messages
I have no name!@busybox2:/$
```