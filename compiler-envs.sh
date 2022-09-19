#!/bin/bash

export TARGET=riscv64-cartesi-linux-gnu
# export TARGET_DIR=/opt/riscv/riscv64-cartesi-linux-gnu/riscv64-cartesi-linux-gnu
export TARGET_DIR=/opt/riscv/rootfs/buildroot/work/staging/usr
export ROOT_DIR=${PWD} #/opt/cartesi/dapp
export PYTHON_DIR=/opt/build-python/

export CC="${TARGET}-gcc"
export CXX="${TARGET}-g++"
export CXXFLAGS="-I${TARGET_DIR}/include -I${PYTHON_DIR}/include"
export CFLAGS="-I${TARGET_DIR}/include -I${PYTHON_DIR}/include"
export LDFLAGS="-L${TARGET_DIR}/lib -L${PYTHON_DIR}/lib -L${ROOT_DIR}/.env/cross/lib" # -L${TARGET_DIR}/sysroot/lib -L${TARGET_DIR}/sysroot/lib64/ld64 -L${TARGET_DIR}/sysroot/usr/lib -L${TARGET_DIR}/sysroot/usr/lib64/ld64"
export LDSHARED="${TARGET}-gcc"
export LD="${TARGET}-gcc"


# unset TARGET
# unset TARGET_DIR
# unset ROOT_DIR
# unset CC
# unset CXX
# unset CFLAGS
# unset CXXFLAGS
# unset LDFLAGS
# unset LDSHARED
# unset LD