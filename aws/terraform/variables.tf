variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ecr_name" {
  description = "Name for the ECR repository"
  type        = string
  default     = "booking-platform"
}

variable "image_tag" {
  description = "Image tag to deploy"
  type        = string
  default     = "latest"
}
