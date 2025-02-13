terraform {
  backend "s3" {
    bucket         = "sandtech-terraform-state"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    use_lockfile   = true  #S3 native locking
  }
}