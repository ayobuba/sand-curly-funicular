module "shared-vpc" {
  source       = "../../modules/vpc"
  vpc_cidr     = var.vpc_cidr
  vpc_name     = "shared-vpc"
  az           = var.az

  # We define subnets for dev, staging, and prod
  subnets = {
    dev     = var.dev_subnet_cidr
    staging = var.staging_subnet_cidr
    prod    = var.prod_subnet_cidr
  }
}

module "resource-access-manager" {
  source        = "../../modules/ram"
  environments  = var.environments  # map of environment->account_arn
  subnet_arns   = module.shared-vpc.subnet_arns
}
