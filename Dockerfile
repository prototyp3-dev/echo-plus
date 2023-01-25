# dapp dependencies stage
FROM ubuntu as dapp-build

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=Etc/UTC

RUN apt update && apt install -y python3 python3-opencv python3-shapely python3-requests python3-base58 python3-protobuf python3-pycryptodome python3-pip

RUN pip3 install eth_abi 

RUN apt remove -y python3-pip

# dapp files stage
FROM cartesi/toolchain:0.12.0 as dapp-files-build

WORKDIR /opt/cartesi/dapp

COPY dapp .
