# create a vpc
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "3tier-app-vpc"
  }
}

# create the subnets (private & public)

resource "aws_subnet" "public-1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "public-1"
  }
}

resource "aws_subnet" "public-2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1b"

  tags = {
    Name = "public-2"
  }
}

resource "aws_subnet" "private-1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-1"
  }
}

resource "aws_subnet" "private-2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-2"
  }
}

resource "aws_subnet" "private-3" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.20.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-3"
  }
}

resource "aws_subnet" "private-4" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.21.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-4"
  }
}

# create internet gateway and attach to the vpc(IGW)
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "3tier-igw"
  }
}

# create a route table for the public and private subnet
resource "aws_route_table" "public-rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table" "private-rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "private-rt"
  }
}


# create route table association for public subnets
resource "aws_route_table_association" "public" {
  for_each = {
    "public-1" = aws_subnet.public-1.id
    "public-2" = aws_subnet.public-2.id
  }

  subnet_id      = each.value
  route_table_id = aws_route_table.public-rt.id
}

# create route table association for private subnets
resource "aws_route_table_association" "private_subnet_assoc" {
  for_each = {
    "private-1" = aws_subnet.private-1.id
    "private-2" = aws_subnet.private-2.id
    "private-3" = aws_subnet.private-3.id
    "private-4" = aws_subnet.private-4.id
  }

  subnet_id      = each.value
  route_table_id = aws_route_table.private-rt.id
}

# create EIP for the NAT gateway
resource "aws_eip" "nat_eip" {
  domain = "vpc"

  tags = {
    Name = "nat-gateway-eip"
  }
}

# create NAT gateway
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public-1.id

  tags = {
    Name = "nat-gateway"
  }

  # Ensures the IGW is fully provisioned before AWS tries to spin up the NAT Gateway
  depends_on = [aws_internet_gateway.gw]
}