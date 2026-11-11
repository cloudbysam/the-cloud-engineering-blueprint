# 1. Define the cloud provider
provider "aws" {
  region = "us-east-1"
}

# 2. Set up the variable that GitHub will pass in
variable "env" {
  type        = string
  description = "The deployment environment (staging or production)"
}

# 3. Tell AWS to deploy an EC2 Instance
resource "aws_instance" "my_server" {
  ami           = "ami-0c7217cdde317cfec" # A standard Ubuntu 22.04 LTS AMI in us-east-1
  
  # Condition: If env is production, make it a t3.micro. Otherwise, keep it on t2.micro!
  instance_type = var.env == "production" ? "t3.micro" : "t2.micro"

  tags = {
    Name        = "EC2-${var.env}-Server-Auto"
    Environment = var.env
  }
}
