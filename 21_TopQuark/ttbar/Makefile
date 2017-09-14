######################################################################
# quite generic Makefile for ROOT-based programs with automatic
# dependency scanning
#
# (C) Martin Weber 2011-2013

# Name of the executable
PROGRAM        = ttbar_exec

######################################################################
# You should not modify the lines below here
#

# Setup for ROOT libraries
ROOTCFLAGS   := $(shell root-config --cflags)
ROOTLIBS     := $(shell root-config --libs)

CXX           = g++
CXXFLAGS      = -O2 -Wall -fPIC # -fsignaling-nans -g # -DNDEBUG # -pg for gprof
CXXFLAGS     += $(EXTINCDIR)   # external header files should be here
CXXFLAGS     += $(ROOTCFLAGS)

LD            = g++
LDFLAGS       = -O2 # -fsignaling-nans # -g # -lz # -pg for gprof

SOURCES       = $(wildcard *.C)
HEADERS       = $(SOURCES:.C=.h)
OBJECTS       = $(SOURCES:.C=.o)
DEPENDS       = $(SOURCES:.C=.d)

DATE	     := $(shell date "+%F")

######################################################################
# default targets

all:            $(PROGRAM)

clean:
		@rm -f $(OBJECTS) $(PROGRAM) $(DEPENDS)

distclean:      clean
		@rm -f *~ core *.def *.exp *.root *.ps *.pdf .def gmon.out

tarball:
		tar cvzf $(PROGRAM)-$(DATE).tar.gz Makefile *.h *.C *.cxx

######################################################################
# rules

.SUFFIXES: .cxx .$(ExeSrcSuf) .C .f .o .so .d

.cxx.o:
	$(CXX) $(CXXFLAGS) -c $<

.cpp.o:
	$(CXX) $(CXXFLAGS) -c $<

.cc.o:
	$(CXX) $(CXXFLAGS) -c $<

.C.o:
	$(CXX) $(CXXFLAGS) -c $<

.cpp.d:
	$(SHELL) -ec '$(CXX) -M $(CXXFLAGS) $< > $@'

.cxx.d:
	$(SHELL) -ec '$(CXX) -M $(CXXFLAGS) $< > $@'

.cc.d:
	$(SHELL) -ec '$(CXX) -M $(CXXFLAGS) $< > $@'

.C.d:
	$(SHELL) -ec '$(CXX) -M $(CXXFLAGS) $< > $@'

include $(DEPENDS)

######################################################################
# targets

$(PROGRAM):  $(OBJECTS)
	$(LD) $(LDFLAGS) $+ $(ROOTLIBS) -o $@
		@echo "$@ done"
