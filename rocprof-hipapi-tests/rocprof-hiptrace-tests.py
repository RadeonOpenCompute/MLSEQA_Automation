import os, sys, re, itertools, subprocess, shutil

HOME = os.environ['HOME']
hippath = HOME + "/HIP_Test/HIP/tests/src/"
destfolder = HOME + "/rocprof-hiptrace-tests"
binaryfolder = HOME + "/rocprof-hiptrace-tests/hiptrace-binaries/"
directed_binaries = destfolder + "/directed_binaries"
hiptrace_outdir = HOME + "/rocprof-hiptrace-output"
hipapi_trace_folders = []
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

def remove_hiptrace_outputdir():
    if os.path.exists("%s" %hiptrace_outdir):
       shutil.rmtree(hiptrace_outdir, ignore_errors=True)
    

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
    testnum = 0
    for (path, dirs, files) in os.walk(directed_binaries):
        print("Hi")
        for f in files:
            testnum = testnum + 1
            testpath = directed_binaries + "/" + f
            print(testpath)
            if "hipStressMemcpy" not in f:
                apitracedata_outdir = hiptrace_outdir + "/hiptrace-" + f + "-" + str(testnum)
                os.makedirs(apitracedata_outdir, exist_ok=True)
                #os.system("cd {outdir} && sudo mkdir {outputdir}".format(outdir=hiptrace_outdir,outputdir=apitracedata_outdir))
                os.system("cd %s && sudo /opt/rocm/bin/rocprof --hip-trace -d . -o ./%s_test_case_%s.csv %s" %(apitracedata_outdir,f,testnum,testpath))
                hipapi_trace_folders.append(apitracedata_outdir)


def hip_get_trace_data():
    #hipapitotrace=['','']
    inputdir = []
    rplfolder = ""

    #for folder in hipapi_trace_folders:
    filenames= os.listdir(hiptrace_outdir)
    print(filenames)
    #for (path, dirs, files) in os.walk(hiptrace_outdir):
    #outputpath = hiptrace_outdir + "/" + filenames 
    for subfolder in filenames:
        outputpath = hiptrace_outdir + "/" + subfolder
        print(outputpath)
        for (path, dirs, files) in os.walk(outputpath):
            print(dirs)
            #os.path.join(outputdir, )
            inputdir.append(dirs)
            count = 0
            for string in inputdir:
                count += 1
            print(count)
        #rpldata = os.path.join(subfolder, str(", ".join(inputdir[0])))
        #print(rpldata)
        #hiptrace_dir = os.path.join(rpldata, str(", ".join(inputdir[1])))
        #hiptrace_file = hiptrace_dir + "/hip_api_trace.txt"
        #print(hiptrace_file)
        
        #with open(hiptrace_file, "r") as file:
        



#remove_hiptrace_outputdir()
#create_makefile()
#rocprof_copy_hipcpp()
#rocprof_run_binary()
hip_get_trace_data()
