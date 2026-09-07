# Infrastructure as Code: Provisioning AWS Services with Terraform

By Samuel (cloudbysam) | September 2026 | Categories: Terraform, IaC

**Terraform** is a provisioning tool responsible for creating servers. In fact, you can use provisioning tools to create not only servers but also databases, caches, load balancers, queues, subnet configurations, routing rules, and almost every other aspect of your infrastructure.

---

## On this page
* What is Terraform?
* Key Concepts (Providers, Resources, State File)
* Prerequisites
* Terraform Commands (`init`, `plan`, `apply`, `destroy`)
* Common Pitfalls
* Recommended .gitignore
* Project
* Resources

---

## What is Terraform?
Terraform is an open-source Infrastructure as Code (IaC) tool created by HashiCorp. It uses **HashiCorp Configuration Language (HCL)** to define cloud infrastructure in human-readable code files. Instead of manually creating resources, Terraform reads your code files, determines what needs to be created or updated, and interacts with the AWS API on your behalf.

---

## Key Concepts

* **Provider:** A plugin that tells Terraform how to talk to a specific cloud service (e.g., AWS, Azure, Google Cloud).
* **Resource:** The fundamental building block in HCL that declares a specific piece of infrastructure (e.g., an EC2 instance, an S3 bucket, or a VPC).
* **State File (`terraform.tfstate`):** A JSON file where Terraform keeps track of the real-world resources it created and maps them to your code configuration.

---

## Prerequisites

1. Install the **Terraform CLI** on your computer.
2. Install the **AWS CLI** and configure your credentials locally using `aws configure` (or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your environment variables).

---

## Terraform Commands

* **`terraform init`:** Initializes your working directory and downloads necessary provider plugins.
* **`terraform fmt`:** Automatically formats HCL code files to adhere to standard canonical styling conventions.
* **`terraform validate`:** Checks whether configuration files are syntactically valid and internally consistent.
* **`terraform plan`:** Reads configuration and generates an execution plan showing pending changes without provisioning resources.
* **`terraform apply`:** Executes proposed plan actions to create, update, or replace cloud infrastructure live.
* **`terraform destroy`:** Cleans up and destroys all resources managed by the configuration.
* **`terraform output`:** Extracts and displays public values defined in `outputs.tf` (e.g., DNS names, IP addresses).
* **`terraform state list`:** Lists all managed infrastructure resources tracked within the current state file.

---

## Common Pitfalls

* **Committing `terraform.tfstate` or `.tfvars` to GitHub:** The Terraform state file can contain sensitive outputs and configuration details. Always add `*.tfstate`, `*.tfstate.backup`, and `.terraform/` to your `.gitignore` file.
* **Editing Resources Manually in the AWS Console:** If you create a server with Terraform and then manually delete or change it in the AWS Console, you create drift. Always manage Terraform-provisioned infrastructure using Terraform commands.

---

## Recommended .gitignore

Prevent sensitive state data, local variables, and cached plugins from leaking into version control:

```gitignore
# Local terraform directory
.terraform/

# State files (contains sensitive plan data & raw credentials)
*.tfstate
*.tfstate.*

# Crash logs
crash.log
crash.*.log

# Variable definition files (if storing secrets)
*.tfvars
*.tfvars.json
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# CLI configuration files
.terraformrc
terraform.rc
```

---

## Project

Hey, here is a fun fact: I have built a three-tier project using Terraform ([AWS Three-Tier App Architecture](../projects/terraform-aws-3tier-infra/README.md)). The coolest part is that you can deploy the entire production infrastructure with just a single magic command—`terraform apply`—and spin down everything cleanly with `terraform destroy`.

---

## Resources

To deepen your understanding of Terraform, check out these video courses:

* [Complete Terraform Course - From BEGINNER to PRO!](https://youtu.be/7xngnjfIlK4) by **DevOps Directive**
* [Terraform Course - Automate your AWS Cloud Infrastructure](https://youtu.be/SLB_c_ayRMo)