# CI/CD Learning Playground: GitHub Actions & Terraform

This project demonstrates an automated CI/CD pipeline using GitHub Actions to test Python code, build and push Docker containers to GitHub Container Registry (`ghcr.io`), and provision multi-environment AWS infrastructure (`staging` and `production`) with Terraform and OIDC authentication.

## Pipeline Architecture

The workflow (`.github/workflows/hello-world.yml`) is split into distinct stages to enforce testing and manual review before production changes go live:

1. **Test & Container Build (`python-test-job` & `build-docker-job`):** Validates the Python application and publishes the container image to `ghcr.io`.
2. **Automated Staging (`terraform-staging`):** Authenticates to AWS via OIDC (no static access keys) and automatically deploys changes to the staging state (`staging/terraform.tfstate`).
3. **Production Plan (`plan-production`):** Runs `terraform plan -out=prod.tfplan` without pausing, printing the exact infrastructure diff to the workflow logs and saving the execution plan as a short-lived artifact.
4. **Protected Production Apply (`apply-production`):** Gated behind GitHub's `environment: production` protection rule. Reviewers can inspect the `plan-production` logs *before* approving, and once approved, Terraform executes `terraform apply prod.tfplan`—guaranteeing that only the exact reviewed plan is applied.

## Known Limitations & Security Trade-offs

* **Terraform Plan Artifacts on Public Repositories:**
  To pass the frozen `prod.tfplan` file between `plan-production` and `apply-production`, the workflow uses `actions/upload-artifact` with `retention-days: 1`.
  * **Why this is a caveat:** Terraform `.tfplan` files contain full resource attributes and state snapshots, which can include plaintext secrets (such as database passwords or API keys). On a **public** GitHub repository, any logged-in GitHub user can download workflow artifacts while they are retained.
  * **Mitigation:** In this learning repository, the provisioned resources contain no sensitive secrets, and artifact retention is minimized to 1 day. In a real-world production setup with sensitive state data, this workflow should run inside a **private repository** or store plan files in an encrypted, access-controlled **S3 bucket** instead of GitHub Actions artifacts.
