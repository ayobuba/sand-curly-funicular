resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = var.vpc_name
  }
}

# Example: one private subnet per environment or multiple.
# For simplicity, we'll create three subnets for dev, staging, prod.
resource "aws_subnet" "subnets" {
  for_each                = var.subnets
  vpc_id                  = aws_vpc.this.id
  cidr_block              = each.value
  availability_zone       = var.az
  map_public_ip_on_launch = false

  tags = {
    Name        = "${each.key}-subnet"
    Environment = each.key
  }
}
