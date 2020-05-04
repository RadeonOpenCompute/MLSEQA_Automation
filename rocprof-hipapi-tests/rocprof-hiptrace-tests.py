## Created by    : Rahul Mula
## Creation Date : 06/04/2020
## Description   : Script for Testing Directed hip API's with --hip-trace option (total 158 api's covered)
import os, sys, re, itertools, subprocess, shutil, json
import texttable as tt
from prettytable import PrettyTable



if len(sys.argv) != 2:
    print("Please make sure you have entered HIP path, eg:/home/taccuser/HIP/")
    sys.exit(1)



HOME = os.environ['HOME']
hippath = "%stests/src/" %sys.argv[1]
destfolder = HOME + "/rocprof-hiptrace-tests/"
binaryfolder = HOME + "/rocprof-hiptrace-tests/hiptrace-binaries/"
directed_binaries = destfolder + "directed_binaries"
hiptrace_outdir = HOME + "/rocprof-hiptrace-output"
hipapi_trace_folders = []
conf_path= "./conf.json"
y = []
tab = tt.Texttable()
x = [[]]
tottests=[]
totresults=[]
z = PrettyTable()
z.field_names = ["TotalTests","TotalPass","TotalFail","Not Supported"]





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
    try:
        if os.path.exists("%s" %hiptrace_outdir):
            print(hiptrace_outdir)
            os.system("sudo rm -r %s" %hiptrace_outdir)
            os.system("mkdir -p %s" %hiptrace_outdir)
        else:
            os.system("mkdir -p %s" %hiptrace_outdir)
            print("Hip trace output folder not exist so creating new")
    except:
        print("error in remove_hiptrace_outputdir")
        
    

def create_makefile():
    try:
        os.system("touch {destfolder}/Makefile".format(destfolder=destfolder))
        text_file = open(destfolder + "/Makefile", "w")    
        n = text_file.write(makefile_content)
        text_file.close()
    except:
        print("error in create makefile")



def hip_load_conf(var):
    config = json.loads(open(conf_path).read())
    return config["%s" %var]



#copy all 148 directed hip api cpp files in generic folder
def rocprof_copy_hipcpp():    
    try:
        print(directed_binaries)
        try:
            if os.path.exists("%s" %destfolder):
                print("folder deleted")
                os.system("sudo rm -r %s" %hiptrace_outdir)
                os.system("cd %s && mkdir %s && mkdir  %s" %(HOME,destfolder,directed_binaries))
                os.system("cd %s && mkdir -p directed_binaries" %destfolder)
            else:
                print("folder not deleted")
                os.system("cd %s && mkdir %s && mkdir  %s" %(HOME,destfolder,directed_binaries))
                os.system("cd %s && mkdir -p directed_binaries" %destfolder)
        except:
            print("cannot create directed_binaries folder")
        for (path, dirs, files) in os.walk(hippath):            
            for f in files:
                cppfile = path + "/" + f
                print(f)
                os.system("cp {cppfile} {destfolder}".format(cppfile=cppfile,destfolder=destfolder))
                # filter if not line.startswith('?') and string has "hip_"
                #if "hip_" in f or not f.startswith('h'):                    
                    #print(f + " : Not a hip directed test")
                    #if "test_common" or "is_callable_test" or "gxxApi1" or "hc_am" or "hip_runtime" or "gxxHipApi" or "clara" in f:
                        #os.system("cp {cppfile} {destfolder}".format(cppfile=cppfile,destfolder=destfolder))
                #else:
                    #os.system("cp {cppfile} {destfolder}".format(cppfile=cppfile,destfolder=destfolder))                
    except:
        print("error in rocprof_copy_hipcpp")


def rocprof_make():
    create_makefile()    
    try:
        for r, d, f in os.walk(destfolder):
            for item in f:
                cppfile = r + item
                if '.cpp' in item:
                    binfile = item.split(".")[0]                    
                    #if os.path.exists(directed_binaries):
                    if "hip_" in item or not item.startswith('h'):
                        print(item + " : Not a hip directed test")
                    else:
                            os.system("cd {destfolder} && pwd && make sourcecpp={cppfile} targetbinary=directed_binaries/{binfile}".format(cppfile=cppfile,destfolder=destfolder,binfile=binfile))
                    #else:
                        #os.system("mkdir {destfolder}/directed_binaries/".format(destfolder=destfolder))
                        #os.system("cd {destfolder} && pwd && make sourcecpp={cppfile} targetbinary=directed_binaries/{binfile}".format(cppfile=f,destfolder=destfolder,binfile=binfile))
                        #print("directed binaries folder doesn't exist")
    except:
        print("error in the code")



def rocprof_run_binary():
    try:
        os.system("mkdir -p %s" %hiptrace_outdir)
        print(hiptrace_outdir)
        testnum = 0        
        for (path, dirs, files) in os.walk(directed_binaries):            
            for f in files:
                testnum = testnum + 1
                testpath = directed_binaries + "/" + f
                print(testpath)
                if "hipStressMemcpy" not in f:
                    apitracedata_outdir = hiptrace_outdir + "/" + f                 
                    os.makedirs(apitracedata_outdir, exist_ok=True)
                    os.system("cd %s && sudo /opt/rocm/bin/rocprof --hip-trace -d . -o ./%s_test_case.csv %s" %(apitracedata_outdir,f,testpath))
                    hipapi_trace_folders.append(apitracedata_outdir)
                    print(apitracedata_outdir)
    except:
        print("error in rocprof_run_binary")


def hip_get_trace_data():
    try:
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
                print(inputdir[0])
                print(inputdir[1])
                hiptracefile = outputpath + "/" + inputdir[0][0] + "/" + str(inputdir[1][0]) + "/hip_api_trace.txt"
                x.append([s_no,"rocprof-hiptrace-" + testcase_name,hip_get_trace_api(subfolder,hiptracefile)])
                print("Contains two rpl folders, please make sure only one rpl folder present")
                totresults.append(result)
                #exit()
            else:
                print("one rpl folders")
                if "Tex" in testcase_name:
                    hiptracefile = outputpath + "/" + inputdir[0][0] + "/" + inputdir[1][0] + "/hip_api_trace.txt"
                    #result = hip_get_trace_api(subfolder,hiptracefile)
                    result = "NotApplicable"
                    x.append([testnum,"rocprof-hiptrace-" + testcase_name + "-" + str(testnum),result])
                    totresults.append(result)
                else:  
                    hiptracefile = outputpath + "/" + inputdir[0][0] + "/" + inputdir[1][0] + "/hip_api_trace.txt"
                    result = hip_get_trace_api(subfolder,hiptracefile)
                    x.append([testnum,"rocprof-hiptrace-" + testcase_name + "-" + str(testnum),result])
                    totresults.append(result)
            tottests.append(testnum)
        tab.add_rows(x)
        tab.set_cols_align(['r','r','r'])
        tab.header(['S.no', 'HIPTrace-HIPApi-TestCase Names', 'Result'])
        print(tab.draw())
    except:
        print("error in hip_get_trace_data")



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
        elif len(result) == 0:
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
    totna=[]
    for i in totresults:
        if i == "Pass":
            totpass.append(i)
        elif i == "NotApplicable":
            totna.append(i)
        elif i == "Fail":
            totfail.append(i)
        else:
            print("Notmentioned")
    z.add_row([len(tottests), len(totpass), len(totfail), len(totna)])
    print(z)
        



        



#remove_hiptrace_outputdir()
#rocprof_copy_hipcpp()
#rocprof_make()
#rocprof_run_binary()
hip_get_trace_data()
hiptrace_print_summary()


#hip_get_trace_api()
