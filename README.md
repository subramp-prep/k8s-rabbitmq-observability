# K8s RabbitMQ Observability Lab

A hands-on Kubernetes project demonstrating production-style observability
for a message broker workload.

## Architecture

```
[Producer] → [RabbitMQ on K8s] → [Consumer]
    ↓
[Prometheus]
    ↓
[Grafana Dashboard]
```

## Stack
- **Kubernetes** — minikube (local cluster)
- **RabbitMQ** — deployed via official Kubernetes Cluster Operator
- **Prometheus + Grafana** — deployed via kube-prometheus-stack Helm chart
- **Python** — pika-based producer and consumer apps

## What This Demonstrates
- Deploying stateful workloads via a Kubernetes Operator
- Writing ServiceMonitor CRDs to wire custom metrics into Prometheus
- Observing queue depth, message rates, and consumer lag in Grafana
- Kubernetes concepts: pods, namespaces, secrets, services, port-forwarding

## Quick Start

### 1. Start the cluster
```bash
minikube start --cpus=4 --memory=6g --driver=docker
```

### 2. Deploy observability stack
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install kube-prom-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.adminPassword=admin123
```

### 3. Deploy RabbitMQ
```bash
kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"
kubectl apply -f k8s/rabbitmq-cluster.yaml
kubectl apply -f k8s/rabbitmq-servicemonitor.yaml
```

### 4. Run the app
```bash
cd app
pip install -r requirements.txt

RABBIT_HOST=localhost RABBIT_USER=<user> RABBIT_PASS=<pass> python producer.py &
RABBIT_HOST=localhost RABBIT_USER=<user> RABBIT_PASS=<pass> python consumer.py
```

### 5. Open dashboards
| Service | URL | Notes |
|---|---|---|
| Grafana | http://localhost:3000 | admin / admin123 |
| RabbitMQ UI | http://localhost:15672 | see K8s secret |
| Prometheus | http://localhost:9090 | targets + queries |

## Key Concepts Learned

**Operators & CRDs** — The RabbitMQ Operator extends K8s with a
`RabbitmqCluster` resource type, handling cluster formation and storage
management automatically.

**ServiceMonitor** — A Prometheus CRD that declares which services to scrape
and at what interval, enabling automatic metrics discovery.

**Pull-based scraping** — Prometheus pulls metrics from targets on a schedule,
rather than targets pushing to a central collector.

**CPU Requests vs Limits** — Requests are used by the scheduler for pod
placement; limits are hard ceilings enforced at runtime.
EOF