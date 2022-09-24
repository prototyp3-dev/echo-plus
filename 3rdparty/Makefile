
GEOS_VERSION := 3.11.0

.PHONY: clean

all: geos

geos:
	wget https://github.com/libgeos/geos/archive/refs/tags/$(GEOS_VERSION).tar.gz
	tar xvf $(GEOS_VERSION).tar.gz
	rm $(GEOS_VERSION).tar.gz
	cd geos-$(GEOS_VERSION) && mkdir build && cd build && \
		cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${ROOT_DIR}/geos -DBUILD_SHARED_LIBS=true ..
	# cd geos-$(GEOS_VERSION)/build && make -j3 && make install
	# CC=$(CC) CXX=$(CXX) CXXFLAGS="-march=${ARCH} -I${ROOT_DIR}/glibc/include -I${TARGET_DIR}/include ${CXXFLAGS}" \
	# 	CFLAGS="-march=${ARCH} -I${ROOT_DIR}/glibc/include -I${TARGET_DIR}/include ${CFLAGS}" \
	# 	LDFLAGS="-L${ROOT_DIR}/glibc/libs -L${TARGET_DIR}/lib -L${ROOT_DIR}/../.env/cross/lib -L${PYTHON_DIR}/lib ${LDFLAGS}" && \
	# 	cd geos-$(GEOS_VERSION) && mkdir build && cd build && \
	cd geos-$(GEOS_VERSION)/build && make -j$(nproc) && make install
	rm -rf geos-$(GEOS_VERSION)
