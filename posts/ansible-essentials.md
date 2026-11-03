# Configuration Management: Automating Server Setup with Ansible

By Samuel (cloudbysam) | September 2026 | Categories: Ansible, DevOps, IaC

Once your infrastructure is provisioned using a tool like Terraform, you need a way to configure the operating systems, install packages, and manage application code inside those servers. This is where **Ansible** comes in—an agentless configuration management tool that allows you to automate server setup across hundreds of machines simultaneously.

---

## On this page
* Provisioning vs. Configuration Management
* What is Ansible?
* Key Concepts (Control Node, Managed Nodes, Inventory, Playbooks)
* Prerequisites
* Step-by-Step Walkthrough: Installing & Running Ansible
* Writing Your First Playbook
* Common Pitfalls

---

## Provisioning vs. Configuration Management

It is important to understand the division of labor in modern DevOps tools:

* **Provisioning (Terraform):** Creates the underlying infrastructure (VPCs, Subnets, EC2 Instances, S3 Buckets).
* **Configuration Management (Ansible):** Configures what runs *inside* the servers (installing Nginx, updating system security patches, setting up environment variables).

---

## What is Ansible?

Ansible is an open-source automation engine created by Red Hat. Unlike tools that require special software (agents) installed on target servers, Ansible is **agentless**. It communicates directly over standard **SSH** (for Linux) or **WinRM** (for Windows) to execute commands.

---

## Key Concepts

* **Control Node:** The computer (your local machine or a management server) where Ansible is installed and executed from.
* **Managed Nodes:** The remote servers (such as your AWS EC2 instances) that Ansible connects to and configures.
* **Inventory File (`hosts`):** A plain text or YAML file listing the IP addresses or domain names of your target servers, grouped by role (e.g., `[webservers]`, `[dbservers]`).
* **Playbook (`playbook.yml`):** A YAML file containing a sequential list of **Tasks** (instructions) executed on your managed nodes.
* **Modules:** Pre-built Ansible functions used to perform specific actions (e.g., `apt`, `yum`, `copy`, `service`).

---

## Prerequisites

1. An active Linux machine or WSL (Windows Subsystem for Linux) acting as your Control Node.
2. One or more running AWS EC2 Linux instances with your SSH key pair downloaded locally.

---

## Step-by-Step Walkthrough

### 1. Install Ansible on the Control Node
```bash
# Update local packages and install Ansible
sudo apt update
sudo apt install -y ansible
```

### 2. Create an Inventory File (`hosts`)
Create a file named `hosts` in your project folder to define your target servers:
```bash
[webservers]
web1 ansible_host=YOUR_EC2_PUBLIC_IP ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/your-key.pem
```

### 3. Test Connection with Ad-Hoc Ping
Run an initial connection check across all webservers:
```bash
ansible webservers -i hosts -m ping
```
Expected Output: `"ping": "pong"` showing successful SSH authentication!

---
## Writing Your First Playbook (`setup-webserver.yml`)
Create a file named `setup-webserver.yml` to automatically update your Linux server and install the Nginx web server:
```YAML
---
- name: Configure Web Server Infrastructure
  hosts: webservers
  become: true # Run tasks with sudo root privileges

  tasks:
    - name: Update all system packages
      apt:
        name: '*'
        state: latest

    - name: Install Nginx web server
      apt:
        name: nginx
        state: present

    - name: Start and enable Nginx service
      service:
        name: nginx
        state: started
        enabled: true
```
---
## Run the Playbook
Execute your playbook against your inventory file:
```bash
ansible-playbook -i hosts setup-webserver.yml
```
---
## Common Pitfalls
- **Incorrect YAML Indentation:** YAML relies strictly on two-space indentation. Using tabs or mismatched spaces will cause syntax parsing errors.
- **Hardcoding Private SSH Keys:** Never commit your SSH `.pem` private keys or sensitive variables into Git repositories. Use **Ansible Vault** to encrypt sensitive data files.
- **Forgetting `become: true:`** Installing software packages or restarting services requires root permissions. If your task fails with permission errors, ensure `become: true` is set.