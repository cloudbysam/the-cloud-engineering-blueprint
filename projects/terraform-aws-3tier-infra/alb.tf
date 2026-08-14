# create alb
resource "aws_lb" "tier3-app" {
  name               = "3tier-app-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public-1.id, aws_subnet.public-2.id]

  tags = {
    Environment = "production"
  }
}

# create target group
resource "aws_lb_target_group" "tg" {
  name        = "3tier-app-lb-tg"
  target_type = "instance"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# create target group listener
resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.tier3-app.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}
