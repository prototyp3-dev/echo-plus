# syntax=docker.io/docker/dockerfile:1.4
# FROM cartesi/toolchain:0.11.0 as dapp-build
# FROM toolchain-python as dapp-build
FROM toolchain-python as dapp-build

WORKDIR /opt/cartesi/dapp

SHELL ["/bin/bash", "-c"]

RUN apt update && apt install -y cmake

COPY . .

RUN source compiler-envs.sh && cd 3rdparty && make geos

RUN <<EOF 
pip3.10 install crossenv 
python3.10 -m crossenv /mnt/python-dapp/bin/python3 .env 
. ./.env/bin/activate 
pip install -r requirements.txt 
EOF
