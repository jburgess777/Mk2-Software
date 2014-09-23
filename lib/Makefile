# Tell make to use C++ compiler rule for .c files
COMPILE.c = $(COMPILE.cc)

CPPFLAGS += -g -Wall -O2

.PHONY: clean all test help

help:
	@echo "This Makefile supports the following targets:"
	@echo "    * signer   build signer executable"
	@echo "    * test     check signer operation"
	@echo "    * all      creates executable and runs test"
	@echo "    * clean    removes executable and object files"
	@echo "    * keys.txt generate a new key pair"
	@echo "    * keys.sh  create shell script to set generated keys when running MCP"
	@echo "    * keys.c   generate C code for adding new public key into Tilda firmware"

all: signer test

main.o uECC.o: uECC.h

signer: main.o uECC.o
	$(LINK.cc) -o $@ $^

clean:
	rm -f signer main.o uECC.o

test:
	./test.sh

keys.txt:
	./signer create > $@

keys.sh: keys.txt
	( \
	  echo "# To generate radio messages signed with your key pair you must"; \
	  echo "# set these environment variables before running the MCP"; \
	  echo -n "export EMF_PRIVATE_KEY="; \
	  echo `grep -A 1 "PRIVATE:" $^ | tail -n 1`; \
	  echo -n "export EMF_PUBLIC_KEY="; \
	  echo `grep -A 1 "PUBLIC:" $^ | tail -n 1` \
	) | tee $@

keys.c: keys.txt
	( \
	  echo "# To make your badge trust messages signed by your"; \
	  echo "# new key pair you must replace the public key in"; \
	  echo "# EMF2014Config.h with:"; \
	  echo ""; \
	  echo "const uint8_t EMF_PUBLIC_KEY[40] = {"; \
	  grep -A 1 "PUBLIC:" $^ | tail -n 1 | xxd -r -p | xxd -i -c 10; \
	  echo "};"; \
	  echo ""; \
	  echo "# Then rebuild the firmware and download to your badge."; \
	) | tee $@
