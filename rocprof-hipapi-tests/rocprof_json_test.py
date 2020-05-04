import os, sys, re, itertools, subprocess
from subprocess import PIPE, run
from prettytable import PrettyTable



output_file = "/home/taccuser/json_test_case_1/rocprof_hcc_trace_test_case_1.json"


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
                if "EndNs" in line:
                    endNS_value = int(line.split(":")[1].replace('"','').replace(',',''))
                    if endNS_value <= 0:
                        endNS_result.append("Fail")
                    else:
                        endNS_result.append("Pass")
                if "DurationNs" in line:
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






rocprof_json_time_parser()
