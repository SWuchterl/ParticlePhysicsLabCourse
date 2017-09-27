LIBLAB=$(HOME)/liblab
LIBPATH=$(LIBLAB)
INCPATH=$(LIBLAB)

BIN=control
OBJ=sipm_fe.o

GPP=g++
LD=g++
CFLAGS=-Wall -c -I$(INCPATH)
LDFLAGS=-Wall -L$(LIBPATH) -llab  -lusb -lpthread

.PHONY:	all clean

all:	$(BIN)
	@echo "done."

$(BIN): $(OBJ) $(BIN).o 
	@echo -n ">>> Linking   "
	$(GPP) $^ -o $@ $(LDFLAGS)

%.o:	%.cpp
	@echo -n ">>> Compiling "
	$(GPP) $(CFLAGS) $<

clean:
	rm -f $(BIN)
	rm -f *.o
