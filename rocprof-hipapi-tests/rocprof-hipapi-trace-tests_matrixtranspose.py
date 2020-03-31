import os, sys, re, itertools, subprocess, shutil, json
import os.path
import texttable as tt
from pathlib import Path


HOME = os.environ['HOME']
conf_path= "./conf.json"
testpath = "/opt/rocm/hip/samples/2_Cookbook/0_MatrixTranspose/MatrixTranspose"
outputpath = "%s/rocprofiler_hipapi_trace_automation_test_cases/" %HOME
testcase = "MatrixTranspose"
testnum = "2"
outputdir = outputpath + "rocprofiler_component_build/"
cppapis = []

def hip_clear_hipapi_outputfolder():
    if os.path.exists("%s" %outputpath):
       shutil.rmtree(outputpath, ignore_errors=True)


def hip_load_conf(var):
    config = json.loads(open(conf_path).read())
    return config["%s" %var]


def hip_get_cpp_data():
    cpppath = "/opt/rocm/hip/samples/2_Cookbook/0_MatrixTranspose/MatrixTranspose.cpp"
    apis = hip_load_conf("hip_apis")
    with open(cpppath, "r") as file:
        for line in file:
            for i in apis:
                for match in re.finditer(i, line, re.S):
                    if match:
                        print(i)
                        cppapis.append(i)
    print(cppapis)

def hip_get_trace_data():
    hip_clear_hipapi_outputfolder()
    os.system("/opt/rocm/bin/rocprof --hip-trace -d %s -o %s/%s_test_case_%s.csv %s" %(outputdir,outputdir,testcase,testnum,testpath))

    inputdir = []
    rplfolder = ""
    for (path, dirs, files) in os.walk(outputdir):
        print(dirs)
        #os.path.join(outputdir, )
        inputdir.append(dirs)
    rpldata = os.path.join(outputdir, str(", ".join(inputdir[0])))
    hiptrace_dir = os.path.join(rpldata, str(", ".join(inputdir[1])))
    hiptrace_file = hiptrace_dir + "/hip_api_trace.txt"
    apis = hip_load_conf("hip_apis")
    print(apis[0])
    print(hiptrace_file)
    with open(hiptrace_file, "r") as file:
        for line in file:
            for i in apis:
                for match in re.finditer(i, line, re.S):
                    if match:
                        print(i)




hip_clear_hipapi_outputfolder()
hip_get_cpp_data()
hip_get_trace_data()

