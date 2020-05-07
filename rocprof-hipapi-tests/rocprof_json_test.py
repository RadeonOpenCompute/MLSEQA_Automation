import os, sys, re, itertools, subprocess
from subprocess import PIPE, run
from prettytable import PrettyTable



output_file = "/home/taccuser/json_test_case_1/rocprof_hcc_trace_test_case_1.json"

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




rocprof_json_function_validate()
#rocprof_json_file_validate()
#rocprof_json_time_parser()
