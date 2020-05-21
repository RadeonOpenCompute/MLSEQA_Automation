import os, sys, re, itertools, subprocess, json, logging
from subprocess import PIPE, run
from prettytable import PrettyTable

#import dpath.util
#import pandas as pd


#output_file = "/home/taccuser/json_test_case_1/rocprof_hcc_trace_test_case_1.json"
HOME = os.environ['HOME']
output_file = "/rocprof_hcc_trace_test_case_1/rocprof_hcc_trace_test_case_2.json"
output_path = HOME + "/rocprof-json-output"



def rocprof_pid_checks():    
    pidnames = {"0 CPU HIP API":"2",
            "1 COPY":"1",
            "2 GPU0":"6" }
    try:
        count = 1
        with open(output_file, "r") as f:
            for line in f:                
                if '"ph":"M"' in line:
                    print("found args")
                    count = count + 1
        print(count)
        f = open(output_file,"r")       
        j = json.loads(f.read())
        i = 1
        while i < count:          
          jsonpid = j['traceEvents'][i]['pid']
          pid = pidnames[j['traceEvents'][i]['args']['name']]          
         
          if int(jsonpid) == int(pid):
              print("Pass")
          else:
              print("Fail")            
          i += 1                
    except:
        print("error in rocprof_pid_checks")


def rocprof_stream_checks():
    try:
        f = open(output_file,"r")
        j = json.loads(f.read())
        for i in j['traceEvents']:
            print(i)
            if 'stream' in i:
                print(i)
                print(i.get('args', {}).get('args'))                       
   
    except:
        print("error in rocprof_stream_checks")


def rocprof_kernel_checks():
    try:
        f = open(output_file,"r")
        j = json.loads(f.read())
        for i in j['traceEvents']:
            kernelname = i.get('name')
            #print(kernelname)
            if kernelname == "hipModuleLaunchKernel":
                print(kernelname)
                print(i.get('args', {}).get('args'))
               
    except:
        print("error in rocprof_kernel_checks")


def rocprof_check_args():
    try:
       result = []       
       #phstr = '"ph":"X"'
       f = open(output_file,"r")      
       j = json.loads(f.read())              
       for i in j['traceEvents']:                       
           pid = i.get('pid')
           if pid == None:
               continue
           elif pid == 0:
               print("entered six")
               print(i.get('args'))
               apiname = i.get('name')
               if i.get('args') == None:                   
                   print("HIP API %s : Fail"%apiname)
                   result.append("Fail")
                   logger.info('[HIP API] [%s] has no arguments: Fail'%(apiname))                  
               else:
                   print("HIP API %s has arguments: Pass"%apiname)
                   result.append("Pass")         

    except:
       print("error in rocprof_json_check_args()")
   
         
def load_defaults():
    global pt,tab,x,logger,start
    start=datetime.now()
    logger = logging.getLogger(__name__)
    #file_handler = logging.FileHandler('rdc_test.log')
    logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d :%(message)s',
            datefmt ='%Y-%m-%d %H:%M:%S',
            filename = output_path + '/rocprof_jsontest.log',
            filemode ='w'
    )
    pt = PrettyTable()
    pt.field_names = ["S.no","Test_name","Status"]
    pt.align["Test_name"] = "l"
    pt.align["Status"] = "l"


def rocprof_json_file_validate():
    try:
        count = 0
        with open(output_file, "r") as file:            
            for line in file:
                count = count + 1
            if count > 0:
                print("File_content_test : Pass")
            else:
                print("File_content_test : Fail")
    except:
        print("error in rocprof_json_file_validate")



def rocprof_json_function_validate():
    try:
        cpu=0
        copy=0
        gpu=0
        with open(output_file, "r") as file:
            for line in file:
                if '{"name' in line:
                    if "CPU HIP API" in line:                        
                        cpu = cpu + 1
                    elif "COPY" in line:                        
                        copy = copy + 1
                    elif "GPU0" in line:
                        gpu = gpu + 1
            if cpu > 0 and copy > 0 and gpu > 0:
                print("Json_function_validate : Pass")
            else:
                print("Json_function_validate : Fail")
    except:
        print("error in rocprof_json_function_validate")


def rocprof_json_time_parser():
    try:
        beginNS_result=[]
        endNS_result=[]
        durationNS_result=[]
        with open(output_file, "r") as file:
            for line in file:
                if "BeginNs" in line:
                    beginNS_value = int(line.split(":")[1].replace('"','').replace(',',''))
                    if beginNS_value <= 0:
                        beginNS_result.append("Fail")
                    else:
                        beginNS_result.append("Pass")
                elif "EndNs" in line:
                    endNS_value = int(line.split(":")[1].replace('"','').replace(',',''))
                    if endNS_value <= 0:
                        endNS_result.append("Fail")
                    else:
                        endNS_result.append("Pass")
                elif "DurationNs" in line:
                    durationNS_value = int(line.split(":")[1].replace('"',''))
                    if durationNS_value <= 0:
                        durationNS_result.append("Fail")
                    else:
                        durationNS_result.append("Pass")

        if "Fail" in beginNS_result:
            print("BeginNs : Fail")
        else:
            print("BeginNs : Pass")

        if "Fail" in endNS_result:
            print("EndNs : Fail")
        else:
            print("EndNs : Pass")

        if "Fail" in durationNS_result:
            print("DurationNS : Fail")
        else:
            print("DurationNS : Pass")

    except():
        print("error in rocprof_json_time_parser()")



#load_defaults()
#rocprof_json_function_validate()
#rocprof_json_file_validate()
#rocprof_json_time_parser()
#rocprof_check_args()
#rocprof_pid_checks()
#rocprof_kernel_checks()
rocprof_stream_checks()
