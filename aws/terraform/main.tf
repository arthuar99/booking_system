terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.4.0"
}

provider "aws" {
  region = var.region
}

module "ecr" {
  source = "./modules/ecr"
  name   = var.ecr_name
}

module "apprunner" {
  source         = "./modules/apprunner"
  ecr_repository = module.ecr.repository_url
  image_tag      = var.image_tag
}
