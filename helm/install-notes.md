# Helm Install Notes

## Prerequisites
- minikube running with at least 4 CPUs and 6GB memory
- helm installed via brew

## Prometheus + Grafana
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring

helm install kube-prom-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.adminPassword=admin123
```

## Grafana Access
- URL: http://localhost:3000 (via port-forward)
- User: admin
- Pass: admin123
- RabbitMQ Dashboard ID: 10991

## Port Forwards
```bash
kubectl port-forward -n monitoring svc/kube-prom-stack-grafana 3000:80 &
kubectl port-forward -n monitoring svc/kube-prom-stack-kube-prome-prometheus 9090:9090 &
kubectl port-forward svc/rabbitmq-lab 15672:15672 &
kubectl port-forward svc/rabbitmq-lab 5672:5672 &
```
