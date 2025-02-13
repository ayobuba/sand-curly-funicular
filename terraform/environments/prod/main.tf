module "compute" {
  source = "../../modules/compute"

  # We either pass the known shared subnet IDs,
  # or we use a data source to find them by tag.
  subnet_id = var.shared_subnet_id

  # Additional inputs, e.g. instance type, etc.
  instance_type = "t3.micro"
  environment   = "dev"
}
