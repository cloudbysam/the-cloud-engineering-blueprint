# AWS Networking Essentials: Building Your First VPC Manually

By Samuel (cloudbysam) | August 2026 | Categories: AWS, Networking

Before launching servers or storing data in AWS, you must build a secure virtual network to hold them. A Virtual Private Cloud (VPC) is the isolated network environment where your cloud resources live.

---

## On this page
* What is an AWS VPC?
* Core Networking Components
* Step-by-Step Console Walkthrough
* Common Pitfalls
* Additional AWS Networking Concepts
* References

---

## What is an AWS VPC?
Amazon VPC allows you to provision a logically isolated section of the AWS cloud where you can launch AWS resources in a virtual network that you define. You have complete control over your virtual networking environment, including:
- Selection of your own IP address range (CIDR block)
- Creation and configuration of subnets
- Setup of route tables and network gateways

An AWS VPC enables you to securely run resources like Amazon EC2 instances, Amazon RDS databases, and Elastic Load Balancers (ELBs). Every AWS account comes with a default VPC out of the box, but building your own gives you full architectural control.

---

## Core Networking Components

To build a functional network, you need four key pieces:

| Component | Description |
| :--- | :--- |
| **VPC CIDR Block** | The range of primary IPv4 addresses assigned to your private network (e.g., `10.0.0.0/16`). |
| **Subnets** | Sub-sections of your VPC network tied to specific Availability Zones. <br>• **Public Subnet:** Contains routes to the internet, suitable for web servers.<br>• **Private Subnet:** Isolated from the public internet, used for backend databases. |
| **Internet Gateway (IGW)** | The virtual router connecting your public subnets to the outside internet. |
| **Route Tables** | A set of rules (routes) used to determine where network traffic is directed. |

---

## Step-by-Step Console Walkthrough

### 1. Create the VPC
1. Log in to the **AWS Management Console** and search for **VPC**.
2. Click **Create VPC**.
3. Select **VPC only**.
4. Name your project (e.g., `cloud-vpc`).
5. Set your IPv4 CIDR block (e.g., `10.0.0.0/16`).

### 2. Configure Subnets & Availability Zones
1. Search and select **Subnets**.
2. Click **Create Subnet** and select your VPC (`cloud-vpc`).
3. Assign a name and select an Availability Zone for your subnet.
4. Set your Subnet CIDR block (e.g., `10.0.1.0/24`).
> **Note:** If you create multiple subnets, ensure their CIDR ranges do not overlap with each other.

### 3. Create and Attach the Internet Gateway
1. Search for **Internet Gateways**.
2. Click **Create Internet Gateway**, name it (e.g., `cloud-igw`), and submit.
3. Select the newly created Internet Gateway, click **Actions > Attach to VPC**, and choose your VPC.

### 4. Create Route Tables
1. Search for **Route Tables**.
2. Click **Create Route Table**, name it `Public-RT`, select your VPC, and create.
3. Select `Public-RT`, go to the **Subnet Associations** tab, click **Edit subnet associations**, and attach the subnet you want to make public.
4. Go to the **Routes** tab, click **Edit routes**, and add a default route:
   - **Destination:** `0.0.0.0/0`
   - **Target:** `Internet Gateway` (select the IGW created in Step 3).

### 5. Enable Auto-Assign Public IPv4
1. Go to **Subnets** in the left menu.
2. Select the **Subnet** you made public.
3. Click **Actions > Edit subnet settings**.
4. Check **Enable auto-assign public IPv4 address** and save changes.

---

## Common Pitfalls

1. **Forgetting an Internet Gateway Route:** If your public subnet does not have a default route pointing to an Internet Gateway (`0.0.0.0/0 -> igw-xxx`), servers inside it will not be able to reach the internet or accept inbound SSH connections.
2. **Overlapping IP Ranges:** Choosing a CIDR range that overlaps with your home network, corporate network, or remote VPN will cause routing conflicts. Stick to standard private IP ranges (`10.0.0.0/16`, `172.16.0.0/16`, or `192.168.0.0/16`).

---

## Additional AWS Networking Concepts

- **AWS Regions:** A physical location around the world where AWS clusters data centers (e.g., `us-east-1`).
- **AWS Availability Zones (AZs):** One or more discrete data centers within an AWS Region providing redundancy and high availability (e.g., `us-east-1a`).
- **AWS Local Zones:** Extension of an AWS Region bringing compute and storage services closer to specific geographic areas for low latency.
- **AWS Edge Locations:** Global Points of Presence (PoPs) used as caching endpoints for services like Amazon CloudFront.
- **AWS Elastic IP Address:** A static, dedicated IPv4 address associated with your AWS account that can be dynamically reassigned.
- **AWS Security Groups:** Stateful virtual firewalls operating at the instance/ENI level.
- **AWS Network Access Control Lists (NACLs):** Stateless optional firewalls operating at the subnet level.
- **AWS NAT Gateway:** Managed service enabling private subnets to initiate outbound internet connections without accepting inbound traffic.
- **AWS Route 53:** Highly available cloud Domain Name System (DNS) web service.

---

## References

- [AWS Global Infrastructure: Regions and AZs](https://aws.amazon.com/about-aws/global-infrastructure/regions_az)
- [AWS Builder's Library: Minimizing Correlated Failures in Distributed Systems](https://builder.aws.com/content/3Ev2H7t312eZa9xBXiZCAjZ12JK/minimizing-correlated-failures-in-distributed-systems)
- [AWS Local Zones Features](https://aws.amazon.com/about-aws/global-infrastructure/localzones/features)
- [AWS VPC Documentation: Subnet Sizing](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html#subnet-sizing-ipv4)