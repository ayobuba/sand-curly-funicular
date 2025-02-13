variable "environments" {
  type = map(string)
  # Example: { dev = "arn:aws:organizations::123456789012:account/o-myorg/111111111111", ... }
  description = "Map of environment name to the principal (account ARN) for AWS RAM"
}

variable "subnet_arns" {
  type        = map(string)
  description = "Map of environment name to the subnet ARN in the VPC"
}
