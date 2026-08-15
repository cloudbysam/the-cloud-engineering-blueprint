# URL Shortener — Version 3: Serverless Microservices & In-Memory Caching

This is the third evolutionary milestone of the URL Shortener project. Building directly upon the multi-AZ infrastructure of Version 2, Version 3 modernizes compute to serverless containers with AWS ECS Fargate, introduces a Redis-backed Key Generation Service (KGS) and read-through caching using Amazon ElastiCache Serverless, and replaces the development server with a multi-worker Gunicorn WSGI server.

## Architecture Overview

```text
                                [ Public Internet ]
                                         │
                                         ▼
                           [ Application Load Balancer ]
                               (Public Subnets / ALB)
                                         │
                                         ▼
                           [ AWS ECS Fargate Cluster ]
                       (Serverless Containers + Gunicorn)
                                  │             │
                    ┌─────────────┘             └─────────────┐
                    ▼                                         ▼
    [ ElastiCache Serverless Redis ]              [ AWS RDS PostgreSQL ]
    (KGS Pool & Read-Through Cache)                (Multi-AZ / Private)
```

## Key Architectural Highlights

- **Serverless Container Compute:** Migrated compute from manual EC2 instances to **AWS ECS (Fargate)** running production-grade **Gunicorn** WSGI servers, eliminating server OS management, patching, and AMI maintenance.
- **Key Generation Service (KGS):** Implemented an in-memory Redis set (`kgs_pool`) that pre-generates Base62 keys in advance, delivering $O(1)$ key allocation and eliminating real-time database collision locks.
- **Sub-Millisecond Read-Through Caching:** Integrated **Amazon ElastiCache Serverless (Redis)** in front of RDS with a 1-hour sliding TTL, completely bypassing PostgreSQL queries on cache hits.
- **Resilient & Fault-Isolated Networking:** Configured dynamic SSL/TLS socket connections, automatic database startup connection retries, and strict multi-AZ Security Groups across ALB, ECS, RDS, and ElastiCache.

## Tech Stack

- **Language & Framework:** Python 3.11, Flask, Flask-SQLAlchemy, Gunicorn WSGI
- **Database & Cache:** PostgreSQL (AWS RDS), Redis (Amazon ElastiCache Serverless)
- **Containerization & Registry:** Docker, Amazon Elastic Container Registry (ECR)
- **Cloud Infrastructure (AWS Console):** VPC, AWS ECS (Fargate Tasks & Services), Application Load Balancer (ALB), Amazon RDS (PostgreSQL), Amazon ElastiCache Serverless (Redis)
- **Load Testing & Benchmarking:** Locust

## Environment Configuration

The application consumes database and cache parameters dynamically via environment variables, automatically detecting whether to enable TLS/SSL for cloud endpoints:

```bash
DB_USER="postgres"
DB_PASSWORD="<your-rds-password>"
DB_HOST="<your-rds-endpoint-url>"
DB_NAME="url_db"
REDIS_HOST="<your-elasticache-serverless-endpoint-url>"
REDIS_PORT="6379"
```

## Production Deployment Steps (AWS)

- **Container Registry Push:** Build and push the Gunicorn-enabled Docker image to **Amazon ECR**.
- **Managed Storage & Cache Provisioning:** Provision an **Amazon RDS PostgreSQL** instance and an **Amazon ElastiCache Serverless Redis** cluster in private subnets.
- **Security Group Networking:** Configure strict inbound security rules allowing ECS tasks access to RDS (Port `5432`) and ElastiCache (Ports `6379` & `6380`).
- **ECS Task Definition & Service Setup:** Create an ECS Task Definition on Fargate with container environment variables, and launch an ECS Service attached to the Application Load Balancer target group.
- **ALB Deployment & Routing:** Attach the ECS Fargate tasks to an ALB target group probing `/health` on Port `5000`.

## Post-Deployment Inspection & Verification Checklist

1. **Application Load Balancer (ALB) Routing Test**
   - **Goal:** Confirm the ALB receives public HTTP traffic and routes it to the running Fargate task containers.
      ```bash
      curl -i http://<YOUR-ALB-DNS-NAME>/health

      # Expected output:
     HTTP/1.1 200 OK with JSON response {"status":"healthy"}.
     ```
2. **End-to-End API Persistence & Redirection**
   - **Goal:** Verify that a shortened URL created via the ALB uses the KGS pool, writes to RDS, and caches in ElastiCache Serverless.

        ```bash
     # Create Short URL:
     curl -X POST http://<YOUR-ALB-DNS-NAME>/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "[https://aws.amazon.com/ecs/](https://aws.amazon.com/ecs/)"}'

     # Test Redirection (First request hits Redis Read Cache):
     curl -i http://<YOUR-ALB-DNS-NAME>/<short_code>

     # Expected Output:
     HTTP/1.1 302 FOUND pointing Location: [https://aws.amazon.com/ecs/](https://aws.amazon.com/ecs/)
     ```
3. **High-Concurrency Load Testing with Locust**
   - **Goal:** Benchmark peak throughput, response latency, and system stability under simulated heavy traffic.

## Running the Load Test

1. **Install Locust locally:**
    ```bash
    pip install locust
    ```
2. **Launch Locust targeting the ALB endpoint:**

    ```bash
    locust -f locust.py
    ```
3. Open `http://localhost:8089` in your browser and run `50 virtual users` with a spawn rate of `10 users/sec`.   

## Traffic Flow Under Load
```text

                                 Locust
                                    │
                             14,912 requests
                                    │
                                    ▼
                                   ALB
                                    │
                           ┌────────┴────────┐
                           ▼                 ▼
                       ECS Task          ECS Task
                           │                 │
                           └────────┬────────┘
                                    │
                           ┌────────┴────────┐
                           ▼                 ▼
                         Redis              RDS
                      Cache + KGS        PostgreSQL
```

## Endpoint Performance Breakdown

| Endpoint | Requests | Failures | Avg Latency | Median (p50) | p95 | Max Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `GET /<short_code>` | 11,881 | 0% | 249 ms | 230 ms | 350 ms | 1.13 s |
| `POST /shorten` | 2,981 | 0% | 253 ms | 240 ms | 350 ms | 820 ms |
| **Total / Aggregated** | **14,912** | **0%** | **251 ms** | **230 ms** | **350 ms** | **1.13 s** |

**Key Takeaway:** Across nearly 15,000 sustained requests, the Redis KGS pool and read-through caching maintained a **0% failure rate** and a **230 ms median response time**, effectively eliminating database lock contention under heavy concurrent writes, validating the scalability of the ECS, Redis, and PostgreSQL architecture.
