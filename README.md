# Flask Kubernetes Observability

A production-ready Flask application deployed on Kubernetes with full observability stack (Prometheus + Grafana).

---

## Architecture
Request → Service (port 80) → Flask Pod 1 (port 5000)
→ Flask Pod 2 (port 5000)
Prometheus → scrapes /metrics → stores data
Grafana    → reads Prometheus → displays dashboards

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + Flask | REST API |
| Docker | Containerization |
| Kubernetes (Kind) | Container orchestration |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |
| Helm | Kubernetes package manager |
| kubectl | Kubernetes CLI |

---

## Project Structure
flask-kubernetes-observability/
├── app/
│   └── main.py          # Flask REST API
├── k8s/
│   ├── deployment.yml   # 2 replicas Flask deployment
│   └── service.yml      # ClusterIP service
├── Dockerfile           # Container recipe
└── requirements.txt     # Python dependencies

---

## Kubernetes Concepts Used

**Deployment** — Declares 2 Flask replicas. If a pod crashes, Kubernetes automatically recreates it (auto-healing).

**Service** — Provides a stable IP address and load balances traffic between the 2 pods.

**Namespace** — Logical isolation between app (default) and monitoring (monitoring).

**Zero Downtime** — With 2 replicas, the app stays available even when one pod is restarting.

---

## API Endpoints

| Endpoint | Method | Response |
|----------|--------|----------|
| `/` | GET | App status + pod name + node name |
| `/health` | GET | Health check |
| `/metrics` | GET | Prometheus metrics |

---

## Getting Started

### Prerequisites

- Docker Desktop
- Kind
- kubectl
- Helm

### Create the cluster

```bash
kind create cluster --name flask-cluster
```

### Build and load the image

```bash
docker build -t flask-k8s:v1 .
kind load docker-image flask-k8s:v1 --name flask-cluster
```

### Deploy the application

```bash
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
```

### Verify

```bash
kubectl get pods
kubectl get services
```

### Access the app

```bash
kubectl port-forward service/flask-service 8080:80
```

Visit `http://localhost:8080`

---

## Monitoring Setup

### Install Prometheus + Grafana with Helm

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### Access Grafana

```bash
# Get password
kubectl --namespace monitoring get secrets monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d ; echo

# Port forward
kubectl --namespace monitoring port-forward service/monitoring-grafana 3000:80
```

Visit `http://localhost:3000` — login with `admin` and the password above.

---

## Key Features Demonstrated

- Auto-healing : deleted pod recreated in under 1 second
- Load balancing : traffic distributed between 2 pods
- Zero downtime : app always available during pod restarts
- Real-time monitoring : CPU, RAM, network metrics in Grafana
- Infrastructure as Code : everything defined in YAML files

---

## What I Learned

- Deploying applications on Kubernetes
- Writing Deployment and Service YAML manifests
- Understanding pods, nodes, replicas and labels
- Implementing auto-healing and zero downtime
- Setting up observability with Prometheus and Grafana
- Using Helm to install complex applications on K8s

---

## Author

**Yosra Benali**
Cloud & DevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-yosrabnali-black)](https://github.com/yosrabnali)