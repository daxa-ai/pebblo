variable "PEBBLO_VERSION" {
  default = "main"
}

variable "GITHUB_REF" {
  default = ""
}

variable "IMAGE_NAME" {
  default = "daxaai/pebblo"
}

variable "IMAGE_TAG_SUFFIX" {
  default = "local"
}

variable "BASE_IMAGE_TAG_SUFFIX" {
  default = "local"
}

variable "PEBBLO_EXTRAS" {
  default = ""
}

target "base" {
  dockerfile = "Dockerfile.base"
  tags = ["${IMAGE_NAME}:${IMAGE_TAG_SUFFIX}", "${IMAGE_NAME}:latest"]
  args = {
    build_image = "python:3.11"
    base_image = "python:3.11"
    pebblo_version = "${PEBBLO_VERSION}"
  }
  platforms = ["linux/amd64", "linux/arm64"]
}
