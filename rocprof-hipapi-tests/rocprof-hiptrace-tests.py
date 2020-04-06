import os, sys, re, itertools, subprocess, shutil, json
import texttable as tt
from prettytable import PrettyTable



if len(sys.argv) != 2:
    print("Please make sure you have entered HIP path, eg:/home/taccuser/HIP/")
    sys.exit(1)



HOME = os.environ['HOME']
hippath = HOME + "%s/tests/src/" %sys.argv[1]
destfolder = HOME + "/rocprof-hiptrace-tests"
binaryfolder = HOME + "/rocprof-hiptrace-tests/hiptrace-binaries/"
directed_binaries = destfolder + "/directed_binaries"
hiptrace_outdir = HOME + "/rocprof-hiptrace-output"
hipapi_trace_folders = []
conf_path= "./conf.json"
y = []
tab = tt.Texttable()
x = [[]]
tottests=[]
totresults=[]
z = PrettyTable()
z.field_names = ["TotalTests","TotalPass","TotalFail"]
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
        print(hiptrace_outdir)
        #shutil.rmtree(hiptrace_outdir)
        os.system("sudo rm -r %s" %hiptrace_outdir)
    else:
        print("Hip trace output folder not exist so creating new")
        
    

def create_makefile():
    os.system("mkdir {destfolder} && touch {destfolder}/Makefile".format(destfolder=destfolder))
    text_file = open(destfolder + "/Makefile", "w")    
    n = text_file.write(makefile_content)
    text_file.close()



def hip_load_conf(var):
    config = json.loads(open(conf_path).read())
    return config["%s" %var]



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
                apitracedata_outdir = hiptrace_outdir + "/" + f 
                #+ "-" + str(testnum)
                os.makedirs(apitracedata_outdir, exist_ok=True)
                #os.system("cd {outdir} && sudo mkdir {outputdir}".format(outdir=hiptrace_outdir,outputdir=apitracedata_outdir))
                os.system("cd %s && sudo /opt/rocm/bin/rocprof --hip-trace -d . -o ./%s_test_case.csv %s" %(apitracedata_outdir,f,testpath))
                hipapi_trace_folders.append(apitracedata_outdir)



def hip_get_trace_data():
    rplfolder = ""    
    filenames= os.listdir(hiptrace_outdir)   
    testnum = 0
    for subfolder in filenames:
        outputpath = hiptrace_outdir + "/" + subfolder
        inputdir = []
        inputfiles = []
        count = 0
        for (path, dirs, files) in os.walk(outputpath):                     
            inputfiles.append(files)
            inputdir.append(dirs)            
            count += 1              
        testcase_name = subfolder
        testnum = testnum + 1
        if count > 3:
            print("two rpl folders")
            hiptracefile = outputpath + "/" + inputdir[0][0] + "/" + str(inputdir[1][0]) + "/hip_api_trace.txt"            
            #hip_get_trace_api(subfolder,hiptracefile)
            x.append([s_no,"rocprof-hiptrace-" + testcase_name,hip_get_trace_api(subfolder,hiptracefile)])
        else:            
            print("one rpl folders")       
            hiptracefile = outputpath + "/" + inputdir[0][0] + "/" + inputdir[1][0] + "/hip_api_trace.txt"
            #hip_get_trace_api(subfolder,hiptracefile)
            result = hip_get_trace_api(subfolder,hiptracefile)
            x.append([testnum,"rocprof-hiptrace-" + testcase_name + "-" + str(testnum),result])
            totresults.append(result)
            tottests.append(testnum)    
    tab.add_rows(x)
    tab.set_cols_align(['r','r','r'])
    tab.header(['S.no', 'HIPTrace-HIPApi-TestCase Names', 'Result'])
    print(tab.draw())



def hip_get_trace_api(test,path):
    res = ""
    try:        
        apiname = test
        result = []
        try:
            print(path)            
            apis = hip_load_conf(test)
            for i in apis:
                with open(path, "r") as f:
                    if i in f.read():
                        print("pass")
                        print(i)
                        result.append("pass")
                    else:                        
                        print("fail")
                        print(i)
                        result.append("fail")
        except FileNotFoundError:
            print("File does not exist")
            res="Fail"
            pass
        except:
            res="Fail"
            print("Other error")
        if "fail" in result:
            print(test + ": Failed")
            res = "Fail"
        else:
            print(test + ": Passed")
            res = "Pass"        
    except:
        res = "Fail"
        print("Other error")
    return res
        

        
def hiptrace_print_summary():   
    totpass=[]
    totfail=[]
    for i in totresults:
        if i == "Pass":
            totpass.append(i)
        else:
            totfail.append(i)
    z.add_row([len(tottests), len(totpass), len(totfail)])
    print(z)
        



        



#remove_hiptrace_outputdir()
#create_makefile()
#rocprof_copy_hipcpp()
#rocprof_run_binary()
hip_get_trace_data()
hiptrace_print_summary()
#hip_get_trace_api()
