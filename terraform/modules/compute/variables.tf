variable "ami_id" {
  type    = string
  default = "ami-1234567890abcdef0"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID to place this instance"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, staging, prod)"
  default     = "dev"
}

variable "name" {
  type        = string
  default     = "example-ec2"
}
