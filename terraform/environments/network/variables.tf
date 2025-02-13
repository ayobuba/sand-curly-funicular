variable "vpc_cidr" {
  type    = string
  default = "10.10.0.0/16"
}

variable "az" {
  type    = string
  default = "us-east-1a"
}

variable "dev_subnet_cidr" {
  type    = string
  default = "10.10.1.0/24"
}

variable "staging_subnet_cidr" {
  type    = string
  default = "10.10.2.0/24"
}

variable "prod_subnet_cidr" {
  type    = string
  default = "10.10.3.0/24"
}

# Provide environment -> principal mappings
# (account ARN or OU ARN if using entire OU)
# data "aws_organizations_organization" "org" {}
#
# data "aws_organizations_organizational_units" "ou" {
#   parent_id = data.aws_organizations_organization.org.roots[0].id
# }
#
# data "aws_organizations_account" "dev" {
#   for_each = toset([for ou in data.aws_organizations_organizational_units.ou.children : ou.id if ou.tags["Environment"] == "dev"])
#   id       = each.value
# }
#
# data "aws_organizations_account" "staging" {
#   for_each = toset([for ou in data.aws_organizations_organizational_units.ou.children : ou.id if ou.tags["Environment"] == "staging"])
#   id       = each.value
# }
#
# data "aws_organizations_account" "prod" {
#   for_each = toset([for ou in data.aws_organizations_organizational_units.ou.children : ou.id if ou.tags["Environment"] == "prod"])
#   id       = each.value
# }
#
# locals {
#   environments = {
#     dev     = data.aws_organizations_account.dev[0].arn
#     staging = data.aws_organizations_account.staging[0].arn
#     prod    = data.aws_organizations_account.prod[0].arn
#   }
# }

variable "environments" {
  type = map(string)
  default = {}
}