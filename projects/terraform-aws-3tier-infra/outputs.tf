# 1. Application Load Balancer Output
# Access your web app in the browser using this URL
output "alb_dns_name" {
  description = "The public DNS URL of the Application Load Balancer"
  value       = "http://${aws_lb.tier3-app.dns_name}"
}


# 2. Bastion Host Output
# Public IP to SSH into from your local machine
output "bastion_public_ip" {
  description = "Public IP address of the Bastion Host"
  value       = aws_instance.bastion.public_ip
}


# 3. Application EC2 Server Output
# Private IP to SSH into from the Bastion Host
output "app_server_private_ip" {
  description = "Private IP address of the Application Server"
  value       = aws_instance.app_server.private_ip
}


# 4. RDS Database Endpoint Output
# Address used by the App Server to connect to PostgreSQL
output "rds_endpoint" {
  description = "Connection endpoint for the PostgreSQL RDS instance"
  value       = aws_db_instance.postgres.endpoint
}