
TARGET := riscv64-cartesi-linux-gnu
TARGET_DIR := /opt/riscv/$(TARGET)/$(TARGET)

CC := $(TARGET)-gcc
CXX := $(TARGET)-g++


GEOS_VERSION := 3.11.0
GLIBC_VERSION := 2.36
OPENCV_VERSION := 4.6.0
OPENCV_PYTHON_VERSION := 66
NUMPY_VERSION := 1.23.3
OPENSSL_VERSION := 3.0.5
SK_VERSION := 0.15.0

.PHONY: clean

all: geos

# glibc:
# 	wget https://ftp.gnu.org/gnu/glibc/glibc-$(GLIBC_VERSION).tar.xz
# 	tar xvf glibc-$(GLIBC_VERSION).tar.xz
# 	rm glibc-$(GLIBC_VERSION).tar.xz
# 	CXXFLAGS="${CXXFLAGS} -O2" CFLAGS="${CFLAGS} -O2" && \
# 		cd glibc-$(GLIBC_VERSION) && mkdir build && cd build && \
# 		../configure $(TARGET) CC=$(CC) --prefix=$(ROOT_DIR)/3rdparty/glibc
# 	cd glibc-$(GLIBC_VERSION)/build && make && make install
# 	# cd glibc-$(GLIBC_VERSION)/build && make -j$(nproc) && make install
# 	rm -rf glibc-$(GLIBC_VERSION)

geos: 
	wget https://github.com/libgeos/geos/archive/refs/tags/$(GEOS_VERSION).tar.gz
	tar xvf $(GEOS_VERSION).tar.gz
	rm $(GEOS_VERSION).tar.gz
	CXXFLAGS="-march=${ARCH} ${CXXFLAGS}" CFLAGS="-march=${ARCH} ${CFLAGS}" && \
		cd geos-$(GEOS_VERSION) && mkdir build && cd build && \
		cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${ROOT_DIR}/3rdparty/geos -DBUILD_SHARED_LIBS=true ..
	cd geos-$(GEOS_VERSION)/build && make -j3 && make install
	# cd geos-$(GEOS_VERSION)/build && make -j$(nproc) && make install
	rm -rf geos-$(GEOS_VERSION)

openssl:
	wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz
	tar xvf openssl-$(OPENSSL_VERSION).tar.gz
	rm openssl-$(OPENSSL_VERSION).tar.gz
	CXXFLAGS="-march=${ARCH} ${CXXFLAGS}" CFLAGS="-march=${ARCH} ${CFLAGS}" && \
		cd openssl-${OPENSSL_VERSION} && \
		./Configure linux64-riscv64 --prefix=${ROOT_DIR}/3rdparty/openssl
	cd openssl-${OPENSSL_VERSION} && make -j3 && make install
	# cd openssl-${OPENSSL_VERSION} && make -j$(nproc) && make install
	rm -rf openssl-${OPENSSL_VERSION}

CYTHON_VERSION := 0.29.32

cython:
	wget https://github.com/cython/cython/archive/refs/tags/${CYTHON_VERSION}.tar.gz
	tar xvf ${CYTHON_VERSION}.tar.gz
	rm ${CYTHON_VERSION}.tar.gz
	cd cython-${CYTHON_VERSION} && \
		python setup.py build && python setup.py install
	rm -rf cython-${CYTHON_VERSION}


numpy: 
	wget https://github.com/numpy/numpy/releases/download/v$(NUMPY_VERSION)/numpy-$(NUMPY_VERSION).tar.gz
	tar xvf numpy-$(NUMPY_VERSION).tar.gz
	rm numpy-$(NUMPY_VERSION).tar.gz
	cd numpy-$(NUMPY_VERSION) && \
		python setup.py build && python setup.py install
#		python -m pip install -r test_requirements.txt && \
#		pip3.10 install -vvv --no-use-pep517 --global-option="install"  --global-option="${CFLAGS}" --global-option="${LDFLAGS}" .
# 	cd numpy-$(NUMPY_VERSION) && CXX=$(CXX) CC=$(CC) python setup.py build -j$(nproc) install --prefix $(ROOT_DIR)/3rdparty/numpy
# 	pip3.10 install .
	rm -rf numpy-$(NUMPY_VERSION)

opencv: openssl
	wget https://github.com/opencv/opencv/archive/refs/tags/$(OPENCV_VERSION).tar.gz
	tar xvf $(OPENCV_VERSION).tar.gz
	rm $(OPENCV_VERSION).tar.gz
	CXXFLAGS="-march=${ARCH} ${CXXFLAGS}" CFLAGS="-march=${ARCH} ${CFLAGS}" && \
		cd opencv-$(OPENCV_VERSION) && mkdir build && cd build && \
		cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$(ROOT_DIR)/3rdparty/geos -DBUILD_SHARED_LIBS=true ..
	cd opencv-$(OPENCV_VERSION)/build && make -j3 && make install
	rm -rf opencv-$(OPENCV_VERSION)
	wget https://github.com/opencv/opencv-python/archive/refs/tags/$(OPENCV_PYTHON_VERSION).tar.gz
	tar xvf $(OPENCV_PYTHON_VERSION).tar.gz
	rm $(OPENCV_PYTHON_VERSION).tar.gz
	CXXFLAGS="${CXXFLAGS} -I${ROOT_DIR}/3rdparty/openssl/include -I${ROOT_DIR}/3rdparty/opencv/include" CFLAGS="${CFLAGS} -I${ROOT_DIR}/3rdparty/openssl/include -I${ROOT_DIR}/3rdparty/opencv/include" 
		LDFLAGS="${LDFLAGS} -L${ROOT_DIR}/3rdparty/openssl/lib -L${ROOT_DIR}/3rdparty/opencv/lib" && \
		pip3.10 install scikit-build==${SK_VERSION} && \
		pip install -vvv --no-use-pep517 --global-option="${CFLAGS}" --global-option="${LDFLAGS}" .
	#	pip install -vvv --no-binary opencv-python --global-option="${CFLAGS}" --global-option="${LDFLAGS}"
	#	cd opencv-python-$(OPENCV_PYTHON_VERSION) && \
	#	python3 setup.py bdist_wheel && python setup.py build && python setup.py install
	# rm -f /usr/bin/g++ || :
	# ln -s $(whereis $(CXX) | awk '{print $2}') /usr/bin/g++
	# rm -f /usr/bin/gcc || :
	# ln -s $(whereis $(CC) | awk '{print $2}') /usr/bin/gcc
	# export CMAKE_ARGS="-DCMAKE_C_COMPILER=$(CC) -DCMAKE_CXX_COMPILER=$(CXX) -DCMAKE_SYSTEM_PROCESSOR=$(TARGET) -DCMAKE_INSTALL_PREFIX=$(ROOT_DIR)/3rdparty/opencv-python"
	# export CMAKE_C_COMPILER=$(CC)
	# cd opencv-python-$(OPENCV_PYTHON_VERSION) && pip wheel . --verbose
	rm -rf opencv-python-$(OPENCV_PYTHON_VERSION)
