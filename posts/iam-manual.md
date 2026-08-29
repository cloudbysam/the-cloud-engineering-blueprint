# AWS Security Essentials: Managing Access Manually with AWS IAM

By Samuel (cloudbysam) | August 2026 | Categories: AWS, Security

AWS Identity and Access Management (IAM) is the central security service that controls **who** can access your cloud resources and **what** actions they are allowed to perform.

---

## On this page
* What is AWS IAM?
* Key Concepts (Users, Groups, Roles, Policies)
* Step-by-Step Console Walkthrough
* The Principle of Least Privilege
* Common Pitfalls

---

## What is AWS IAM?
AWS IAM is a free service that provides fine-grained access control across your entire AWS account. Without IAM, anyone with your account login could modify, delete, or expose your infrastructure. 

IAM enables access control and enforces security measures in terms of authentication and authorization for different AWS resources or your overall AWS account.

---

## Key Concepts

* **Root User:** The primary account owner identity created when you sign up for AWS. Has unlimited access to all resources and billing. *Never use the root user for daily tasks.*
* **IAM Users:** Individual identities created inside your account for real people (e.g., developers or admins).
* **IAM Groups:** A collection of users. Applying a policy to a group gives all users in that group the same permissions.
* **IAM Roles:** An identity with specific permissions that can be assumed by a person or an AWS service (such as allowing an EC2 instance to read files from an S3 bucket safely).
* **IAM Policies:** JSON documents that explicitly state what actions are `Allowed` or `Denied` on specific resources.

---

## The Principle of Least Privilege

> **Rule #1 of Cloud Security:** Always grant **only** the minimum permissions necessary to perform a task, and nothing more.

Never attach broad administrator access policies (`AdministratorAccess`) to application roles or user accounts unless strictly necessary.

---

## Step-by-Step Console Walkthrough

### 1. Secure Your Root Account
* Log in to the AWS Management Console as the Root User.
* Search for **IAM** in the top search bar.
* Enable **Multi-Factor Authentication (MFA)** immediately on your Root account using an authenticator app (like Google Authenticator or Authy).

### 2. Create an Admin IAM User (For Daily Use)
* Search for IAM in the search bar, click **Users > Add user**.
* Enter a username (e.g., `sam-admin`).
* Check **Provide user access to the AWS Management Console**.
* Assign permissions by adding the user to an Admin group with `AdministratorAccess`.
* Save the credentials and log out of your Root account. *Use this new user for all daily work* and creating of other IAM users. 

### 3. Create an IAM Role for an EC2 Instance
* Search for IAM in the search bar and in the sidebar, click **Roles > Create role**.
* Select **AWS service** as the trusted entity type, and choose **EC2**.
* Search for the policy `AmazonS3ReadOnlyAccess` and check the box.
* Name the role `EC2-S3-ReadOnly-Role` and click **Create role**.
* *Result:* You can now attach this role to an EC2 instance so your server can access S3 buckets without needing hardcoded credentials!

---

## Common Pitfalls

1. **Using the Root Account for Daily Work:** If your root credentials are leaked, an attacker has complete control of your account, billing, and resources. Lock it down with MFA and use IAM users instead.
2. **Hardcoding AWS Access Keys in Code:** Never paste secret keys directly inside Python scripts, Dockerfiles, or Git repositories. Use IAM Roles instead.
3. **Overly Permissive Policies:** Granting wildcard permissions (`"Action": "*"`) makes your system vulnerable to security breaches. Always restrict actions to specific services and resources.