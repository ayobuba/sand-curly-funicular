variable "shared_subnet_id" {
  type        = string
  description = "Subnet ID shared via RAM from the network account"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}
