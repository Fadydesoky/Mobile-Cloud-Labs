## How to Run

### Build Image
docker build -f Dockerfile.basic -t lab3 .

### Run Container
docker run -p 5000:5000 lab3

### Kubernetes (Simulation)
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

## Observations

- Multi-stage Docker builds significantly reduce image size.
- Kubernetes ensures high availability through replica management.
- Self-healing behavior improves system reliability.
- Kubernetes follows a declarative model where the system continuously maintains the desired state.

## Self-Healing

When a pod is deleted, Kubernetes automatically creates a new one to maintain the desired state.

## Reflection

### Why namespaces alone are not enough?
Namespaces isolate processes but do not limit resource usage.

### How do cgroups help?
They control CPU and memory usage, ensuring fair resource allocation.

### What is desired state?
Kubernetes continuously ensures the system matches the defined state.

### Difference between readiness and liveness?
Readiness checks availability, liveness checks health.

## Namespaces and cgroups

Namespaces isolate process visibility such as PID and network.
Cgroups control resource allocation like CPU and memory limits.

## Scheduling

Kubernetes automatically schedules pods to nodes based on available resources and constraints.


## Design Decisions

- Multi-stage builds were used to reduce image size.
- Kubernetes Deployment ensures scalability and fault tolerance.
- Probes improve system reliability by monitoring health.

## Practical Execution

Docker images were prepared and configured for building and execution.
Kubernetes configuration files were designed to represent deployment scenarios and expected orchestration behavior.

## Execution Note

The Kubernetes configuration files represent a deployment scenario for a containerized application.

The expected behavior includes:
- Automatic pod scheduling
- Replication management
- Self-healing in case of failure

## Critical Thinking

Although full Kubernetes cluster execution was not performed, the provided configurations reflect real-world deployment scenarios.

The system is designed to handle:
- Automatic scheduling of pods
- Fault tolerance through self-healing
- Load distribution using replicas

This demonstrates an understanding of how modern cloud-native systems operate in production environments.
