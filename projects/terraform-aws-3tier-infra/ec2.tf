# Fetch latest Amazon Linux 2023 AMI
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# Create Bastion Host (Public Subnet)
resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.amazon_linux_2023.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public-1.id
  vpc_security_group_ids      = [aws_security_group.bastion_sg.id]
  associate_public_ip_address = true
#   key_name                    = uncomment and add key name if using key pair
  tags = {
    Name        = "3tier-bastion-host"
    Environment = "production"
  }
}

# App Server (Private Subnet)
resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private-1.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  # Install PostgreSQL client tools and Web server on startup
  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              dnf install -y postgresql15 nginx
              systemctl enable nginx
              systemctl start nginx
              echo "<h1>3-Tier App Server Online</h1>" > /usr/share/nginx/html/index.html
              EOF

  tags = {
    Name        = "3tier-app-server"
    Environment = "production"
  }
}

# Attach App Server to Target Group
resource "aws_lb_target_group_attachment" "app_attachment" {
  target_group_arn = aws_lb_target_group.tg.arn
  target_id        = aws_instance.app_server.id
  port             = 80
}