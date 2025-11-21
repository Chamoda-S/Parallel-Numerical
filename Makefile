CC ?= gcc
MPICC ?= mpicc
CFLAGS ?= -O2 -Wall -std=c11 -Iinclude
OMPFLAG ?= -fopenmp
LIBS ?= -lm

SRCDIR = src
BINDIR = bin

all: serial openmp mpi

serial: $(BINDIR)/serial

openmp: $(BINDIR)/openmp

mpi: $(BINDIR)/mpi

$(BINDIR):
	mkdir -p $(BINDIR)

$(BINDIR)/serial: $(SRCDIR)/main_serial.c $(SRCDIR)/trapezoid.c | $(BINDIR)
	$(CC) $(CFLAGS) $^ $(LIBS) -o $@

$(BINDIR)/openmp: $(SRCDIR)/main_openmp.c $(SRCDIR)/trapezoid.c | $(BINDIR)
	$(CC) $(CFLAGS) $(OMPFLAG) $^ $(LIBS) -o $@

$(BINDIR)/mpi: $(SRCDIR)/main_mpi.c $(SRCDIR)/trapezoid.c | $(BINDIR)
	$(MPICC) $(CFLAGS) $^ $(LIBS) -o $@

clean:
	rm -f $(BINDIR)/serial $(BINDIR)/openmp $(BINDIR)/mpi

.PHONY: all serial openmp mpi clean
