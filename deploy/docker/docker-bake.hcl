variable "PEBBLO_VERSION" {
  default = "dev"
}

variable "PEBBLO_BRANCH" {
  default = "main"
}

variable "IMAGE_NAME" {
  default = "daxaai/pebblo"
}

target "base" {
  dockerfile = "Dockerfile.base"
  tags = ["${IMAGE_NAME}:${PEBBLO_VERSION}", "${IMAGE_NAME}:latest"]
  args = {
    build_image = "python:3.11"
    base_image = "python:3.11"
    pebblo_branch = "${PEBBLO_BRANCH}"
  }
  platforms = ["linux/amd64"]
}
