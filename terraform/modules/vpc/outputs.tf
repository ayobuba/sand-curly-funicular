output "vpc_id" {
  value = aws_vpc.this.id
}

output "subnet_ids" {
  value = {
    for k, s in aws_subnet.subnets : k => s.id
  }
}

output "subnet_arns" {
  value = {
    for k, s in aws_subnet.subnets : k => s.arn
  }
}
