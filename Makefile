ifeq ($(filter -j%,$(MAKEFLAGS)),)
MAKEFLAGS += -j$(shell nproc)
endif

THIRD_PARTY_DIR := $(abspath third_party)

.PHONY: all
all: lake fixtures

.PHONY: setup
setup:
	./setup.sh

.PHONY: lake
lake:
	cd ElfLoader && lake build elfloader

.PHONY: fixtures
fixtures:
	$(MAKE) -C ElfLoader THIRD_PARTY_DIR=$(THIRD_PARTY_DIR)

.PHONY: run
run:
	cd ElfLoader && THIRD_PARTY_DIR=$(THIRD_PARTY_DIR) ./run.sh

.PHONY: clean
clean:
	$(MAKE) -C ElfLoader THIRD_PARTY_DIR=$(THIRD_PARTY_DIR) clean
