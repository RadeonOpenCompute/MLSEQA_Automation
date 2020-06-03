## Created by    : Rahul Mula
## Creation Date : 05/05/2020
## Description   : Scripts for JSON tracing
import os, sys, re, itertools, subprocess, json, logging
from subprocess import PIPE, run
from prettytable import PrettyTable
from datetime import datetime
import texttable as tt


#output_file = "/home/taccuser/json_test_case_1/rocprof_hcc_trace_test_case_1.json"
HOME = os.environ['HOME']
#output_file = "/rocprof_hcc_trace_test_case_1/rocprof_hcc_trace_test_case_1.json"
output_file = HOME + "/JSON_validate_file/result.json"
output_path = HOME + "/rocprof-json-output"
os.system("mkdir %s"%output_path)
print("output_path :%s"%output_path)
tab = tt.Texttable()
x = [[]]
results=[]
test_names = ["rocprof_json_validate_file_test_case_1",
        "rocprof_json_validate_timestamp_test_case_2",
        "rocprof_json_args_check_test_case_3",
        "rocprof_json_pid_check_test_case_4",
        "rocprof_json_kernel_test_case_5",         
        "rocprof_json_stream_test_case_6"
        ]


def rocprof_pid_checks(tstname,tstnum):    
    logger.info('Entered test: rocprof_json_pid_check_test_case_4')
    pidnames = {"CPU HIP API":"2",
            "COPY":"1",
            "GPU0":"6" }
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
        result=[]
        while i < count:          
          jsonpid = j['traceEvents'][i]['pid']
          pid = pidnames[j['traceEvents'][i]['args']['name']]          
         
          if int(jsonpid) == int(pid):
              print("Pass")
              result.append("Pass")
              #logger_pass(tstname, tstnum)
          else:
              print("Fail")      
              result.append("Fail")      
              #logger_fail(tstname, tstnum)
          i += 1                
        if "Fail" in result:
            logger_fail(tstname, tstnum)
        else:           
            logger_pass(tstname, tstnum)

    except:
        print("error in rocprof_pid_checks")
        logger.error("error in rocprof_pid_checks")
        logger.exception("error in rocprof_pid_checks")
        #print("Unexpected error:", sys.exc_info()[0])
        

def rocprof_json_stream_checks():
    logger.info('Entered test: rocprof_json_stream_test_case_6')
    try:
        #f = open(output_file,"r")
        #j = json.loads(f.read())
        #for i in j['traceEvents']:
            #print(i)
        with open(output_file, "r") as f:
            for line in f:
                if 'stream' in line:
                    #print(line)
                    m = re.search('stream(((.*)))', line).group(1)
                    #print(re.search('stream(((.*)))', line).group(1))
                    #str1 = str("nill")
                    if "nill" in m:
                        print("nill")   
                    else:
                        print("not nill")
                    #print(i)
                    #print(i.get('args', {}).get('args'))                       
   
    except:
        print("error in rocprof_stream_checks")


def rocprof_json_kernel_checks():
    logger.info('Entered test: rocprof_json_kernel_test_case_5')
    print("kernel")
    try:
        f = open(output_file,"r")
        j = json.loads(f.read())
        results = []
        print("Kernel")
        for i in j['traceEvents']:
            kernelname = i.get('name')
            #print(kernelname)            
            if kernelname == "hipModuleLaunchKernel":
                #print(kernelname)                
                print(i.get('args', {}).get('args'))
                if (i.get('args', {}).get('args')) == "Null":
                    results.append("Fail")
                else:
                    results.append("Pass")
        if "Fail" in results:
            logger_fail(tstname,tstnum)      
        else:
            logger_pass(tstname,tstnum)

    except:
        print("error in rocprof_kernel_checks")


def rocprof_check_args(tstname,tstnum):
    logger.info('Entered test: rocprof_json_args_check_test_case_3')
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
               #print("entered six")
               #print(i.get('args'))
               apiname = i.get('name')
               if i.get('args') == None:                   
                   #print("HIP API %s : Fail"%apiname)
                   result.append("Fail")
                   #logger.info('[HIP API] [%s] has no arguments: Fail'%(apiname))                  
               else:
                   #print("HIP API %s has arguments: Pass"%apiname)
                   result.append("Pass")         
       if "Fail" in result:
           logger_fail(tstname,tstnum)
       else:
           logger_pass(tstname,tstnum)

    except:
       print("error in rocprof_json_check_args()")
       logger.error("error in rocprof_check_args")
       logger.exception("error in rocprof_check_args")

         
def load_defaults():
    global pt,tab,x,logger,start
    start=datetime.now()
    logger = logging.getLogger(__name__)
    #file_handler = logging.FileHandler('rdc_test.log')
    logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d :%(message)s',
            datefmt ='%Y-%m-%d %H:%M:%S',
            filename = './rocprof_jsontest.log',
            filemode ='w'
    )
    pt = PrettyTable()
    pt.field_names = ["S.no","Test_name","Status"]
    pt.align["Test_name"] = "l"
    pt.align["Status"] = "l"


def rocprof_json_file_validate(tstname,tstnum):
    logger.info('Entered test: rocprof_json_file_validate')
    try:
        count = 0
        with open(output_file, "r") as file:            
            for line in file:
                count = count + 1
            if count > 0:
                print("File_content_test : Pass")
                logger_pass(tstname, tstnum)
            else:
                print("File_content_test : Fail")
                logger_fail(tstname, tstnum)
    except:
        print("error in rocprof_json_file_validate")
        logger.error("error in rocprof_json_file_validate()")
        logger.exception("error in rocprof_json_file_validate()")


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


def rocprof_json_time_parser(tstname,tstnum):
    logger.info('Entered test: rocprof_json_validate_timestamp_test_case_2')
    try:
        beginNS_result=[]
        endNS_result=[]
        durationNS_result=[]
        result=[]
        with open(output_file, "r") as file:
            for line in file:
                if "BeginNs" in line:
                    beginNS_value = int(line.split(":")[1].replace('"','').replace(',',''))
                    if beginNS_value <= 0:
                        beginNS_result.append("Fail")
                        result.append("Fail")
                    else:
                        beginNS_result.append("Pass")
                        result.append("Pass")
                elif "EndNs" in line:
                    endNS_value = int(line.split(":")[1].replace('"','').replace(',',''))
                    if endNS_value <= 0:
                        endNS_result.append("Fail")
                        result.append("Fail")
                    else:
                        endNS_result.append("Pass")
                        result.append("Pass")
                elif "DurationNs" in line:
                    durationNS_value = int(line.split(":")[1].replace('"',''))
                    if durationNS_value <= 0:
                        durationNS_result.append("Fail")
                        result.append("Fail")
                    else:
                        durationNS_result.append("Pass")
                        result.append("Pass")

        if "Fail" in beginNS_result:
            print("BeginNs : Fail")
            logger.info('BeginNs: Fail')
        else:
            print("BeginNs : Pass")
            logger.info('BeginNs: Pass')

        if "Fail" in endNS_result:
            print("EndNs : Fail")
            logger.info('EndNs: Fail')
        else:
            print("EndNs : Pass")
            logger.info('EndNs: Pass')

        if "Fail" in durationNS_result:
            print("DurationNS: Fail")
            logger.info('DurationNS: Fail')
        else:
            print("DurationNS: Pass")
            logger.info('DurationNS: Pass')

        if "Fail" in result:
            logger_fail(tstname, tstnum)
        else:
            logger_pass(tstname, tstnum)

    except():
        print("error in rocprof_json_time_parser()")
        logger.error("error in rocprof_json_time_parser()")
        logger.exception("error in rocprof_json_time_parser()")


#def load_defaults():
    #global pt,tab,x,logger,start
    #start=datetime.now()
    #x = [[]]
    #results=[]
    #logger = logging.getLogger(__name__)
    ##file_handler = logging.FileHandler('rdc_test.log')
    #logging.basicConfig(
            #level=logging.DEBUG,
            #format='%(asctime)s.%(msecs)03d :%(message)s',
            #datefmt ='%Y-%m-%d %H:%M:%S',
            #filename = 'rocprof_jsontest.log',
            #filemode ='w'
    #)
    #pt = PrettyTable()
    #pt.field_names = ["S.no","Test_name","Status"]
    #pt.align["Test_name"] = "l"
    #pt.align["Status"] = "l"


def logger_pass(test_string,testnum):
    global x,pt
    try:        
        pt.add_row([testnum,test_string,"PASS"])
        logger.info('Run Test : %s'%test_string)
        #logger.error('Run Command : %s'%command)
        logger.info('Test: %s is Passed'%test_string)
        x.append([testnum,test_string,"PASS"])
        results.append("pass")
    except:
        print("error in logger_pass for %s"%test_string)



def logger_fail(test_string,testnum):
    
    try:        
        pt.add_row([testnum,test_string,"FAIL"])
        logger.info('Run Test : %s'%test_string)
        #logger.error('Run Command : %s'%command)
        logger.info('Test: %s is Failed'%test_string)
        logger.info('\n')
        x.append([testnum,test_string,"FAIL"])
        results.append("fail")
    except:
        print("error in logger_fail for %s"%test_string)



#def load_defaults():
    #global pt,tab,x
    #pt = PrettyTable()
    #pt.field_names = ["Test_name","Status"]
    #pt.align["Test_name"] = "l"
    #pt.align["Status"] = "l"
    #x = [[]]
    #results=[]
    #logger = logging.getLogger(__name__)
    ##file_handler = logging.FileHandler('rdc_test.log')
    #logging.basicConfig(
            #level=logging.DEBUG,
            #format='%(asctime)s.%(msecs)03d :%(message)s',
            #datefmt ='%Y-%m-%d %H:%M:%S',        
            #filename = 'rdc_test.log',
            #filemode ='w'


def json_run_tests():
    logger.info('Started running JSON trace test cases')
    try:
        testnum = 0
        for tstname in test_names:
            testnum = testnum + 1
            #command = test_commands[tstname]
            if tstname == "rocprof_json_validate_file_test_case_1":                
                rocprof_json_file_validate(tstname,testnum)                                                
            elif tstname == "rocprof_json_validate_timestamp_test_case_2":
                rocprof_json_time_parser(tstname,testnum)
            elif tstname == "rocprof_json_args_check_test_case_3":
                rocprof_check_args(tstname,testnum)   
            elif tstname == "rocprof_json_pid_check_test_case_4":
                rocprof_pid_checks(tstname,testnum)  
            elif tstname == "rocprof_json_kernel_test_case_5":
                print("kernel start") 
                rocprof_json_kernel_checks(tstname,testnum)
                
                print("Hello1")
            #elif tstname == "rocprof_json_stream_test_case_6":
                #rocprof_json_stream_checks(tstname,testnum)
                       
        tab.add_rows(x)
        tab.set_cols_align(['r','r','r'])
        tab.header(['S.no', 'JSON-TestCases', 'Result'])
        print(tab.draw())
    except:
        print("error in json_run_tests")


def main():
    start = datetime.now()
    logging.info("starting test suite")
    load_defaults()
    json_run_tests()
    end = datetime.now()-start
    endtime = end.total_seconds() / 60




if __name__ == '__main__':
    main()



#load_defaults()
#rocprof_json_function_validate()
#rocprof_json_file_validate()
#rocprof_json_time_parser()
#rocprof_check_args()
#rocprof_pid_checks()
#rocprof_kernel_checks()
#rocprof_stream_checks()
