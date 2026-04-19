## How to Run

### Build Image
docker build -f Dockerfile.basic -t lab3 .

### Run Container
docker run -p 5000:5000 lab3

### Kubernetes
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

## Observations

- Multi-stage Docker builds significantly reduce image size.
- Kubernetes ensures high availability through replica management.
- Self-healing behavior improves system reliability.

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
