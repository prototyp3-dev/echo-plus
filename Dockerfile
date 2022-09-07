# syntax=docker.io/docker/dockerfile:1.4
# FROM cartesi/toolchain:0.10.0 as dapp-build
FROM toolchain-python as dapp-build

WORKDIR /opt/cartesi/dapp
COPY . .

RUN <<EOF 
pip3 install crossenv 
python3 -m crossenv $(which python3) .env 
. ./.env/bin/activate 
pip install -r requirements.txt 
EOF


# target "dapp" {
#   contexts = {
#     toolchain-python = "target:toolchain-python"
#   }
# }
