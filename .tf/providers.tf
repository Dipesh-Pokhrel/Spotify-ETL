provider "aws" {
  region                   = var.region
  shared_credentials_files = ["C:/Users/terraform/.aws/credentials"]
  profile                  = "default"
}