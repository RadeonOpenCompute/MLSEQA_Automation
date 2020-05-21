## Created by    : Paresh Patel
## Creation Date : 20/12/2018
## Description   : Script for Testing rocprofiler with HIP APP
import subprocess as sp
import os
import sys
if sys.version_info >= (3,0):
    os.system('echo AH64_uh1 | sudo -S pip3 install prettytable')
else:
    os.system('echo AH64_uh1 | sudo -S pip install prettytable')
if os.path.exists("/etc/centos-release"):
    os.system('echo AH64_uh1 | sudo -S yum -y install cifs-utils --nogpgcheck')
else:
    os.system('echo AH64_uh1 | sudo -S apt-get install -y cifs-utils')
import sys
sys.path.append("..")
import re
import argparse
import subprocess
import random
import time
import logging
import inspect
from prettytable import PrettyTable
import csv
from datetime import datetime
from common import artifactorypath as Apath
from common.artifactorypath import Common as cm
from common.artifactorypath import FileInfo
auto = cm()
import common.upload_db as db
auto.Initialzation('rocprof_pytorch_tests')
HTML = '''
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 5px;
  text-align: left;    
}
</style>
</head>
'''
#os.system('rm -f rocprof_tests.log')

total_tests=0
failcount=0
passcount=0
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d :%(message)s',
        datefmt ='%Y-%m-%d %H:%M:%S',
        filename = FileInfo['logfile'],
        #filename='rocpro_test.log',
        filemode ='a+'
)
print( FileInfo['logfile'])

test_list=["rocprof_pyt_test_case_1",
           "rocprof_pyt_test_case_2",
           "rocprof_pyt_test_case_3",
           "rocprof_pyt_test_case_4",
           "rocprof_pyt_hip_api_test_case_1",
           "rocprof_pyt_hip_api_test_case_2",
           "rocprof_pyt_hip_api_mgpu_test_case_1"
]

commands = {
    "rocprof_pyt_test_case_1":'/opt/rocm/bin/rocprof --timestamp on --obj-tracking on -i $PWD/input.xml -d $PWD/rocprof_pyt_test_case_1 -o $PWD/rocprof_pyt_test_case_1.csv python3 micro_benchmarking_pytorch.py --network alexnet --batch-size 256 --iterations 1 --fp16 1',
    "rocprof_pyt_test_case_2":'/opt/rocm/bin/rocprof --timestamp off --obj-tracking on -i $PWD/input.xml -d $PWD/rocprof_pyt_test_case_2 -o $PWD/rocprof_pyt_test_case_2.csv python3 micro_benchmarking_pytorch.py --network alexnet --batch-size 256 --iterations 1 --fp16 1',
    "rocprof_pyt_test_case_3":'/opt/rocm/bin/rocprof --basenames on --obj-tracking on -i $PWD/input.xml -d $PWD/rocprof_pyt_test_case_3 -o $PWD/rocprof_pyt_test_case_3.csv python3 micro_benchmarking_pytorch.py --network alexnet --batch-size 256 --iterations 1 --fp16 1',
    "rocprof_pyt_test_case_4":'/opt/rocm/bin/rocprof --basenames off --obj-tracking on -i $PWD/input.xml -d $PWD/rocprof_pyt_test_case_4 -o $PWD/rocprof_pyt_test_case_4.csv python3 micro_benchmarking_pytorch.py --network alexnet --batch-size 256 --iterations 1 --fp16 1',
    "rocprof_pyt_hip_api_test_case_1":'/opt/rocm/bin/rocprof  --hip-trace  --obj-tracking on -i $PWD/input_hip.xml -d $PWD/rocprof_pyt_hip_api_test_case_1 -o $PWD/rocprof_pyt_hip_api_test_case_1/rocprof_pyt_hip_api_test_case_1.csv python3 micro_benchmarking_pytorch.py --network alexnet --batch-size 256 --iterations 1 --fp16 1',
    "rocprof_pyt_hip_api_test_case_2":'/opt/rocm/bin/rocprof  --hip-trace --obj-tracking on -d $PWD/rocprof_pyt_hip_api_test_case_2 -o $PWD/rocprof_pyt_hip_api_test_case_2/rocprof_pyt_hip_api_test_case_2.csv  python3 micro_benchmarking_pytorch.py --network alexnet --batch-size 256 --iterations 1 --fp16 1',
    "rocprof_pyt_hip_api_mgpu_test_case_1":'/opt/rocm/bin/rocprof  --hip-trace --obj-tracking on -d $PWD/rocprof_pyt_hip_api_mgpu_test_case_1 -o $PWD/rocprof_pyt_hip_api_mgpu_test_case_1/rocprof_pyt_hip_api_mgpu_test_case_1.csv python3 micro_benchmarking_pytorch.py --data_parallel --network alexnet --batch-size 256 --iterations 1 --fp16 1',
            }

def print_test_list_help(listname):
    logger.info('Entering %s'%(inspect.stack()[0][3])[:-4].upper())
    test_list=""
    indexval = 0
    try:
        for i in range(len(listname)):
           test_list += "%d.%s    "%(i+1,listname[indexval])
           indexval = indexval + 1
        return test_list
    except IndexError:
        print('That index value you gave is out of range.')
    logger.info('Exiting %s'%(inspect.stack()[0][3])[:-4].upper())


def hip_trace_validation():
    hip_stats = False
    if os.path.exists('%s/%s/%s.hip_stats.csv'%(cwd,test_string,test_string)):
        try:
            with open('%s/%s/%s.hip_stats.csv'%(cwd,test_string,test_string), mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                count = 0
                for row in csv_reader:
                    if line_count == 0:
                        #print('Column names are',','.join(row))
                        line_count += 1
                    #print(row["Name"])
                    searchObj = re.search(r'hip', row["Name"], re.I)
                    if searchObj:
                        count += 1
                    else:
                        logger.error('HIP api File validation failed for Test : %s'%test_string)
                        return False
                    line_count += 1
                #print('Processed line_count is %s lines.'%line_count)
                logger.info('Processed line_count is %s lines.'%line_count)
                logger.info('Processed count is %s lines.'%count)
            if line_count == 29 and  count == 28:
                hip_stats = True
            else:
                logger.error('HIP api validation failed for hip_stats file for Test : %s'%test_string)
                hip_stats =  False
        except:
            logger.error('HIP api hip_stats File open/validation failed for Test : %s'%test_string)
            hip_stats =  False
    else:
        logger.error('HIP api hip_stats file not found for Test : %s'%test_string)
        return False
    # Validation of hip_api_trace.txt
    hip_api_stats = False
    for root, dirs, files in os.walk("%s/%s"%(cwd,test_string)):
        for file in files:
            #print('file',file)
            if file == "hip_api_trace.txt":
                #print(os.path.join(root, file))
                hip_file = os.path.join(root, file)
                #print('hip_file',hip_file)
                try:
                    with open(hip_file) as trace_file:
                        first = trace_file.read(1)
                        if not first:
                            #print('First')
                            logger.error('hip_api_trace File generated but empty for Test : %s'%test_string)
                            return False
                        hip_api_count = 0
                        for line in trace_file:
                            print('Opening hip_api_trace.txt 13')
                            searchObj = re.search(r'hip', line, re.I)
                            if searchObj:
                                hip_api_count += 1
                        logger.info('hip_api_count is %s '%hip_api_count)
                        if hip_api_count > 10900:
                            hip_api_stats = True
                        else:
                            logger.error('hip_api_trace File hip_api_count failed for Test : %s'%test_string)
                            hip_api_stats = False
                except:
                    logger.error('hip_api_trace File open/validation failed for Test : %s'%test_string)
                break
    hc_ops_val = False
    hc_ops_api_list = ['hcCommandKernel', 'hcMemcpyHostToDevice', 'hcMemcpyDeviceToHost', 'hcMemcpyDeviceToDevice']
    for root, dirs, files in os.walk("%s/%s"%(cwd,test_string)):
        for file in files:
            #print('file',file)
            if file == "hcc_ops_trace.txt":
                #print(os.path.join(root, file))
                hc_ops_file = os.path.join(root, file)
                print('hc_ops_file',hc_ops_file)
                try:
                    hc_ops_count = 0
                    with open(hc_ops_file) as trace_file:
                       first = trace_file.read(1)
                       if not first:
                           logger.error('hcc_ops File generated but empty for Test : %s'%test_string)
                           hc_ops_val = False
                       i = 0
                       for val_str in hc_ops_api_list:
                           for line in trace_file:
                               searchObj = re.search(r'%s'%hc_ops_api_list[i], line, re.I)
                               if searchObj:
                                   hc_ops_count += 1
                                   break
                           i += 1
                       logger.info("hc_ops_count is %d"%hc_ops_count)
                       if hc_ops_count == 1249:
                            hc_ops_val = True
                       else:
                            logger.error('hcc_ops_trace File hc_ops_count failed for Test : %s'%test_string)
                            hc_ops_val = False
                except:
                    logger.error('hcc_ops_trace File open/validation failed for Test : %s'%test_string)
                    hc_ops_val = False
                break
    if hip_stats and hip_api_stats and hc_ops_val:
        return True
    else:
        logger.error('HIP api validation failed either for hip_stats/hip_api_stats/hcc_ops_trace for Test : %s'%test_string)
        return False


def hip_perf_validation():
    global test_string, command
    kernel_count = timestamp_val = time_val = False
    timensd = timensb = timensc = timense = 0
    if re.search(r'--timestamp on', command, re.I):
        timestamp_val = True
    if os.path.exists('%s/%s.csv'%(cwd,test_string)):
        try:
            with open('%s/%s.csv'%(cwd,test_string), mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                count = 0
                for row in csv_reader:
                    if line_count == 0:
                        #print('Column names are',','.join(row))
                        line_count += 1
                    #print(row["Name"])
                    
                    count = int(row["Index"])
                    if timestamp_val: 
                        try:
                            timensd =  int(row["DispatchNs"])
                            timensb =  int(row["BeginNs"])
                            timense =  int(row["EndNs"])
                            timensc =  int(row["CompleteNs"])
                            #print('timensd timensb timense timensc', timensd, timensb, timense, timensc)
                            if timensd and timensb and timense and timensc:
                                time_val = True
                            else:
                                logger.error('hip perf validation failed for Test : %s for timestamp'%test_string)
                                time_val = False
                                break
                        except:
                            logger.error('hip perf validation failed for Test : %s for timestamp except'%test_string)
                            time_val = False
                            break
                    line_count += 1
                #print('Processed line_count is %s lines.'%line_count)
                logger.info('Processed line_count is %s lines.'%line_count)
                logger.info('Processed count is %s .'%count)
            if count == 1196:
                kernel_count = True
            else:
                logger.error('hip perf validation failed for Test : %s for count'%test_string)
                kernel_count = False
        except:
            logger.error('hip perf validation failed for Test : %s for except'%test_string)
            kernel_count =  False
    #print("count",count)
    if timestamp_val:
        if kernel_count and time_val:
            return True
        else:
            return False
    else:
        if kernel_count:
            return True
        else:
            return False

def number_of_devices():
    nDev = 0
    p = subprocess.Popen('/opt/rocm/bin/rocm-smi -i', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    for line in p.stdout:
        if "GPU ID" in line.decode():
            nDev += 1
    #print('nDev',nDev)
    return nDev

def validate_file():
    logger.info('Entering %s'%(inspect.stack()[0][3]).upper())
    global test_string
    # HIP API tests parsing
    search_test = re.search("rocprof_pyt_hip_api",test_string, re.M)
    if search_test:
        if not hip_trace_validation():
            logger.error('HIP API File validation failed for Test : %s'%test_string)
            return False
    # HIP perf cponter tests parsing
    search_test = re.search("rocprof_pyt_test_case",test_string, re.M)
    if search_test:
        if not hip_perf_validation():
            logger.error('counters generated but contains wrong information for : %s'%test_string)
            return False
    logger.info('Exiting %s'%(inspect.stack()[0][3]).upper())
    return True

def validate_output(p,logger):
    ret = 1
    for line in p.stdout:
        if ret == 1:
            searchObj = re.search(r'\bUnable\b|\bError\b|\bFail\b|\bfailed\b|\bSegmentation\b',\
            line.decode(), re.I)
            if not searchObj:
                logger.info('%s'%line.decode())
                ret = 1
            else:
                ret = 0
                logger.error('%s'%line.decode())
        else:
            searchObj = re.search(r'\bUnable\b|\bError\b|\bFail\b|\bfailed\b|\bSegmentation\b',\
            line.decode(), re.I)
            if not searchObj:
                logger.info('%s'%line.decode())
            else:
                logger.error('%s'%line.decode())
    for line in p.stderr:
        if ret == 1:
            searchObj = re.search(r'\bUnable\b|\bError\b|\bFail\b|\bfailed\b|\bSegmentation\b',\
            line.decode(), re.I)
            if not searchObj:
                logger.info('%s'%line.decode())
                ret = 1
            else:
                ret = 0
                logger.error('%s'%line.decode())
        else:
            searchObj = re.search(r'\bUnable\b|\bError\b|\bFail\b|\bfailed\b|\bSegmentation\b',\
            line.decode(), re.I)
            if not searchObj:
                logger.info('%s'%line.decode())
            else:
                logger.error('%s'%line.decode())
    return ret

def rocprof_run_tests(test):
    logger.info('Entering %s'%inspect.stack()[0][3])
    ##print test.tests
    t_iter=0
    global test_string,steps,pt,command
    searchObj = None
    #print len(test.tests)
    try:
        for t_iter in range (len(test.tests)):
            err_str = False
            test_string="%s"%test.tests[t_iter]
            command="%s"%(commands[test_string])
            print('Running Test : %s\n Cmd : %s \n'%(test_string,command))
            p = subprocess.Popen('%s'%command, shell=True, stdout=subprocess.PIPE,\
                    stderr=subprocess.PIPE)
            p.wait()
            steps = steps + 1
            logger.info('Run Test : %s'%test_string)
            logger.info('Run Command : %s'%command)

            if validate_output(p,logger) and validate_file():
                #print "searchObj.group() : ", searchObj;
                fo.write("\n[STEP_%.3d]\nDescription=%s\nStatus=Passed\n"\
                %(steps,test_string))
                pt.add_row([test_string,"PASS"])
                logger.info('\n')
            else:
                fo.write("\n[STEP_%.3d]\nDescription=%s\nStatus=Failed\n"\
                %(steps,test_string))
                pt.add_row([test_string,"FAIL"])
                #logger.error('Run Command : %s'%test_string)
                #logger.error('Run Command : %s'%command)
                logger.info('\n')
    except subprocess.CalledProcessError:
        logger.error('Test execution failed for %s'%test_string)
    logger.info('Exiting %s'%inspect.stack()[0][3])

def roctracer_test():
    if not os.path.isdir("./roctracer"):
        os.system("git clone -b amd-master https://github.com/ROCm-Developer-Tools/roctracer")
    else:
        logger.info("removing old roctracer")
        os.system("rm -rf roctracer")
        os.system("git clone -b amd-master https://github.com/ROCm-Developer-Tools/roctracer")
    os.system("pip3 install CppHeaderParser")
    os.system("pip3 install argparse")
    os.chdir("%s/roctracer" %cwd)
    os.environ['HIP_PATH']='/opt/rocm/hip'
    os.environ['HCC_HOME']='/opt/rocm/hcc'
    os.environ['CMAKE_PREFIX_PATH']='/opt/rocm'
    os.environ['CMAKE_BUILD_TYPE']='release'
    os.system('mkdir build')
    os.chdir('build')
    os.system("cmake -DCMAKE_INSTALL_PREFIX=/opt/rocm .. 2>&1 | tee %s/roctracer.log"%(cwd))
    os.system("make -j 16  2>&1 | tee %s/roctracer.log"%(cwd))
    os.chdir("%s" %cwd)
    p = subprocess.Popen('%s/roctracer/build/run.sh'%cwd, shell=True, stdout=subprocess.PIPE,\
                    stderr=subprocess.PIPE)
    p.wait()
    test_string = 'roctracer_test'
    global steps
    steps = steps + 1
    if validate_output(p,logger):
        #fo.write("\n[STEP_%.3d]\nDescription=%s\nStatus=Passed\n"\
        #%(steps,test_string))
        pt.add_row([test_string,"PASS"])
        logger.info('\n')
    else:
        #fo.write("\n[STEP_%.3d]\nDescription=%s\nStatus=Failed\n"\
        #%(steps,test_string))
        pt.add_row([test_string,"FAIL"])
        logger.info('\n')
    os.chdir("%s" %cwd)


def copy_pyt_bench_files():
    logger.info('Entering %s'%inspect.stack()[0][3])
    global cwd
    os.system('wget https://raw.githubusercontent.com/wiki/ROCmSoftwarePlatform/pytorch/micro_benchmarking_pytorch.py')
    os.system('wget https://raw.githubusercontent.com/wiki/ROCmSoftwarePlatform/pytorch/fp16util.py')
    os.system('wget https://raw.githubusercontent.com/wiki/ROCmSoftwarePlatform/pytorch/shufflenet_v2.py')
    os.system('wget https://raw.githubusercontent.com/wiki/ROCmSoftwarePlatform/pytorch/shufflenet.py')

    if not os.path.exists('%s/micro_benchmarking_pytorch.py'%cwd):
        logger.error('micro_benchmarking_pytorch.py copy failed so can not proceed')
        logger.info('Exiting %s'%inspect.stack()[0][3])
        return False
    if not os.path.exists('%s/fp16util.py'%cwd):
        logger.error('fp16util.py copy failed so can not proceed')
        logger.info('Exiting %s'%inspect.stack()[0][3])
        return False
    if not os.path.exists('%s/shufflenet_v2.py'%cwd):
        logger.error('shufflenet_v2.py copy failed so can not proceed')
        logger.info('Exiting %s'%inspect.stack()[0][3])
        return False
    if not os.path.exists('%s/shufflenet.py'%cwd):
        logger.error('shufflenet.py copy failed so can not proceed')
        logger.info('Exiting %s'%inspect.stack()[0][3])
        return False

    os.system('pip3 install torchvision')
    return True

def parse_args():
    ap=argparse.ArgumentParser()
    ap.add_argument("-m", "--mail", nargs='?', default=None, const='0')
    ap.add_argument("-s", "--save",action="store_true",
                    help="Store the logs & summary files in artifactory")
    ap.add_argument(
        '-t',
        '--tests',
        nargs='+',
        #required=True,
        choices=test_list,
        default=test_list,
        metavar='',
        help="Select Test from    %s"%print_test_list_help(test_list))
    return ap.parse_args()

def set_test_defaults():
    global fo, cwd, steps, i, ext, pt, logger
    cwd=os.getcwd()
    os.system("rm -rf Results.ini")
    #os.system("rm -rf rocprof_pyt_test_case*")
    #os.system("rm -rf rocprof_pyt_hip_api*")
    #os.system("results.sh")
    fo=open("Results.ini","a+")
    steps=0
    i=1
    ext="log"
    pt = PrettyTable()
    pt.field_names = ["Test_name","Status"]
    pt.align["Test_name"] = "l"
    pt.align["Status"] = "l"


def rocprofiler_build_check(in_tests):
    logger.info('Entering %s'%(inspect.stack()[0][3]).upper())
    global steps
    #logger = logging.getLogger(__name__)
    logger.info('rocprofiler build check started')
    fo.write("[STEPS]\nNumber=%.3d\n"%(len(in_tests.tests)+1))
    platform = sp.check_output("awk -F= '/^NAME/{print $2}' /etc/os-release", shell=True)
    platform = platform.decode('utf-8')
    if os.path.exists("/etc/centos-release") or 'red Hat' in platform :
        p = subprocess.Popen('echo %s | sudo -S yum -y remove roctracer-dev.x86_64'%auto.password,\
            shell=True)
        p.wait() 
        p = subprocess.Popen('echo %s | sudo -S yum -y install roctracer-dev --nogpgcheck'%auto.password,\
            shell=True)
        p.wait() 
        p = subprocess.Popen('echo %s | sudo -S yum -y remove rocprofiler-dev.x86_64'%auto.password,\
            shell=True)
        p.wait() 
        p = subprocess.Popen('echo %s | sudo -S yum -y install rocprofiler-dev --nogpgcheck'%auto.password,\
            shell=True)
        p.wait() 
        p = subprocess.Popen('echo %s | sudo -S yum -y install rocblas --nogpgcheck'%auto.password,\
            shell=True)
        p.wait() 
    elif 'Ubuntu' in platform:
        p = subprocess.Popen('echo %s | sudo -S apt-get -y install roctracer-dev'%auto.password,\
            shell=True)
        p.wait() 
        p = subprocess.Popen('echo %s | sudo -S apt-get -y install rocprofiler-dev'%auto.password,\
            shell=True)
        p.wait() 
        p = subprocess.Popen('echo %s | sudo -S apt-get -y install rocblas'%auto.password,\
            shell=True)
        p.wait() 
    elif 'SLES' in platform:
        p = subprocess.Popen('echo %s | sudo -S zypper -y install roctracer-dev'%auto.password,\
            shell=True)
        p.wait()
        p = subprocess.Popen('echo %s | sudo -S zypper -y install rocprofiler-dev'%auto.password,\
            shell=True)
        p.wait()
        p = subprocess.Popen('echo %s | sudo -S zypper -y install rocblas'%auto.password,\
            shell=True)
        p.wait()
        os.environ["ROCP_PYTHON_VERSION"] = 'python3'


    #if not os.path.exists("/opt/rocm/rocprofiler/bin/rpl_run.sh"):
        os.system('git clone -b roc-2.10.x https://github.com/ROCm-Developer-Tools/rocprofiler.git')
        os.environ['CMAKE_PREFIX_PATH']='/opt/rocm/hsa/include/hsa:/opt/rocm/hsa/lib'
        os.environ['CMAKE_BUILD_TYPE']='release'
        os.environ['CMAKE_DEBUG_TRACE']='1'
        os.chdir('rocprofiler')
        os.system('mkdir build')
        os.chdir('build')
        os.system('cmake -DCMAKE_PREFIX_PATH=/opt/rocm/lib:/opt/rocm/include/hsa -DCMAKE_INSTALL_PREFIX=/opt/rocm ..')
        os.system('make')
        os.system('echo %s | sudo -S make install'%auto.password)
        os.chdir("%s"%cwd)

    # Below check is for if input files are available or not
    if not (os.path.exists("%s/input.xml"%cwd) and \
            os.path.exists("%s/input_hip.xml"%cwd) and \
            os.path.exists("%s/input_hsa.xml"%cwd)):
        logger.info('input.xml or input_hip.xml or input_hsa.xml not found')
        print('Exiting as input.xml or input_hip.xml or input_hsa.xml not found')
        exit()

    if os.path.exists("/opt/rocm/rocprofiler/bin/rpl_run.sh") and \
    os.path.exists("/opt/rocm/roctracer"):
        steps = steps + 1
        fo.write("\n[STEP_%.3d]\nDescription=rocprofiler build\nStatus=Passed\n"%steps)
        pt.add_row(["rocprofiler_roctracer_build","PASS"])
        logger.info('rocprofiler_roctracer_build Successful')
    else:
        steps = steps + 1
        fo.write("\n[STEP_%.3d]\nDescription=rocprofiler build\nStatus=Failed\n"%steps)
        pt.add_row(["rocprofiler_roctracer_build","FAIL"])
        logger.info('rocprofiler_roctracer_build Failed')
        print('Exiting as rocprofiler_roctracer_build Failed ')
        exit()
    os.environ["HCC_HOME"] = '/opt/rocm/hcc'
    logger.info('Exiting %s'%(inspect.stack()[0][3]).upper())

def write_summary(runtime,pt,fn,testname):
    sum_f = fn
    with open(sum_f,'a+') as summary:
        Line = ('=' * 70)
        summary.write('%s\nTest Execution time : %s\n%s' % (Line, runtime, Line))
        summary.write("\n%s test summary\n %s\n"%(testname,str(pt[0])))
        summary.write("\n%s test cases\n %s\n"%(testname,str(pt[1])))
        summary.write("System Information \n%s\n"%str(pt[2]))


def write_summary_html(runtime,pt,fn,testname):

    sum_f = fn
    with open(sum_f,'a+') as summary:
        summary.write(HTML)
        Line=('='*70)
        summary.write('<b>%s<br>Test Execution time : %s <br>%s</b>' % (Line, runtime, Line))
        summary.write("</br><b>%s test summary</b></br>"%testname)
        summary.write(pt[0].get_html_string())
        summary.write("</br><b>%s testcases </b></br>"%testname)
        summary.write(pt[1].get_html_string())
        summary.write("</br><b>System information</b></br>")
        summary.write(pt[2].get_html_string())

def Final_summary(pt):
    global total_tests
    global failcount
    global passcount
    Final=PrettyTable()
    Final.field_names=['Summary','Total','PASS','FAIL']
    for row in pt:
        row.border = False
        row.header = False
        Status=row.get_string(fields=["Status"]).strip()
        total_tests=total_tests+1
        if "FAIL" in Status:
            failcount=failcount+1
        elif 'PASS' in Status:
            passcount=passcount+1
    Final.add_row([' ',total_tests,passcount,failcount])
    return Final


commands1 = {
    "rocprof_pyt_sys_trace_mgpu_test_case_1":'HIP_VISIBLE_DEVICES=0,1,2,3 WORLD_SIZE=4 TEMP_DIR=/tmp BACKEND=nccl /opt/rocm/bin/rocprof -d $PWD/rocprof_pyt_sys_trace_mgpu_test_case_1 --sys-trace python3.6 $PWD/pytorch/test/test_distributed.py --verbose TestDistBackend.test_all_gather_multigpu'
}

def rocprof_run_systest():
    logger.info('Entering %s'%inspect.stack()[0][3])
    ##print test.tests
    t_iter=0
    global test_string,steps,pt,command
    searchObj = None
    test_string="rocprof_pyt_sys_trace_mgpu_test_case_1"
    output_path = "/rocprof_pyt_sys_trace_mgpu_test_case_1"
    #print len(test.tests)
    try:
       #for t_iter in range (len(test.tests)):
       err_str = False
       #test_string="%s"%test.tests[t_iter]
       command="%s"%(commands1[test_string])
       print('Running Test : %s\n Cmd : %s \n'%(test_string,command))
       p = subprocess.Popen('%s'%command, shell=True, stdout=subprocess.PIPE,\
               stderr=subprocess.PIPE)
       p.wait()
       steps = steps + 1
       logger.info('Run Test : %s'%test_string)
       logger.info('Run Command : %s'%command)

       print(output_path)
       inputdir = []
       for (path, dirs, files) in os.walk(output_path):
           print(dirs)
           inputdir.append(dirs)
       hsatrace_file = output_path + "/" + inputdir[0][0] + "/" + inputdir[1][0] + "/hsa_api_trace.txt"
       print(hsatrace_file)
       num_lines = 0
       with open(hsatrace_file, "r") as f:
           print("hsatrace_file")
           for line in f:
               num_lines += 1
       if num_lines > 1:
           #print "searchObj.group() : ", searchObj;
           fo.write("\n[STEP_%.3d]\nDescription=%s\nStatus=Passed\n"\
           %(steps,test_string))
           pt.add_row([test_string,"PASS"])
           logger.info('\n')
       else:
           fo.write("\n[STEP_%.3d]\nDescription=%s\nStatus=Failed\n"\
           %(steps,test_string))
           pt.add_row([test_string,"FAIL"])
           #logger.error('Run Command : %s'%test_string)
           #logger.error('Run Command : %s'%command)
           logger.info('\n')
    except:
        print("error in systrace_printresult")
        #logger.error('Test execution failed for %s'%test_string)
    #logger.info('Exiting %s'%inspect.stack()[0][3])


def main():
    mail=None
    versions = Apath.systeminfo()
    start = datetime.now()
    logging.info(versions)
    options = parse_args()
    #print("options %s"%options)
    set_test_defaults()
    rocprofiler_build_check(options)
    if not copy_pyt_bench_files():                                    
        print('copy_pyt_bench_files fails, first fix this.\n')
        exit()
    rocprof_run_tests(options)
    rocprof_run_systest()
    #roctracer_test()
    total = Final_summary(pt)
    print(pt)
    pretty = [total,pt,versions]
    end = datetime.now()-start
    endtime = end.total_seconds() / 60
    runtime = str(end).split('.')[0]
    write_summary(runtime,pretty,FileInfo['txt'],FileInfo['name'])
    write_summary_html(runtime,pretty,FileInfo['html'],FileInfo['name'])

    mail=options.mail
    if options.save == True:
        try:
            Apath.Auto_save(FileInfo['name'],FileInfo['logpath'])
            try:
                db.update_or_create('rocm_tools', 'rocprof_pytorch_tests', total_tests, passcount, failcount, endtime, start, Apath.Artifactory_path('rocprof_pytorch_tests'))
            except:
                print('db error')
        except:
            try:
                db.update_or_create('rocm_tools', 'rocprof_pytorch_tests', total_tests, passcount, failcount, endtime, start, "artifactory issue")
            except:
                print('db error')
    else:
        try:
            db.update_or_create('rocm_tools', 'rocprof_pytorch_tests', total_tests, passcount, failcount, endtime, start, " ")
        except:
            print('db error')
    if mail != None:
        Apath.autoMailer(FileInfo['name'],FileInfo['logpath'],mail)

    logger.info('Exiting main()')


if __name__ == '__main__':
    main()
