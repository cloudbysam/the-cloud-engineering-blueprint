# 1. Application Load Balancer Security Group
# Allows public inbound HTTP traffic from anywhere on the internet (Port 80)
resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "alb_sg"
  }
}


resource "aws_vpc_security_group_ingress_rule" "allow_http_ipv4" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

resource "aws_vpc_security_group_egress_rule" "alb_all_out" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # -1 means all traffic
}


# 2. Bastion Host Security Group & Rules
# Allows inbound SSH management traffic from a trusted IP / Bastion (Port 22)
resource "aws_security_group" "bastion_sg" {
  name        = "bastion_sg"
  description = "Security group for Bastion Host"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "bastion_sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "bastion_ssh_in" {
  security_group_id = aws_security_group.bastion_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_egress_rule" "bastion_all_out" {
  security_group_id = aws_security_group.bastion_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}


# 3. EC2 Application Layer Security Group
# Allows inbound HTTP traffic ONLY from the ALB Security Group (Port 80)
resource "aws_security_group" "ec2_sg" {
  name        = "ec2-app-sg"
  description = "Security group for Application EC2 instances"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "ec2-app-sg"
  }
}

# Ingress: HTTP from ALB
resource "aws_vpc_security_group_ingress_rule" "allow_alb_ipv4" {
  security_group_id            = aws_security_group.ec2_sg.id
  referenced_security_group_id = aws_security_group.alb_sg.id
  from_port                    = 80
  ip_protocol                  = "tcp"
  to_port                      = 80
}

# Ingress: SSH from Bastion
resource "aws_vpc_security_group_ingress_rule" "ec2_ssh_from_bastion" {
  security_group_id            = aws_security_group.ec2_sg.id
  referenced_security_group_id = aws_security_group.bastion_sg.id
  from_port                    = 22
  to_port                      = 22
  ip_protocol                  = "tcp"
}

#Egress
resource "aws_vpc_security_group_egress_rule" "ec2_all_out" {
  security_group_id = aws_security_group.ec2_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}


# 4. RDS Database Layer Security Group
# Allows inbound PostgreSQL traffic ONLY from the EC2 Security Group (Port 5432)
resource "aws_security_group" "rds_sg" {
  name        = "rds-db-sg"
  description = "Security group for PostgreSQL RDS instance"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "rds-db-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "rds_pg_from_ec2" {
  security_group_id            = aws_security_group.rds_sg.id
  referenced_security_group_id = aws_security_group.ec2_sg.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}
