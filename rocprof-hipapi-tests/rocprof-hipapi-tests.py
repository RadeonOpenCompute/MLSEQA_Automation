## Created by    : Rahul Mula
## Creation Date : 12/03/2020
## Description   : Script for Testing rocprofiler with HIP 148 API's
import os, sys, re, itertools, subprocess, shutil
import os.path
import texttable as tt


if len(sys.argv) != 2:
    print("Please make sure you have entered HIP path, eg:/home/taccuser/HIP/")
    sys.exit(1)


HOME = os.environ['HOME']
hip_gitpath = "https://github.com/ROCm-Developer-Tools/HIP.git"
outputpath = "%s/rocprofiler_hipapi_automation_test_cases/" %HOME
hippath = "%sbuild/directed_tests/" %sys.argv[1]
newlist = []
tab = tt.Texttable()
x = [[]]


def prerequisite():
    os.popen("sudo apt-get install git")       
    subprocess.check_call([sys.executable, "-m", "pip", "install", "texttable"]) 


def hip_clone_repo():
    if os.path.exists("%s/HIP" %HOME):
        try:
            os.system("sudo chmod 755 %s/HIP/" %HOME) 
            shutil.rmtree("%s/HIP/" %HOME, onerror=handleError)
        except:
            os.rmdir("%s/HIP/" %HOME)
    else:
        print("HIP path doesn't exists")
    os.system("cd %s && git clone %s" %(HOME,hip_gitpath))
    os.system("cd %s/HIP && mkdir build" %HOME)
    os.system("cd %s/HIP/build && cmake .. -DCMAKE_INSTALL_PREFIX=$PWD/install && sudo make -j16" %HOME)
    os.system("cd %s/HIP/build && sudo make install && make check" %HOME)




def handleError(func, path, exc_info):
    pass

def hip_clear_hipapi_outputfolder():
    if os.path.exists("%s" %outputpath):
       shutil.rmtree(outputpath, ignore_errors=True)
   

   
def hip_run_apitests():
    list_dir = []   
    testnum = 0
    for (path, dirs, files) in os.walk(hippath):
        for f in files:
            hip_apitests = os.path.join(path, f)
            testnum = testnum + 1
            testpath = outputpath + f + "_test_case_" + str(testnum)
            os.system("/opt/rocm/bin/rocprof -d %s -o %s/%s_test_case_%s.csv %s" %(testpath,testpath,f,testnum,hip_apitests))
        src_path = path.split("/")
        print(src_path)


def hip_print_testresults():

    #testpath = r'/home/taccuser/HIP/build/directed_tests/'
    #csvdir = "/home/taccuser/rocprof_automation_test_cases/"
    kernel_count = []
    count = 0
    for (path, dirs, files) in os.walk(hippath):                
        for f in files:
            hip_apitests = os.path.join(path, f)
            count = count + 1
            testpath = outputpath + f + "_test_case_" + str(count)
            csvfile = testpath + "/" + f + "_test_case_%s.csv" %count
            print(csvfile)
            directedpath= path + "/" + f
            cpppath = directedpath.replace("//", "/")                                                               
            hip_print_testsummary(count,hip_get_cpppath(cpppath),csvfile,hip_get_csvkernel_count(csvfile),hip_api_determine(f,hip_get_cpppath(cpppath)))          
            cppkernelcount = hip_api_determine(f, hip_get_cpppath(cpppath))
            if hip_get_csvkernel_count(csvfile) == cppkernelcount:
                x.append([count,str("rocprof_hipapi_" + f + "test_case_" + str(count)),"Pass"])
            else:
                x.append([count,str("rocprof_hipapi_" + f + "test_case_" + str(count)),"Fail"])
            
    tab.add_rows(x)
    tab.set_cols_align(['r','r','r'])
    tab.header(['S.no', 'ROCProf-HIPApi-TestCase Names', 'Result'])
    print(tab.draw())

          

def hip_print_testsummary(count,cpppath,csvfile,csvkernelcount,cppkernelcount):
    print(count)
    print("CPP path: " + str(cpppath))
    print("CSV path: " + str(csvfile))
    print("CSV kernel count: " + str(csvkernelcount))
    print("CPP kernel count: " + str(cppkernelcount))


def hip_api_determine(testname,path):

    watchword = "hipLaunchKernelGGL"
    if testname == "hipFuncDeviceSynchronize":
        return hip_get_cppkernel_count(watchword,path) + 1
    elif testname == "hipNormalizedFloatValueTex":
        return hip_get_cppkernel_count(watchword,path) + 4
    elif testname == "hipTexObjPitch":
        return hip_get_cppkernel_count(watchword,path) + 5
    elif testname == "simpleTexture3D":
        return (hip_get_cppkernel_count(watchword,path) + 2) * 24
    elif testname == "simpleTexture2DLayered":
        return hip_get_cppkernel_count(watchword,path) + 4
    elif testname == "hipLanguageExtensions":
        return hip_get_cppkernel_count(watchword,path) - 1
    elif testname == "hipShflTests":
        return hip_get_cppkernel_count(watchword,path) + 3
    elif testname == "hipShflUpDownTest":
        return hip_get_cppkernel_count(watchword,path) + 6
    elif testname == "hipExtLaunchKernelGGL":
        watchword = "hipExtLaunchKernelGGL"
        return hip_get_cppkernel_count(watchword,path)
    elif testname == "hipLaunchParmFunctor":
        return hip_get_cppkernel_count(watchword,path) - 2
    elif testname == "hip_test_ldg":
        return hip_get_cppkernel_count(watchword,path) * 9
    elif testname == "hipTestDevice" or testname == "hipMathFunctions" or testname == "complex_loading_behavior":
        return hip_get_cppkernel_count(watchword,path) - 1
    elif testname == "LaunchKernel":
        watchword = "hipLaunchKernel"
        return hip_get_cppkernel_count(watchword,path)
    elif testname == "hipClassKernel":
        return hip_get_cppkernel_count(watchword,path) - 6
    else:
        return hip_get_cppkernel_count(watchword,path)
    


def hip_get_cpppath(path):   
    src_path = path.split("/")
    len_srcpath = len(src_path)    
    if len_srcpath == 8:
        source_path = "/" + src_path[1] + "/" + src_path[2] + "/" + src_path[3] + "/tests/src/" + src_path[6] + "/" + src_path[7]        
        return hip_check_fileexists(source_path)        
    elif len_srcpath == 7:
        source_path = "/" + src_path[1] + "/" + src_path[2] + "/" + src_path[3] + "/tests/src/" + src_path[6]        
        return hip_check_fileexists(source_path)        
    elif len_srcpath == 9:
        source_path = "/" + src_path[1] + "/" + src_path[2] + "/" + src_path[3] + "/tests/src/" + src_path[6] + "/" + src_path[7] + "/" + src_path[8]        
        return hip_check_fileexists(source_path)


def hip_check_fileexists(path):
    cpppath = path + ".cpp"
    cpath = path + ".c"
    if os.path.isfile(cpppath):
        return cpppath
    elif os.path.isfile(cpath):
        return cpath
    else:
        print ("File not exist")




def hip_get_cppkernel_count(watchword,path):     
    kernel_count = []
    try: 
        with open(path, "r") as fp:
            for line in fp:
                if watchword in line:                    
                    kernel_count.append(line)                
        count=0
        for i in kernel_count:
            count=count+1            
        return count
    except FileNotFoundError as error:
        print(error)
        print("File does not exist")
        pass
    except:
        print("Other error")
        pass


def hip_get_csvkernel_count(csvfile):
    kernel_count = [] 
    try:
        with open(csvfile, "r") as fp:
            for line in fp:                            
                kernel_count.append(line)    
        count=0
        for i in kernel_count:
            count=count+1
        return count - 1
    except:
        print("Other error")
        pass



prerequisite()
#hip_clone_repo()
hip_clear_hipapi_outputfolder()
hip_run_apitests()
hip_print_testresults()
print("------------------------Output logs will be stored in: " + outputpath)
