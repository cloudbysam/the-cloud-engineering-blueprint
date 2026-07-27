# URL Shortener — Version 2: High Availability & Managed Persistence

This is the second evolutionary milestone of the URL Shortener project. Building directly upon the single-instance foundation of Version 1, this stage transforms the application into an enterprise-grade, fault-tolerant cloud service deployed across multiple Availability Zones on AWS.

## Architecture Overview

```text
                        [ Public Internet ]
                                 │
                                 ▼
                   [ Application Load Balancer ]
                        (Public Subnets / ALB)
                       /                      \
                      ▼                        ▼
           [ EC2 Instance 1 ]            [ EC2 Instance 2 ]
           (Docker Container)            (Docker Container)
                       \                      /
                        ▼                    ▼
                   [ AWS RDS PostgreSQL Database ]
                         (Multi-AZ / Private)

```

## Key Architectural Highlights

- **Stateless Compute Layer:** Flask backend runs inside Docker containers on EC2 instances managed dynamically by an AWS Auto Scaling Group (ASG).
- **Load Balancing & Health Monitoring:** AWS Application Load Balancer (ALB) distributes incoming traffic across instances and performs automated HTTP /health probes.
- **Persistent Managed Storage:** Database state is moved completely out of the container memory into a centralized, durable **AWS RDS PostgreSQL** instance.
- **Elasticity & Self-Healing:** Auto Scaling Group automatically maintains target instance capacity, scaling up under high load and replacing unhealthy instances without downtime.

## Key Features & Endpoints

| Endpoint | Method | Description | Success Response                                                 |
| :--- | :--- | :--- |:-----------------------------------------------------------------|
| `/health` | `GET` | Probed by AWS ALB to assess instance status. | `200 OK` → `{"status": "healthy"}`                               |
| `/shorten` | `POST` | Hashes a long URL (MD5) and persists mapping in RDS. | `201 Created` → `{"short_url": "http://localhost:5000/99999eb"}` |
| `/<short_code>` | `GET` | Fetches long URL mapping from RDS and redirects user. | `302 Found` (Redirects to target URL) |

## Tech Stack

- **Language & Framework:** Python 3.11, Flask, Flask-SQLAlchemy
- **Database:** PostgreSQL (AWS RDS) using `psycopg2` driver
- **Containerization:** Docker & Docker Hub
- **Cloud Infrastructure (AWS Console):** VPC, EC2, Application Load Balancer (ALB) & Target Groups, Auto Scaling Group (ASG) & Custom AMI, Amazon RDS (PostgreSQL)

## Environment Configuration

The application consumes database configuration dynamically via environment variables, allowing the same Docker image to run locally or in AWS without hardcoding secrets:
```bash
DB_USER="<your-rds-username>"
DB_PASSWORD="<your-rds-password>"
DB_HOST="<your-rds-endpoint-url>"
DB_NAME="url_db"
```
## Local Development & Containerization
### 1. Start Local PostgreSQL Container
Before running the application, start a local PostgreSQL container mapped to host port 5432:

```bash
docker run -d \
  --name local-url-db \
  -e POSTGRES_USER="postgres" \
  -e POSTGRES_PASSWORD="password" \
  -e POSTGRES_DB="url_db" \
  -p 5432:5432 \
  -d postgres:15
```
### 2.Build and Run Application Container
Navigate to the project directory, build the image, and launch the container linked to host network/PostgreSQL:

```bash
# Navigate to project directory
cd projects/url-shortener/v2-high-availability

# Build Docker image
docker build -t url-shortener:v2 .

# Run container linked to local PostgreSQL via host bridge
docker run -d \
  -p 5000:5000 \
  -e DB_USER="postgres" \
  -e DB_PASSWORD="password" \
  -e DB_HOST="host.docker.internal" \
  -e DB_NAME="url_db" \
  --name url-app \
  url-shortener:v2
```
**Note on `host.docker.internal`:** This standard hostname allows the app container to reach port `5432` on your host system. On Linux systems, add `--add-host=host.docker.internal:host-gateway` to the `docker run` command if host resolution is restricted.

### 3. Quick Terminal check

```bash
# Verify Target Group Health Endpoint
curl -i http://localhost:5000/health

# Shorten a URL
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "[https://aws.amazon.com](https://aws.amazon.com)"}'

# Test redirection (replace <short_code> with returned hash)
curl -i http://localhost:5000/<short_code>

# Verify data in postgresql
docker exec -it local-url-db psql -U myuser -d url_db

# To list tables
\dt

# view the saved rows
SELECT * FROM url_mappings;
```

## Production Deployment Steps (AWS)

- **Database Setup:** Provision an **AWS RDS PostgreSQL** instance inside private subnets with a security group accepting inbound port `5432` strictly from EC2 instances.
- **Container Build & Registry:** Push the app image to Docker Hub containing the `/health` endpoint and dynamic host resolution using `request.host`.
- **Initial Compute & Container Setup:** Launch an EC2 instance, install Docker, pull the app image, and launch the container with production RDS credentials.
- **Load Balancer Configuration:** Deploy an ALB, create a Target Group probing HTTP /health on port `80` (expecting 200 OK), and attach the instance.
- **AMI & Launch Template:** Create an Amazon Machine Image (AMI) from the working EC2 instance and build an EC2 Launch Template with User Data startup script (`systemctl start docker && docker start url-app`).
- **Auto Scaling Group Setup:** Deploy an ASG across multiple Availability Zones attached to the Target Group, with target tracking scaling policies.

## Post-Deployment Inspection & Verification Checklist

To verify that all components of the Version 2 architecture are fully integrated and functioning, execute the following inspection steps:

---
### 1. Application Load Balancer (ALB) Routing Test
* **Goal:** Confirm the ALB receives public HTTP traffic and routes it to the underlying target group.
```bash
curl -i http://<YOUR-ALB-DNS-NAME>/health

# Expected output:
HTTP/1.1 200 OK with JSON response {"status":"healthy"}.  
```

### 2. End-to-End API Persistence & Redirection
* **Goal:** Verify that a shortened URL created via the ALB is written to RDS and redirected properly.

```bash
# Create Short URL:
curl -X POST http://<YOUR-ALB-DNS-NAME>/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "[https://aws.amazon.com](https://aws.amazon.com)"}'

# Inspect Response:
Ensure the returned short_url contains your ALB DNS domain (e.g., http://<YOUR-ALB-DNS-NAME>/<short_code>).

# Test Redirection:
curl -i http://<YOUR-ALB-DNS-NAME>/<short_code>

# Expected Output:
HTTP/1.1 302 FOUND pointing Location: https://aws.amazon.com
```
### 3. Database State Inspection (AWS RDS)
* **Goal:** Confirm that the EC2 instances write to and read from the central PostgreSQL database rather than local memory.

```bash
# Connect directly to your RDS database from an EC2 instance:
  psql -h <YOUR-RDS-ENDPOINT> -U <DB_USER> -d url_db
  
# Run a query to inspect the persisted records:
  SELECT * FROM url_mappings;
  
# Expected Result:
  Every short URL created via curl should appear as a row in the url_mappings table, regardless of which EC2 instance processed the HTTP request.
```
### 4. Auto Scaling & Self-Healing Verification
* **Goal:** Validate high availability and zero-downtime failover.
```bash
# Target Group Health Inspection:
Navigate to AWS Console > EC2 > Target Groups > url-shortener-tg. Verify that all of your EC2 instances show a green status of Healthy.

# Simulate Host Failure:
Navigate to EC2 Console > Instances, select one among your active instances launched by the ASG, and click Terminate.

# Active Monitoring: Run continuous requests against the ALB during termination:
while true; do curl -s -o /dev/null -w "%{http_code}\n" http://<YOUR-ALB-DNS-NAME>/health; sleep 1; done

# Expected Result:
The ALB continues returning 200 status codes without dropping requests. Within 2–3 minutes, the Auto Scaling Group automatically provisions a replacement EC2 target to restore desired capacity.
```
## Architectural Limitations & Flaws

While Version 2 solves data persistence and single points of failure, it introduces new enterprise-level limitations:

### 1. Database Read Bottleneck under High Concurrency

- **The Flaw:** Every single redirection request (`GET /<short_code>`) executes a synchronous read query against PostgreSQL.
- **The Impact:** Under massive viral traffic spikes, the database connection pool becomes saturated, causing latency spikes and degraded response times.

### 2.Manual Virtual Machine Management

- **The Flaw:** EC2 instances require underlying OS management, patching, AMI maintenance, and boot-up overhead during scaling events.
- **The Impact:** Slow scale-out times compared to modern serverless or lightweight container orchestrators.

## The Next Evolution: Moving to Version 3

In Version 3, we will address these limitations by migrating to a modern container platform and adding microservices caching:

- **Sub-Millisecond Read Caching:** Implementing **AWS ElastiCache (Redis)** in front of RDS to serve cached redirect lookups instantaneously.
- **Serverless Container Orchestration:** Migrating compute from manual EC2 instances to **AWS ECS (Fargate)** or **AWS App Runner**.