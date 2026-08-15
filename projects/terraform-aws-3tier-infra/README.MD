# AWS 3-Tier Production Infrastructure (Terraform)

An automated, highly available, and secure 3-tier cloud architecture provisioned on **AWS** using Infrastructure as Code (IaC) with **Terraform**.

---


## Architecture Overview

The infrastructure isolates work into three distinct security and operational tiers across multiple Availability Zones (AZs):

```text
[ Internet ]
      │
      ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Public Subnets (AZ1 & AZ2)                                            │
│   ├── Application Load Balancer (ALB)                                 │
│   ├── NAT Gateway                                                     │
│   └── Bastion Host (Jump Box)                                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Private Application Subnets (AZ1 & AZ2)                               │
│   └── App Server Instances (EC2)                                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ 
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Isolated Database Subnets (AZ1 & AZ2)                                 │
│   └── Amazon RDS (PostgreSQL)                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## Key Architectural Highlights

- **Networking Tier:** Custom VPC with 6 subnets across 2 AZs (2x Public, 2x Private App, 2x Private DB), Internet Gateway, and NAT Gateway for outbound connectivity from private subnets.
- **Security Layer:** Strict, least-privilege Security Groups ensuring:
    -  security group chaining (ALB $\rightarrow$ Private App Tier $\rightarrow$ Isolated Database Tier).
    - Secure access path using a **Bastion Host (Jump Box)** for administrative SSH access to private instances.
- **Database Tier:** Managed RDS PostgreSQL running in isolated subnets with TLS 1.2 encryption enforced.

## Project Directory Structure

```text
terraform-aws-3tier-infra/
├── alb.tf              # Application Load Balancer, target groups, and listeners
├── ec2.tf              # Bastion host and App server EC2 instances
├── rds.tf              # RDS PostgreSQL database & DB subnet group
├── sg.tf               # Security Groups & firewall rules
├── vpc.tf              # VPC, subnets, route tables, IGW, and NAT Gateway
├── variables.tf        # Input variable definitions
├── outputs.tf          # Terraform output variables (ALB DNS, Bastion IP, RDS Endpoint)
└── README.md           # Project documentation, architecture diagram, and deployment guide
```

## Deployment Instructions

**Prerequisites**
- Terraform CLI installed
- AWS CLI configured with proper credentials
- An SSH Key Pair created in AWS 

**Step 1: Initialize Terraform**

Initialize the working directory and install the required AWS provider plugins:

```bash
terraform init
```

**Step 2: Validate & Plan Infrastructure**

Validate code syntax and generate an execution plan:

```bash
terraform validate
terraform plan
```

**Step 3: Provision Resources**

Apply the configuration to deploy the infrastructure on AWS:

```bash
terraform apply 
```

## Database & Connectivity Verification

To verify end-to-end network connectivity and database functionality, execute a test jump through the Bastion Host into the private Application Server, connect to RDS PostgreSQL over SSL/TLS, and perform database operations.

## Jump Topology

```test
[ Local Machine ] ──► (SSH) ──► [ Bastion Host ] ──► (SSH) ──► [ App Server ] ──► (psql / TLS) ──► [ RDS PostgreSQL ]
```

1. **SSH into Private App Server via Bastion Host**

    From your local terminal, hop into the Bastion Host, then jump to the private App Server:
    ```bash
    # Connect to Bastion Host
    ssh -i "N.Virginia-key.pem" ec2-user@<BASTION_PUBLIC_IP>

    # SSH into Private App Server
    ssh -i "N.Virginia-key.pem" ec2-user@10.0.10.111
    ```
2. **Connect to RDS PostgreSQL**

    Connect to the database instance from inside the App Server:
    ```bash
    psql -h <RDS_ENDPOINT> -p 5432 -U <DB_USERNAME> -d postgres
    ```

3. **Execute Verification Queries**

    Once connected at the `postgres=>` prompt, execute the following SQL test suite:   
    ```SQL
    -- 1. Create a test table
    CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 2. Insert test record
    INSERT INTO test_table (item_name) VALUES ('3-tier deployment successful!');

    -- 3. Query the table
    SELECT * FROM test_table;
    ```
   
## Output Verification:

```test
SSL connection (protocol: TLSv1.2)

 id |           item_name           |         created_at         
----+-------------------------------+----------------------------
  1 | 3-tier deployment successful! | 2026-08-14 16:33:30.051343
(1 row)
```

This confirms complete multi-tier network connectivity, proper security group chain routing, and isolated database write capabilities!

## Teardown

To destroy all provisioned AWS resources and avoid unnecessary charges:

```bash
terraform destroy 
```