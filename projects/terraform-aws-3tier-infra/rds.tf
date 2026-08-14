resource "aws_db_instance" "postgres" {
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  identifier             = "demo-postgres"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  username               = var.username
  password               = var.password
  skip_final_snapshot    = true
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "3tier-rds-subnet-group"
  subnet_ids = [aws_subnet.private-3.id, aws_subnet.private-4.id]

  tags = {
    Name = "3tier-rds-subnet-group"
  }
}
