# uncomment to use
# terraform {
#   backend "s3" {
#     bucket         = "sandtech-terraform-state"
#     key            = "network/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     use_lockfile   = true  #S3 native locking
#   }
# }

#local stack

terraform {
  backend "s3" {
    bucket         = "mock-bucket"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    endpoints = {
      s3 = "http://localhost:4566"
    }
    access_key     = "mock_access_key"
    secret_key     = "mock_secret_key"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
  }
}