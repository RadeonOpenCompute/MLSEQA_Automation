import os, sys, re, itertools, subprocess, shutil
import os.path
import texttable as tt


HOME = os.environ['HOME']
hip_gitpath = "https://github.com/ROCm-Developer-Tools/HIP.git"
#kernel_count = []
newlist = []
tab = tt.Texttable()
x = [[]]

def prerequisite():
    os.popen("sudo apt-get install git")    
    if os.path.exists("%s/HIP" %HOME):        
        shutil.rmtree("%s/HIP" %HOME)


def hip_clone_repo():
    os.system("cd %s && git clone %s" %(HOME,hip_gitpath))
    os.system("cd %s/HIP && mkdir build" %HOME)
    os.system("cd %s/HIP/build && cmake .. -DCMAKE_INSTALL_PREFIX=$PWD/install && sudo make -j16" %HOME)
    os.system("cd %s/HIP/build && sudo make install && make check" %HOME)


def hip_clear_hipapi_testFolder():
    shutil.rmtree('~/rocprof_automation_test_cases', ignore_errors=True)
   

   
def hip_run_apitests():
    list_dir = []
    root_dir = "/home/taccuser/HIP/build/directed_tests/"
    # create a list of file and sub directories 
    
    #listOfFile = os.listdir(root_dir)
    testpath = r'/home/taccuser/HIP/build/directed_tests/'
    csvpath = "~/rocprof_automation_test_cases/"


    for (path, dirs, files) in os.walk(testpath):
        #print(path)

        #for d in dirs:
            #print(d)
        
        for f in files:
            hip_apitests = os.path.join(path, f)
            #print(os.path.join(path, f))
            os.system("/opt/rocm/bin/rocprof -d %s -o %s%s_test_case.csv %s" %(csvpath,csvpath,f,hip_apitests))
            
        
        src_path = path.split("/")
        print(src_path)


def hip_print_testresults():

    testpath = r'/home/taccuser/HIP/build/directed_tests/'
    csvdir = "/home/taccuser/rocprof_automation_test_cases/"
    kernel_count = []
    count = 0
    for (path, dirs, files) in os.walk(testpath):
        #print(path)

        #for d in dirs:
            #print(d)        
        for f in files:
            hip_apitests = os.path.join(path, f)
            #print(os.path.join(path, f))
            csvfile = csvdir + f + "_test_case.csv"
            #hip_get_csvkernel_count(csvfile)
            directedpath= path + "/" + f
            cpppath = directedpath.replace("//", "/")
            count = count + 1
            #print(cpppath)
            print(count)
            print("CPP path: " + str(hip_get_cpppath(cpppath)))
            print("CSV path: " + str(csvfile))
            print("CSV kernel count: " + str(hip_get_csvkernel_count(csvfile)))
            print("CPP kernel count: " + str(hip_get_cppkernel_count(hip_get_cpppath(cpppath))))
            if hip_get_csvkernel_count(csvfile) == hip_get_cppkernel_count(hip_get_cpppath(cpppath)):
                x.append([count,str("rocprof_hipapi_" + f + "test_case_" + str(count)),"Pass"])
            else:
                x.append([count,str("rocprof_hipapi_" + f + "test_case_" + str(count)),"Fail"])
            
    tab.add_rows(x)
    tab.set_cols_align(['r','r','r'])
    tab.header(['S.no', 'ROCProf-HIPApi-TestCase Names', 'Result'])
    print(tab.draw())

            #os.system("/opt/rocm/bin/rocprof -d %s -o %s%s_test_case.csv %s" %(csvpath,csvpath,f,hip_apitests))


def hip_get_cpppath(path):
    #csvout = "~/rocprof_automation_test_cases/hip_trig_test_case.csv"
    
    #path = "/home/taccuser/HIP/tests/src/deviceLib/hip_trig.cpp"
    #print(path)
    src_path = path.split("/")
    len_srcpath = len(src_path)
    #print(len_srcpath)
    if len_srcpath == 8:        
        source_path = "/" + src_path[1] + "/" + src_path[2] + "/" + src_path[3] + "/tests/src/" + src_path[6] + "/" + src_path[7]
        #print(source_path)
        return hip_check_fileexists(source_path)
        #return source_path
    elif len_srcpath == 7:
        source_path = "/" + src_path[1] + "/" + src_path[2] + "/" + src_path[3] + "/tests/src/" + src_path[6]
        #print(source_path)
        return hip_check_fileexists(source_path)
        #return source_path
    elif len_srcpath == 9:
        source_path = "/" + src_path[1] + "/" + src_path[2] + "/" + src_path[3] + "/tests/src/" + src_path[6] + "/" + src_path[7] + "/" + src_path[8]
        #print(source_path)
        return hip_check_fileexists(source_path)
        #return source_path


def hip_check_fileexists(path):
    cpppath = path + ".cpp"
    cpath = path + ".c"
    if os.path.isfile(cpppath):
        return cpppath
    elif os.path.isfile(cpath):
        return cpath
    else:
        print ("File not exist")




def hip_get_cppkernel_count(path):
    #path = "/home/taccuser/HIP/tests/src/Functional/device/hipFuncGetDevice.cpp" 
    kernel_count = []
    try: 
        with open(path, "r") as fp:
            for line in fp:
                if "hipLaunchKernel" in line:
                    #generate_lines_that_equal("hipLaunchKernel", fp):
                    kernel_count.append(line)
        #print(kernel_count)
        #print(len(kernel_count.splitlines(  )))
        count=0
        for i in kernel_count:
            count=count+1
            #print(i)
            #newlist.append(i.split('\n')[0])
        #print(newlist)
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
    with open(csvfile, "r") as fp:
        for line in fp:
            #if "hipLaunchKernel" in line:
                #generate_lines_that_equal("hipLaunchKernel", fp):
            kernel_count.append(line)
    #print(kernel_count)
    #print(len(kernel_count.splitlines(  )))
    count=0
    for i in kernel_count:
        count=count+1
    return count - 1
        #print(i)
        #newlist.append(i.split('\n')[0])
    #print(newlist)
    #print(count)



#hip_clear_hipapi_testFolder()
#hip_clone_repo()
#hip_run_apitests()
#hip_print_testresults()
#hip_get_cpppath()
#hip_get_cppkernel_count()
#hip_get_csvkernel_count()
hip_print_testresults()



#prerequisite()
#hip_clone_repo()
#getListOfFiles()
