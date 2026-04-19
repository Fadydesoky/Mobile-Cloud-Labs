# Lab 2 - Distributed Consistency and Cloud Systems

## Objective
This lab explores distributed systems concepts, consistency, and cloud-based deployments.

## Containers vs Virtual Machines
Containers are more efficient and scalable for modern cloud applications.
Virtual Machines provide stronger isolation and are useful for legacy systems.

## Cloud Infrastructure
Cloud platforms provide scalable resources and distributed environments for applications.

## Redis Replication

Redis replication demonstrates eventual consistency where replicas may lag behind the primary node.

## Network Partition

When a node is disconnected, writes may not propagate immediately, illustrating CAP trade-offs.

## Raft Consensus

etcd uses the Raft algorithm to elect a leader and maintain consistency across nodes.

## Experimental Setup

A simulated Redis replication environment was analyzed using two nodes.

A key was written to the primary node and read from a secondary node.

## Observation

The secondary node did not immediately reflect the written value, demonstrating eventual consistency behavior.

## Interpretation

This behavior reflects real-world distributed systems where replication is asynchronous and may introduce delays.

## Consistency
In distributed systems, maintaining consistency between nodes is challenging and depends on coordination and communication.

## Performance
System performance may vary depending on workload distribution and resource usage.

Consistency models like eventual consistency are commonly used in cloud systems to balance performance and reliability.

Distributed systems often sacrifice strong consistency in favor of availability and scalability (CAP theorem).
