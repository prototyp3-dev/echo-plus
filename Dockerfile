# syntax=docker.io/docker/dockerfile:1.4
# FROM cartesi/toolchain:0.11.0 as dapp-build
# FROM toolchain-python as dapp-build
FROM cartesi/toolchain-python as dapp-build

WORKDIR /opt/cartesi/dapp

SHELL ["/bin/bash", "-c"]

RUN apt update && apt install -y cmake

COPY . .

RUN source compiler-envs.sh && cd 3rdparty && make geos

RUN <<EOF 
pip3.10 install crossenv 
python3.10 -m crossenv $(which python3) .env 
. ./.env/bin/activate 
pip install -r requirements.txt 
EOF

RUN <<EOF 
. ./.env/bin/activate 
source compiler-envs.sh
CXXFLAGS="${CXXFLAGS} -I${ROOT_DIR}/3rdparty/glibc/include -I${ROOT_DIR}/3rdparty/geos/include" \
CFLAGS="${CFLAGS} -I${ROOT_DIR}/3rdparty/glibc/include -I${ROOT_DIR}/3rdparty/geos/include" \
LDFLAGS="${LDFLAGS} -L${ROOT_DIR}/3rdparty/glibc/lib -L${ROOT_DIR}/3rdparty/geos/lib" \
GEOS_CONFIG="3rdparty/geos-dist/bin/geos-config" && \
pip3.10 install shapely==1.5.9 -vvv --no-binary shapely
EOF
