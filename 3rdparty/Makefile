
GEOS_VERSION := 3.11.0

.PHONY: clean

all: geos

geos:
	wget https://github.com/libgeos/geos/archive/refs/tags/$(GEOS_VERSION).tar.gz
	tar xvf $(GEOS_VERSION).tar.gz
	rm $(GEOS_VERSION).tar.gz
	cd geos-$(GEOS_VERSION) && mkdir build && cd build && \
		cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${ROOT_DIR}/geos -DBUILD_SHARED_LIBS=true ..
	cd geos-$(GEOS_VERSION)/build && make -j$(nproc) && make install
	rm -rf geos-$(GEOS_VERSION)
