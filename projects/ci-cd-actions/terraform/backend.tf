terraform {
  backend "s3" {
    bucket         = "my-unique-ci-cd-devops-bucket" 
    region         = "us-east-1"
    # We leave the "key" out of this file!
    # Our GitHub Action passes the key dynamically via -backend-config="key=..."
  }
}
