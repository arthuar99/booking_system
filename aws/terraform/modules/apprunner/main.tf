resource "aws_apprunner_service" "this" {
  service_name = "booking-platform-apprunner"

  source_configuration {
    image_repository {
      image_repository_type = "ECR"
      image_identifier      = "${var.ecr_repository}:${var.image_tag}"
      image_configuration {
        port = "8000"
      }
    }
  }

  instance_configuration {
    cpu    = "1024"
    memory = "2048"
  }
}

output "apprunner_url" {
  value = aws_apprunner_service.this.service_url
}
