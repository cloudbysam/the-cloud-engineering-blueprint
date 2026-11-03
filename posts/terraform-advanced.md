# Advanced Infrastructure as Code: Terraform Modules & Variables

By Samuel (cloudbysam) | September 2026 | Categories: Terraform, IaC, DevOps

Writing a single `main.tf` file works great for quick experiments, but as your cloud architecture grows into multi-tier applications, repeating code becomes messy and hard to maintain. In this guide, we explore **Terraform Modules and Input Variables** to write clean, reusable, and enterprise-grade infrastructure code.

---

## On this page
- Why Use Terraform Modules?
- Terraform State
- Input Variables & Output Values
- Structuring a Modular Terraform Project
- Building a Reusable EC2 Module
- Common Pitfalls

---

## Why Use Terraform Modules?
A **Terraform Module** is simply a container for multiple resources that are used together. Think of it like a Python function: you write the logic once, parameterize it with variables, and call it multiple times with different inputs for different environments (Development, Staging, Production).

---

## Terraform State
Every time you run Terraform, it records information about what infrastructure it created in a Terraform state file. By default, when you run Terraform in the folder `/foo/bar`, Terraform creates the file `/foo/bar/terraform.tfstate`. This file contains a custom JSON format that records a mapping from the Terraform resource in your configuration files to the representation of those resources in the real world. In other words, the output of the `plan` command is a diff between the code on your computer and the infrastructure deployed in the real world, as discovered via IDs in the state file.   

If you're using Terraform for a personal project, storing state in a single `terraform.tfstate` file that lives locally on your computer works just fine. But if you want to use Terraform as a team on a real project, you run into several challenges:
- Shared storage for state files
- Locking state files to prevent race conditions
- Isolating state files between environments

The best way to manage shared storage for state files is to use Terraform's built-in support for remote backends. A Terraform backend determines how Terraform loads and stores state. The default backend is the local backend, which stores the state file on your local disk. Remote backends allow you to store the state file in a remote, shared store.

For example, to enable remote state storage with Amazon S3, the first step is to create an S3 bucket. After creating the S3 bucket, add extra layers of protection, such as versioning, server-side encryption configuration, and public access blocks. Once the backend infrastructure is deployed, you need to add a backend configuration block to your Terraform code:

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state-bucket"
    key    = "dev/terraform.tfstate"
    region = "us-east-1"
  }
}
```
Note: The `key` attribute is very important—it defines the file path within the S3 bucket where the state file will be stored.

After configuring the backend, you will run the `terraform init` command again to instruct Terraform to migrate and store your state file in the S3 bucket.

## Input Variables & Output Values
- **Variables (`variables.tf`):** Allow you to parameterize your configurations so you don't hardcode values like instance types or region names.
- **Outputs (`outputs.tf`):** Allow you to expose key information (like a server's public IP or a database endpoint) after the infrastructure is deployed.

## Structuring a Modular Terraform Project
A professional, scalable Terraform repository layout looks like this:
```text
terraform-aws-project/
├── modules/
│   └── ec2_instance/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       └── terraform.tfvars
```

## Building a Reusable EC2 Module

- **Module Configuration Files**

`modules/ec2_instance/variables.tf`
```hcl
 variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "server_name" {
  type = string
}
```
`modules/ec2_instance/main.tf`
```hcl
resource "aws_instance" "this" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.instance_type

  tags = {
    Name = var.server_name
  }
}
```
`modules/ec2_instance/outputs.tf`
```hcl
output "instance_ip" {
  value = aws_instance.this.public_ip
}
```
- **Calling the Module in Development** (`environments/dev/main.tf`)
```hcl
provider "aws" {
  region = "us-east-1"
}

module "web_server" {
  source        = "../../modules/ec2_instance"
  instance_type = "t2.micro"
  server_name   = "dev-web-server"
}

output "dev_server_ip" {
  value = module.web_server.instance_ip
}
```
## Common Pitfalls
- **Deeply Nested Module Hierarchies:** Avoid chaining modules 4 or 5 levels deep (a module calling a module calling a module). Keep your module structure flat (1 level deep) for readability and easy debugging.
- **Hardcoding Environment Values:** Never hardcode environment-specific parameters inside module resource blocks. Always pass them down via `variables.tf` and `.tfvars` files.