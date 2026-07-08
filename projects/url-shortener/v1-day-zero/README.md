# URL Shortener — Version 1: Day Zero (Baseline)

This is the first evolutionary milestone of the URL Shortener project. In this stage, the focus is on taking a standard Python Flask backend application, containerizing it using Docker for environment consistency, and deploying it live to the AWS cloud via a single AWS EC2 instance.

### Core Objectives of this Iteration:
1. Accept a long URL and return a unique short identifier string.
2. Accept a short identifier string and seamlessly redirect the user's browser back to the original long URL.

## System Design Primer: Core Foundations
Before writing code or provisioning infrastructure, building any production-ready system requires addressing fundamental architectural questions. Below is the conceptual blueprint and engineering rationale behind this URL shortener.

### 1. Functional vs. Non-Functional Requirements
Think of this as what the system does versus how well it performs its duties.

- **Functional Requirements (Features):** The direct actions a user can take. For this system, a user submits a long URL and receives a shortened token, or they visit a shortened URL and are automatically redirected to the original destination.
- **Non-Functional Requirements (System Qualities):** The operational boundaries. This includes **high availability **(the service stays online), **minimal latency** (redirection happens in milliseconds), and **scalability** (the ability to handle sudden traffic spikes).

### 2.System APIs
These are the entry points or REST endpoints that the web server exposes to the internet. A baseline URL shortener requires two primary routes:

- `POST /api/v1/shorten` — Accepts a long URL payload and returns a shortened string token.
- `GET /{short_url_id}` — Accepts the short token from the browser and issues an HTTP 302 Found redirect to the original destination.

### 3. Database Selection
A critical choice must be made between Relational (SQL) and Non-Relational (NoSQL) storage:

- **Data Structure:** This application stores incredibly simple data mapping (e.g., `short_id` $\rightarrow$ `long_url`). There are no complex relational tables or heavy joins.
- **The Decision:** Because the data model is simple, highly read-heavy, and must eventually scale horizontally, a NoSQL key-value store (like AWS DynamoDB) is highly efficient. However, for this **"Day Zero"** baseline, a lightweight SQL database (like PostgreSQL or MySQL via AWS RDS) is also a highly predictable and common starting point.

### 4. URL Shortening Algorithms
How do we reliably compress a massive URL into a clean 6 or 7-character token?

- **Approach A: Hashing (MD5 / SHA-256):** We can hash the long URL and encode the result using Base62 (`a-z`, `A-Z`, `0-9`). The bottleneck here is **collisions**—two different long URLs could theoretically yield the same hash, requiring complex database lookup logic to detect and resolve conflicts.
- **Approach B: Unique ID Generation (Recommended):** Instead of hashing, every single incoming request is assigned a globally unique, sequential ID (e.g., `100,000,001`). This base-10 ID is then converted into a Base62 string (e.g., `100,000,001` $\rightarrow$ `6Yg7`). This completely eliminates collisions because every generated ID is guaranteed to be unique.

### 5. Key Generation Service (KGS)
While the Unique ID approach is highly reliable, hitting a single database to fetch the "next sequential number" creates a massive write bottleneck at scale.

- A **KGS** is a dedicated microservice that pre-generates random, unique tokens in advance and stores them in a rapid-access cache. When the URL shortener needs a token, it doesn't compute anything or lock a database row; it simply pulls an unused token from the KGS, marks it as used, and pairs it with the user's URL

### 6. Storage Space Estimation
Before provisioning cloud infrastructure, we must forecast data storage requirements over time to right-size our database hardware.

- **Assumptions:** Assume an influx of **10 million** new URLs per month. Each database row (Long URL + Short ID + Timestamp) consumes roughly **500 bytes** of data.
$$\text{Total Storage per Month} = 10,000,000 \times 500\text{ bytes} \approx 5\text{ GB}$$

- **5-Year Projection:** Over a span of five years, this amounts to roughly **300 GB**. Knowing this data footprint helps us realize that a standard, budget-friendly database storage tier can easily handle our data for years without needing immediate, massive cluster scaling.
---

##  Architecture Overview

- **Backend Framework:** Python / Flask
- **Containerization Engine:** Docker
- **Cloud Infrastructure:** AWS EC2 (Ubuntu)
- **Networking/Security:** AWS Security Groups opening inbound TCP port `5000` to the internet and port `22` for SSH management.

---

##  Step-by-Step Implementation Guide

### 1. Local Development & Containerization
To test and build this application on your local machine:

- **Clone the repository and navigate here:**
   ```bash
   cd projects/url-shortener/v1-day-zero
  ```
- **Build the isolated Docker image:**
    ```bash
  docker build -t url-shortener .
  ```
-  **Run the container locally (mapping port 5000):**
     ```bash
    docker run -p 5000:5000 url-shortener
   ```
- **Verify it works by sending a local HTTP request:**
    ```bash
    curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "[https://www.google.com](https://www.google.com)"}'
  ```
-   **Push the Docker image to a registry (like Docker Hub) so your cloud server can pull it down:**
    ```bash    
    docker login
    docker tag url-shortener YOUR_DOCKERHUB_USERNAME/url-shortener:latest
    docker push YOUR_DOCKERHUB_USERNAME/url-shortener:latest
    ```


### 2.  Shipping to the Cloud (AWS EC2)
To replicate the deployment on an active cloud server:

- **Provision Infrastructure:** Launch an Ubuntu `t2.micro` EC2 instance on AWS. Ensure your inbound security group rules allow traffic on port `5000` (for application traffic) and port `22` (for your SSH access).
- **Prepare the Host Environment:** SSH into the EC2 instance and install Docker:
    ```bash
    sudo apt-get update && sudo apt-get install -y docker.io
    sudo usermod -aG docker ubuntu && newgrp docker
   ```
- **Pull the image from Docker Hub, and run it:**
    ```bash
    docker run -d -p 5000:5000 --name web-app YOUR_USERNAME/url-shortener:latest
   ```
- **Test the live cloud app:** Open your local terminal tab and run `curl` command against your EC2 Public IP address instead of `localhost`:
    ```bash
    curl -X POST http://YOUR_EC2_PUBLIC_IP:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "[https://www.google.com](https://www.google.com)"}'
  ```