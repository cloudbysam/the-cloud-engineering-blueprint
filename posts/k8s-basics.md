# Container Orchestration Essentials: Kubernetes Basics

By Samuel (cloudbysam) | September 2026 | Categories: Kubernetes, Containers, DevOps

While Docker allows you to package and run an application inside a container, managing hundreds of containers running across a fleet of virtual machines introduces new challenges: *How do you automatically restart crashed containers? How do you scale up during traffic spikes? How do you update code with zero downtime?* 

This is where **Kubernetes (K8s)** comes in—the open-source container orchestration platform designed to automate container deployment, scaling, and operations.

---

## On this page
* Why Kubernetes?
* Core Architecture (Control Plane & Worker Nodes)
* Foundational Objects (Pods, Deployments, Services)
* Prerequisites & Local Setup (`minikube` / `kubectl`)
* Step-by-Step Manifest Walkthrough
* Essential `kubectl` Commands
* Common Pitfalls

---

## Why Kubernetes?

Docker handles the container **runtime**, but Kubernetes provides the container **orchestration**:

* **Auto-healing:** Restarts failed containers, replaces pods, and kills un-responsive nodes automatically.
* **Horizontal Scaling:** Scales application instances up or down based on CPU, memory, or custom metrics.
* **Load Balancing:** Automatically distributes network traffic across pods to ensure high availability.
* **Zero-Downtime Rollouts:** Deploys new application code gradually (Rolling Updates) without dropping active user connections.

---

## Core Architecture

A Kubernetes cluster is divided into two primary parts:

1. **Control Plane (Master Node):** The brain of the cluster. It makes global decisions (scheduling pods, detecting node failures, maintaining desired cluster state). Key components include `kube-apiserver`, `etcd`, and `kube-scheduler`.
2. **Worker Nodes:** The muscle of the cluster. Physical or virtual machines that actually run your containerized applications under the control of the `kubelet` agent.

---

## Foundational Objects

Kubernetes uses declarative YAML manifests to state **what** you want your system to look like:

* **Pod:** The smallest deployable unit in Kubernetes. A Pod wraps one or more co-located containers (usually just a single application container).
* **Deployment:** Manages the lifecycle of Pods. It declares how many identical Pod replicas should run, handles rolling updates, and automatically replaces dead Pods.
* **Service:** Defines a persistent logical endpoint and network policy to expose a group of Pods internally or to the public internet (e.g., `ClusterIP`, `NodePort`, `LoadBalancer`).

---

## Prerequisites & Local Setup

1. Enable **Kubernetes** inside Docker Desktop settings, or install **Minikube** locally.
2. Install the Kubernetes command-line interface tool, **`kubectl`**.
3. Verify your connection to the cluster:
   ```bash
   kubectl cluster-info
    ```
## Step-by-Step Manifest Walkthrough
Create a file named `nginx-deployment.yaml` to define your application deployment and service exposure in declarative YAML:    

```YAML
---
# 1. Define the Deployment Object
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-web-deployment
  labels:
    app: nginx-web
spec:
  replicas: 3 # Run 3 identical instances for high availability
  selector:
    matchLabels:
      app: nginx-web
  template:
    metadata:
      labels:
        app: nginx-web
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80

---
# 2. Define the Service Object to expose traffic
apiVersion: v1
kind: Service
metadata:
  name: nginx-web-service
spec:
  type: LoadBalancer
  selector:
    app: nginx-web
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

## Essential `kubectl` Commands
Run these core imperative commands from your terminal:

### 1. Apply Manifests (Deploy)
Apply your configuration to the cluster:

```bash
kubectl apply -f nginx-deployment.yaml
```

### 2. Inspect Cluster State
Check the health of your Pods, Deployments, and Services:

```bash
# List all running pods
kubectl get pods

# View deployment details and replica count
kubectl get deployments

# List services and IP addresses
kubectl get svc
```

### 3. Debugging & Troubleshooting
When a Pod fails to start, inspect its detailed events or output its logs:

```bash
# View live events and errors for a specific pod
kubectl describe pod <POD_NAME>

# Stream live container logs
kubectl logs -f <POD_NAME>
```

## 4. Teardown
Cleanly destroy resources defined in your manifest:

```bash
kubectl delete -f nginx-deployment.yaml
```

## Common Pitfalls

- **Using the `latest` Image Tag in Production:** Specifying `image: nginx:latest` can lead to unpredictable deployments if the image updates behind the scenes. Always use explicit version tags (e.g., `nginx:1.25.3`).

- **Omitting Resource Limits:** Failing to specify `resources.requests` and `resources.limits` (CPU and Memory) can cause a single leaky container to consume all node resources and crash neighbouring Pods.