# Kubernetes Setup Guide for Messaging App

This guide provides instructions for deploying the Django messaging app on Kubernetes.

## Prerequisites

1. **Docker** - For building container images
2. **Minikube** - For local Kubernetes cluster
3. **kubectl** - Kubernetes command-line tool
4. **wrk** (optional) - For load testing

## Setup Steps

### 1. Build Docker Image

First, build and tag your Docker image:

```bash
cd messaging_app
docker build -t messaging-app:latest .
docker build -t messaging-app:1.0 .
docker build -t messaging-app:2.0 .
```

### 2. Load Image into Minikube

```bash
minikube image load messaging-app:latest
minikube image load messaging-app:1.0
minikube image load messaging-app:2.0
```

### 3. Start Kubernetes Cluster

Run the setup script:

```bash
./kurbeScript
```

Or manually:

```bash
minikube start
kubectl cluster-info
```

### 4. Create ConfigMap and Secrets

```bash
kubectl apply -f mysql-config.yaml
```

### 5. Deploy the Application

```bash
kubectl apply -f deployment.yaml
```

Verify deployment:

```bash
kubectl get pods
kubectl get services
kubectl logs <pod-name>
```

### 6. Scale the Application

Run the scaling script:

```bash
./kubctl-0x01
```

This will:
- Scale to 3 replicas
- Verify pods are running
- Perform load testing with wrk
- Monitor resource usage

### 7. Set Up Ingress

Install Nginx Ingress Controller:

```bash
minikube addons enable ingress
```

Apply Ingress configuration:

```bash
kubectl apply -f ingress.yaml
```

Get the ingress IP:

```bash
minikube ip
```

Access the app at `http://<INGRESS_IP>/api/`

### 8. Blue-Green Deployment

Deploy both blue and green versions:

```bash
./kubctl-0x02
```

This will:
- Deploy blue version (1.0)
- Deploy green version (2.0)
- Check logs for errors
- Set up services for traffic switching

To switch traffic from blue to green, update `kubeservice.yaml`:

```yaml
selector:
  app: messaging-app
  version: green  # Change from blue to green
```

### 9. Rolling Updates

Apply rolling update:

```bash
./kubctl-0x03
```

This will:
- Apply updated deployment (version 2.0)
- Monitor rollout status
- Test for downtime with continuous curl requests
- Verify update completion

## Useful Commands

```bash
# Get pods
kubectl get pods

# Get services
kubectl get services

# Get deployments
kubectl get deployments

# View logs
kubectl logs <pod-name>

# Describe resource
kubectl describe pod <pod-name>

# Port forward
kubectl port-forward service/messaging-app-service 8000:8000

# Scale deployment
kubectl scale deployment messaging-app-deployment --replicas=3

# Check rollout status
kubectl rollout status deployment/messaging-app-blue

# View rollout history
kubectl rollout history deployment/messaging-app-blue

# Monitor resources
kubectl top pods
```

## Troubleshooting

1. **Pods not starting**: Check logs with `kubectl logs <pod-name>`
2. **Image pull errors**: Ensure images are loaded into minikube
3. **Database connection issues**: Verify ConfigMap and Secrets are created
4. **Ingress not working**: Check if ingress addon is enabled: `minikube addons list`

## Cleanup

To remove all resources:

```bash
kubectl delete -f deployment.yaml
kubectl delete -f blue_deployment.yaml
kubectl delete -f green_deployment.yaml
kubectl delete -f kubeservice.yaml
kubectl delete -f ingress.yaml
kubectl delete -f mysql-config.yaml
```

To stop minikube:

```bash
minikube stop
```

