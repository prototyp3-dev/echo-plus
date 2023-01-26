
target "dapp-dependencies" {
  target  = "dapp-build"
}

target "dapp-files" {
  target  = "dapp-files-build"
}

variable "TAG" {
  default = "devel"
}

variable "DOCKER_ORGANIZATION" {
  default = "cartesi"
}

target "server" {
  tags = ["${DOCKER_ORGANIZATION}/dapp:echo-plus-${TAG}-server"]
}

target "console" {
  tags = ["${DOCKER_ORGANIZATION}/dapp:echo-plus-${TAG}-console"]
}

target "machine" {
  tags = ["${DOCKER_ORGANIZATION}/dapp:echo-plus-${TAG}-machine"]
}
