# AWS Compute Essentials: Deploying an Amazon EC2 Instance Manually

By Samuel (cloudbysam) | August 2026 | Categories: AWS, Compute

Amazon Elastic Compute Cloud (EC2) provides virtual servers in the cloud, allowing you to run applications, host services, and process data without managing physical hardware.

---

## On this page
* What is Amazon EC2?
* Key Concepts (AMIs, Instance Types, Security Groups)
* Step-by-Step Console Walkthrough
* Connecting via SSH
* Common Pitfalls
* Additional AWS Compute Concepts
* References

---

## What is Amazon EC2?

Amazon EC2 is a scalable virtual server hosting service provided by AWS. You can leverage the EC2 service to create virtual machines (VMs) in the AWS cloud with a custom set of hardware configurations, including CPU, Memory, Storage, and Networking. 

These virtual computing environments are called **instances**. AWS provides the option to launch resources on dedicated bare-metal servers or within a virtualized environment managed via a hypervisor, depending on your business, performance, and compliance requirements.

---

## Key Concepts

- **AMI (Amazon Machine Image):** A pre-configured template containing the Operating System (Linux, Windows, Ubuntu) and initial software required to launch your server. AMIs are Region-specific; if an AMI is not available in your target Region, you can copy it over before launching instances.
- **Instance Type:** The hardware specification of your server (CPU, Memory, Storage type, and Network performance). For example, `t2.micro` offers 1 vCPU and 1 GB of RAM.
- **Key Pair:** A security credential pair consisting of a public key stored by AWS and a private key (`.pem` file) downloaded to your local machine, used to securely authenticate SSH connections.
- **Security Group:** A stateful virtual firewall that controls inbound and outbound network traffic to your EC2 instance.
- **Root Device Storage:** The primary volume containing the boot image used to initialize the instance. AMIs are backed either by Amazon Elastic Block Store (EBS) or by an Instance Store (ephemeral storage).

---

## Step-by-Step Console Walkthrough

### 1. Launching the Instance
1. Log in to your **AWS Management Console** and search for **EC2**.
2. Click the **Launch instance** button.
3. Enter a **Name tag** for your server (e.g., `web-server-01`).

### 2. Select Operating System & Instance Type
1. Under **Application and OS Images (Amazon Machine Image)**, choose **Amazon Linux** (Free Tier eligible).
2. Under **Instance type**, select **t2.micro** (or **t3.micro** depending on region availability).

### 3. Create a Key Pair
1. Under **Key pair (login)**, click **Create new key pair**.
2. Enter a name (e.g., `ec2-key-pair`), select **RSA** as the key pair type and **.pem** as the private key file format.
3. Click **Create key pair**.
> **Important:** Save the downloaded `.pem` file in a secure directory on your local machine.

### 4. Network & Security Settings
1. Under **Network settings**, click **Edit**.
2. The **VPC** will be automatically set to the default **VPC**.
3. Make sure the **Auto-assign public IP** is **Enabled**.
4. Under **Firewall (security groups)**, select **Create security group**.
5. Configure the inbound security group rule:
   - **Type:** `SSH`
   - **Port:** `22`
   - **Source type:** `My IP` (*Never set this to `0.0.0.0/0` in production*).

---

## Connecting via SSH

Once your instance state transitions to **Running**, open your terminal (macOS/Linux/WSL) or Git Bash and run the following commands:

```bash
# 1. Restrict private key permissions (required for SSH client compliance)
chmod 400 ec2-key-pair.pem

# 2. Connect to your instance using its assigned Public IP address
ssh -i "ec2-key-pair.pem" ec2-user@YOUR_INSTANCE_PUBLIC_IP

```

---

## Common Pitfalls

1. **Leaving SSH Open to 0.0.0.0/0:** Exposing port 22 to the public internet allows automated bots to attempt brute-force login attempts. Always restrict SSH access to your specific IP address.
2. **Losing Your `.pem` Key File:** AWS only allows you to download your private key pair once during creation. Losing this file results in losing administrative SSH access to the instance.
3. **Forgetting to Terminate Test Instances:** Leaving unused instances running continuously will consume your monthly Free Tier compute hours. Always stop or terminate practice instances when finished.

---

## Additional AWS Compute Concepts

- **AWS Auto Scaling:** An AWS service that monitors your applications and automatically adjusts compute capacity (adding or removing EC2 instances) based on defined policies and demand metrics.
- **AWS Lambda:** A fully managed, serverless compute service that lets you run code without provisioning or managing servers. You only supply your code (Lambda functions) and pay for execution time.
- **AWS Containerization Services:** Managed container orchestration services for running Docker containers at scale:
   - **Amazon Elastic Container Service (ECS):** A fully managed AWS-native container orchestration service.
   - **Amazon Elastic Kubernetes Service (EKS):** A managed service for running open-source Kubernetes on AWS.

---

## References

- [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types)
- [AWS Documentation: Storage for the Root Device](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device)
- [AWS Documentation: Copying an AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html)
- [AWS Auto Scaling Documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [Amazon ECS Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)