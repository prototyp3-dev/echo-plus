# syntax=docker.io/docker/dockerfile:1.4
# layers for caching and versioning
FROM cartesi/toolchain:0.12.0 as toolchain
FROM cartesi/rootfs:0.15.0 as rootfs
FROM cartesicorp/server-manager:0.5.0-rv64gc-test as server-manager

FROM rootfs as toolchain-python

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update \
    && apt install -y \
    libncurses-dev \
    libgdbm-dev \
    libz-dev \
    tk-dev \
    libsqlite3-dev \
    libreadline-dev \
    liblzma-dev \
    libffi-dev \
    libssl-dev

ENV PYTHON_VERSION=3.10
ENV PYTHON_VERSION_FULL=3.10.1
ENV BUILD_PYTHON_PREFIX=/opt/build-python
ENV HOST_PYTHON_PREFIX=/mnt/python-dapp

# Download Python source
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION_FULL/Python-$PYTHON_VERSION_FULL.tgz
RUN tar zxfv Python-$PYTHON_VERSION_FULL.tgz

# Build build-python from source
RUN cp -r Python-$PYTHON_VERSION_FULL build-python
WORKDIR /tmp/build-python
RUN ./configure --prefix=$BUILD_PYTHON_PREFIX
RUN make -j$(nproc)
RUN make install

ENV PATH=$BUILD_PYTHON_PREFIX/bin:$PATH

# Build host-python
WORKDIR /tmp
RUN cp -r Python-$PYTHON_VERSION_FULL host-python
WORKDIR /tmp/host-python
RUN CPPFLAGS="-I/opt/riscv/rootfs/buildroot/work/staging/usr/include" \
    LDFLAGS="-L/opt/riscv/rootfs/buildroot/work/staging/usr/lib" \
    ./configure \
    --enable-shared \
    --enable-optimizations \
    --prefix=$HOST_PYTHON_PREFIX \
    --host=riscv64-cartesi-linux-gnu \
    --build=x86_64-linux-gnu \
    --without-ensurepip \
    --disable-test-modules \
    ac_cv_buggy_getaddrinfo=no \
    ac_cv_file__dev_ptmx=yes \
    ac_cv_file__dev_ptc=no
WORKDIR /tmp/host-python
RUN make -j$(nproc)
RUN make install

WORKDIR /tmp
RUN pip3 install crossenv
RUN rm -rf Python-$PYTHON_VERSION_FULL*

# download standard machine drives
FROM busybox as machine-core

WORKDIR /opt/cartesi/share

# download dependencies
COPY dependencies .
COPY shasumfile .
RUN cat dependencies | xargs wget
RUN sha1sum -c shasumfile


# stage to add project files
FROM dapp-files-build as dapp-project-files-build

# install jq
RUN <<EOF
apt-get update
DEBIAN_FRONTEND="noninteractive" apt-get install -y jq
rm -rf /var/lib/apt/lists/*
EOF

COPY copy-dapp-files.sh /usr/local/bin
COPY default.json /opt/cartesi/

RUN copy-dapp-files.sh /opt/cartesi/default.json dapp.json /opt/dapp/


# stage to add dapp files and cartesi boot sys
FROM dapp-build as dapp-fs-build

# clean image
RUN apt -y autoremove && apt clean 
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /opt/dapp/

COPY --from=dapp-project-files-build /opt/dapp .

# TODO change to from dependecies file and add here
ADD bootfs.tar.gz /


# stage to build the dapp ext2 filesystem
FROM dapp-project-files-build as dapp-fsext-build

COPY img-pack.sh /usr/local/bin
COPY --from=dapp-fs-build / dappfs

RUN img-pack.sh /opt/cartesi/default.json dapp.json dappfs dapp.ext2

# stage to build the initial cartesi machine
FROM server-manager as machine-server

WORKDIR /opt/cartesi/dapp

# copy dapp ext2 from dapp stage
COPY --from=dapp-fsext-build /opt/cartesi/dapp/dapp.ext2 .

# copy rootfs, linux, rom
COPY --from=machine-core /opt/cartesi/share/* .

# build machine
COPY build-machine.sh /usr/local/bin
RUN build-machine.sh /opt/cartesi/share/dapp-bin

# switch back to server-manager workdir
WORKDIR /opt/cartesi/bin


# stage to run machine shell
FROM server-manager as machine-console

WORKDIR /opt/cartesi/dapp

# copy dapp ext2 from stage 1
COPY --from=dapp-fsext-build /opt/cartesi/dapp/dapp.ext2 .

# copy rootfs, kernel, rom
COPY --from=machine-core /opt/cartesi/share/* .

COPY run-machine-console.sh /usr/local/bin
CMD ["run-machine-console.sh"]


# stage to copy the stored machine
FROM busybox as machine-standalone

WORKDIR /opt/cartesi/share/dapp-bin
COPY --from=machine-server /opt/cartesi/share/dapp-bin .

CMD ["xxd", "-c", "256", "-p", "hash"]
