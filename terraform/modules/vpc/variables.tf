variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
}

variable "vpc_name" {
  type        = string
  description = "Tag name for the VPC"
}

variable "az" {
  type        = string
  description = "Availability zone to place subnets"
}

variable "subnets" {
  type = map(string)
  description = "Map of environment->subnet CIDRs"
}
