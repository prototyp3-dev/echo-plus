
group "default" {
  targets = ["dapp","server", "console"]
}

# crossenv toolchain for python dapps
target "toolchain-python" {
  context = "./docker"
  target  = "toolchain-python"
  tags    = ["cartesi/toolchain-python"]
}

target "dapp" {
  context = "./docker"
  target  = "dapp-fs-build"
  contexts = {
    dapp-build = "target:dapp-dependencies"
    dapp-files-build = "target:dapp-files"
  }
}

target "fsext" {
  context = "./docker"
  target  = "dapp-fsext-build"
  contexts = {
    dapp-build = "target:dapp-dependencies"
    dapp-files-build = "target:dapp-files"
  }
}

target "server" {
  context = "./docker"
  target  = "machine-server"
  contexts = {
    dapp-build = "target:dapp-dependencies"
    dapp-files-build = "target:dapp-files"
  }
}

target "console" {
  context = "./docker"
  target  = "machine-console"
  contexts = {
    dapp-build = "target:dapp-dependencies"
    dapp-files-build = "target:dapp-files"
  }
}

target "machine" {
  context = "./docker"
  target  = "machine-standalone"
  contexts = {
    dapp-build = "target:dapp"
    dapp-files-build = "target:dapp-files"
  }
}
