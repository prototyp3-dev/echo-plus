#!/bin/bash

export TARGET=riscv64-cartesi-linux-gnu
export TARGET_DIR=/opt/riscv/rootfs/buildroot/work/staging/usr
export ROOT_DIR=${PWD}/3rdparty
export PYTHON_DIR=/opt/build-python/

export CC="${TARGET}-gcc"
export CXX="${TARGET}-g++"
export CXXFLAGS="-I${TARGET_DIR}/include -I${PYTHON_DIR}/include"
export CFLAGS="-I${TARGET_DIR}/include -I${PYTHON_DIR}/include"
export LDFLAGS="-L${TARGET_DIR}/lib -L${PYTHON_DIR}/lib -L${ROOT_DIR}/.env/cross/lib"
export LDSHARED="${TARGET}-gcc"
export LD="${TARGET}-gcc"
