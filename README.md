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
