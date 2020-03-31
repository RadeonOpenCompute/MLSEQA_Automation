import os, sys, re, itertools, subprocess

HOME = os.environ['HOME']
hippath = "/home/master/HIP_Test/HIP/tests/src/"
destfolder = HOME + "/rocprof-hiptrace-tests"
binaryfolder = HOME + "/rocprof-hiptrace-tests/hiptrace-binaries/"
directed_binaries = destfolder + "/directed_binaries"
hiptrace_outdir = HOME + "/rocprof-hiptrace-output"
makefile_content = """
ROOT_PATH = /opt/rocm
LIB_PATH  = $(ROOT_PATH)/lib
ROC_LIBS  = -Wl,--rpath,${LIB_PATH} $(LIB_PATH)/libroctx64.so
HIP_PATH?= $(wildcard /opt/rocm/hip)
ifeq (,$(HIP_PATH))
	HIP_PATH=../../..
endif
HIPCC=$(HIP_PATH)/bin/hipcc
TARGET=hcc
COMMON_SRC = test_common.cpp
SOURCES = $(sourcecpp)
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE=./$(targetbinary)
.PHONY: test
all: clean $(EXECUTABLE)
CXXFLAGS =-g -I$(ROOT_PATH)
CXX=$(HIPCC)
$(EXECUTABLE): $(OBJECTS)
	$(HIPCC) $(OBJECTS) -o $@ $(ROC_LIBS)
test: $(EXECUTABLE)
	$(EXECUTABLE)
clean:
	rm -f $(EXECUTABLE)
	rm -f $(OBJECTS)
	rm -f $(HIP_PATH)/src/*.o
"""



def create_makefile():
    os.system("mkdir {destfolder} && touch {destfolder}/Makefile".format(destfolder=destfolder))
    text_file = open(destfolder + "/Makefile", "w")    
    n = text_file.write(makefile_content)
    text_file.close()


#copy all 148 directed hip api cpp files in generic folder
def rocprof_copy_hipcpp():
    #directed_binaries = destfolder + "/directed_binaries"
    print(directed_binaries)
    os.system("cd %s && mkdir %s && mkdir -r %s" %(HOME,destfolder,directed_binaries))
    os.system("cd %s && mkdir directed_binaries" %destfolder)
    for (path, dirs, files) in os.walk(hippath):
        for f in files:
            cppfile = path + "/" + f            
            os.system("cp {cppfile} {destfolder}".format(cppfile=cppfile,destfolder=destfolder))
            if "cpp" in f:
                print(f)
                binfile = f.split(".")[0]
                if os.path.exists(directed_binaries):                   
                    os.system("cd {destfolder} && pwd && make sourcecpp={cppfile} targetbinary=directed_binaries/{binfile}".format(cppfile=f,destfolder=destfolder,binfile=binfile))
                else:
                    print("directed binaries folder doesn't exist")


def rocprof_run_binary():
    os.system("mkdir %s" %hiptrace_outdir)
    print(hiptrace_outdir)
    for (path, dirs, files) in os.walk(directed_binaries):
        print("Hi")
        for f in files:
            testpath = directed_binaries + "/" + f
            print(testpath)
            os.system("/opt/rocm/bin/rocprof --hip-trace -d %s -o %s/%s_test_case_2.csv %s" %(hiptrace_outdir,hiptrace_outdir,f,testpath))
        



#create_makefile()
#rocprof_copy_hipcpp()
rocprof_run_binary()
