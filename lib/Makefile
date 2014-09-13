# Tell make to use C++ compiler rule for .c files
COMPILE.c = $(COMPILE.cc)

CPPFLAGS += -g -Wall -O2

.PHONY: clean all test

all: signer test

main.o uECC.o: uECC.h

signer: main.o uECC.o
	$(LINK.cc) -o $@ $^

clean:
	rm -f signer main.o uECC.o

test:
	./test.sh

keys.txt: signer
	./signer create > $@

keys.sh: keys.txt
	( \
	  echo -n "export EMF_PRIVATE_KEY="; \
	  echo `grep -A 1 "PRIVATE:" $^ | tail -n 1`; \
	  echo -n "export EMF_PUBLIC_KEY="; \
	  echo `grep -A 1 "PUBLIC:" $^ | tail -n 1` \
	) > $@
