# Lab 1 - Virtualization and Cloud

## Objective
This lab explores virtualization concepts, cloud infrastructure, and latency behavior in cloud-based applications.

---

## Application Overview

A Flask-based API was implemented to simulate a cloud service with variable response times.

The application introduces random delays to mimic real-world latency in distributed systems.

---

## VM vs Container Comparison

| Feature        | Virtual Machine (VM) | Container |
|----------------|---------------------|----------|
| Startup Time   | Minutes              | Seconds  |
| Resource Usage | High                | Low      |
| Isolation      | Strong              | Moderate |
| OS             | Full OS             | Shared Kernel |

---

## Observations

- Containers start significantly faster than virtual machines.
- Containers consume fewer system resources.
- VMs provide stronger isolation but with higher overhead.

---

## Latency Analysis

The application simulates latency using random delays.

### Key Observations:
- Response times vary between requests.
- A long-tail distribution appears under repeated calls.
- This reflects real-world cloud latency behavior.

---

## Latency Histogram

![Latency Histogram](screenshots/latency.png)

---

## AWS Exploration

Amazon EC2 instances use the Nitro Hypervisor, which offloads virtualization tasks to dedicated hardware components.

This enhances:
- Performance
- Security
- Isolation

### EC2 Instance Example

![AWS EC2 Instance](screenshots/aws-ec2.png)
The instance is shown in a running state, demonstrating a typical cloud deployment environment.

The EC2 instance is shown in a running state within a standard AWS region, representing a typical cloud deployment environment.
---

## Tail Latency

Tail latency refers to the slowest responses in a system.

In this experiment:
- Most responses are fast
- A few requests take longer
- This creates a long-tail distribution

---

## How to Run

### Build Docker Image
docker build -t lab1 .

### Run Container
docker run -p 5000:5000 lab1

### Access
http://localhost:5000

---

## Conclusion

Containers provide a more efficient environment for microservices, while virtual machines offer stronger isolation.

Latency behavior in cloud applications is variable, and understanding tail latency is critical for system design.
