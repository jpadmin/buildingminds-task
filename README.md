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

3. IaC:
- Set your infrastructure as code using best practices. Think of how would you upgrade the kafka version, add more brokers, manage topics, etc.

4. Observability (Optional):
- Set up (or explain how to set) monitoring and alerting for your Kafka cluster.

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