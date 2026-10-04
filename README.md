# Cloud Engineering RoadMap 

Welcome to my study roadmap to becoming a professional Cloud Engineer. I created this repository to map out the exact skills, tools, and architectures required to master the cloud from scratch. 

Whether you are transitioning from standard software development or starting fresh, this checklist tracks the day-to-day essentials needed for modern cloud engineering.

---

##  Table of Contents
1. Phase 1: The Core Prerequisites
2. Phase 2: The Cloud Provider (AWS Focus)
3. Phase 3: Infrastructure as Code (IaC)
4. Phase 4: Containers & Architecture (The Shipping Containers of Code)
5. Phase 5: Generative AI in Cloud Engineering (The Future)
6. Hands-On Capstone Projects
7. Extra Learn (Networking)
---

## The Study Roadmap Checklist

### Phase 1: The Core Prerequisites
Before moving to the cloud, you must master the tools used to build and manage local applications.

- [ ] **Linux & Command Line ([Linux Essentials](./posts/linux-essentials.md)):** Learn how to navigate the terminal, manage file permissions, and write basic shell scripts.
- [ ] **Linux Processes & Signals ([Linux Processes](./posts/linux-processes.md)):** Learn how to view running processes, manage foreground/background tasks, and control programs using signals (kill, htop, ps).
- [ ] **Git & GitHub ([Git Essentials](./posts/git-essentials.md)):** Learn repository management, staging, committing, and how to safely undo mistakes using git reset.
- [ ] **Python Programming ([Python Essentials](./posts/python-essentials.md)):** Master functions, modular code design, decorators, and basic error handling for automation and cloud scripting.

---

### Phase 2: The Cloud Provider (AWS Focus)

To start using AWS cloud computing services, you must first create an [AWS account](https://aws.amazon.com/free/). This account acts as your primary gateway to a vast ecosystem of cloud infrastructure. Once your account is set up, you are ready to build in the cloud. 

While AWS offers hundreds of specialized tools, mastering the cloud begins with its four foundational pillars: **Networking, Compute, Storage, and Security**. 

- [ ] **Networking ([AWS VPC](./posts/vpc-manual.md)):** Learn how to build a Virtual Private Cloud, configure public/private subnets, internet gateways, and security firewalls.
- [ ] **Storage ([Amazon S3](./posts/s3-manual.md)):** Learn how to store and retrieve files securely in object storage.
- [ ] **Compute ([Amazon EC2](./posts/ec2-manual.md)):** Learn how to launch, configure, and connect to a virtual Linux server inside your custom network.
- [ ] **Security ([AWS IAM](./posts/iam-manual.md)):** Manage users, roles, and safe policies so your cloud resources remain protected.


---

### Phase 3: Infrastructure as Code (IaC)
**Why is this important?** In the real world, clicking buttons in the AWS console is slow, prone to human error, and impossible to scale across hundreds of servers. Infrastructure as Code (IaC) allows you to define your networks, storage, and servers in code files. This makes your infrastructure version-controlled, repeatable, and automated.

- [ ] **Terraform Basics ([Provisioning Tools](./posts/terraform-essentials.md)):** Learn how to write HashiCorp Configuration Language (HCL) to automatically provision AWS Services.
- [ ] **Ansible Basics ([Configuration Management](./posts/ansible-essentials.md)):** Learn how to automatically configure software, update packages, and manage files inside servers once they are deployed.
- [ ] **Advanced IaC ([Terraform Modules & Variables](./posts/terraform-advanced.md)):** Learn how to write modular, reusable code for multi-environment cloud deployments (Dev/Staging/Prod).

---
## Hands-On Capstone Projects

The best way to prove you are a cloud engineer is to build real things. Here are some milestone projects for practice:

### 1. High-Availability & Serverless URL Shortener (Enterprise SaaS)
* **The Goal:** Build and deploy a production-grade, highly available URL shortening service that scales dynamically, caches frequent redirections in memory, and persists mappings across multi-AZ databases.
* **Cloud Skills:** Docker containerization, AWS ALB & Auto Scaling Groups, Amazon RDS (PostgreSQL), AWS ECS Fargate serverless orchestration and AWS ElastiCache (Redis).

### 2. AWS 3-Tier Production Infrastructure (Terraform)
* **Goal:** Automated and provisioned a secure, multi-AZ, 3-tier cloud architecture on AWS using Infrastructure as Code (IaC) with modular Terraform.
* **Cloud & DevOps Tech Stack:** Terraform, AWS VPC, EC2, Amazon RDS (PostgreSQL), ALB, NAT Gateway, Security Groups, Git.

---

### Networking
Almost every problem you will debug as **cloud engineer** is a networking problem wearing a costume. A pod that will not start is often a DNS problem. A failing deployment is often a certificate problem. A 502 error is a conversation between two machines that went wrong somewhere specific, and knowing where saves you hours.

- [ ] **Communication model ([OSI and TCP/IP](./posts/communication_model.md)):** Learn how data travel across the internet in a reliable manner.
- [ ] **DNS ([Domain name system](./posts/DNS.md)):** Learn how the internet resolve domain name to the appropriate address.
- [ ] **IP and CIDR ([IP address and Subnetting](./posts/IP-Subnet.md)):** Learn how IP addresses are structured, allocated, and subnetted using Classless Inter-Domain Routing notation. 
- [ ] **TCP and UDP ([Transmission Control Protocol and User Datagram Protocol](./posts/transport_layer.md)):** Learn how data is delivered between applications using connection-oriented (TCP) versus connectionless (UDP) transport, ports, and flow control.
**Networking Practice ([Questions](./practices/networking-questions.md)):** Active-recall questions to test networking concepts.
- [ ] **Web Server Systemd Service ([Project](./projects/networking/web-server-unitfile)):** Hands-on unit file implementation for a background service.