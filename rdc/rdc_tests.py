## Created by    : Rahul Mula
## Creation Date : 05/05/2020
## Description   : Script for RDC tool testing
import os, sys, re, itertools, subprocess, shutil, json, logging
import texttable as tt
from prettytable import PrettyTable
from datetime import datetime
import texttable as tt



if len(sys.argv) != 2:
    print('Please make sure you have entered Server IP, eg:python3 rdc_tests.py "10.130.166.204"')
    sys.exit(1)



fieldList = ['100', '101', '140', '150', '155', '200', '201', '203', '312', '313', '525']
fqdn = ""
HOME = os.environ['HOME']
grpid = 0
fgrpid = 0
rdcpath =  "/home/taccuser/rdc/build/"
tab = tt.Texttable()
x = [[]]
results=[]
logger = logging.getLogger(__name__)
#file_handler = logging.FileHandler('rdc_test.log')
logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d :%(message)s',
        datefmt ='%Y-%m-%d %H:%M:%S',        
        filename = 'rdc_test.log',
        filemode ='w'
)
test_names = ["rdc_service_start_test_1",
        "rdc_service_stop_test_2",
        "rdc_verify_rdc_daemon_test_3",
        "rdc_discover_gpu_test_4",
        "rdc_create_gpu_group_test_5",
        "rdc_list_gpu_group_test_6",        
        "rdc_attach_gpu_to_group_test_7",
        #"rdc_delete_gpu_group_test_8",
        "rdc_stats_job_create_test_8",
        "rdc_stats_job_stop_test_9",
        "rdc_stats_show_summary_test_10",
        "rdc_stats_validate_statsfield_test_11",
        "rdc_fieldgroup_create_test_12",
        "rdc_fieldgroup_list_test_13",
        "rdc_fieldgroup_viewinfo_test_14",
        "rdc_check_invalid_field_group_test_15"
        "rdc_monitor_telemetry_test_16",
        "rdc_fieldgroup_delete_test_17",
        #"rdc_monitor_telemetry_test_16",
        "rdc_delete_gpu_group_test_18",
        "rdc_connect_with_auth_test_19",
        "rdc_connect_without_auth_test_20",
        "rdc_check_supported_field_IDs_test_21",
        "rdc_monitor_device_with_field_IDs_test_22",
        "rdc_fieldgroup_with_invalid_fieldID_test_23",
        "rdc_singleinstance_clientserver_setup_test_24"
        ]


def fetch_fqdn():
    global fqdn
    try:
        res = execute_remotely("10.130.166.205","taccuser","AH64_uh1","nslookup 10.130.166.205")
        
        out = res.decode('utf-8')
        for item in out.split("\n"):
            if "name" in item:
                fqdn = item.split("=")[1].strip().replace("com.", "com")
    except:
        print("error in fetch_fqdn")


def rdc_monitor_device_with_field_IDs(tstname,tstnum):
    logger.info('Entered test: %s'%tstname)
    result = []
    try:        
        for i in fieldList:
            cmnd = "rdci dmon --host playground.amd.com:50051 -e %s -i 1 -c 5 -d 1000 -d 1"%i
            res = os.popen("%s"%cmnd).read()
            print(res)
            count = len(res.split('\n')) - 2
            if count == 5:
                result.append("Pass")
            elif count < 5:
                result.append("Fail")
        if "Fail" in result:
            print(tstname + ": Failed")
            logger_fail(tstname, cmnd, tstnum)
        elif len(result) == 0:
            print(tstname + ": Failed")
            logger_fail(tstname, cmnd, tstnum)
        else:
            print(tstname + ": Passed")
            logger_pass(tstname, cmnd, tstnum)
    except:
        logger.error("error in %s"%tstname)
        logger.exception("error in %s"%tstname)


def rdc_service_start(tstname,cmnd,test_string,tstnum):
    logger.info('Entered test: rdc_service_start_test_1')
    try:
        os.popen("%s"%cmnd).read()
        res = os.popen("sudo systemctl status rdc").read()        
        print(res)
        for item in res.split("\n"):
            if "Active:" in item:
                status = item.split("(")[0].split(":")[1].strip()
                print(status)
                if status == "failed":
                    logger_fail(tstname, cmnd, tstnum)
                elif status == "active":
                    logger_pass(tstname, cmnd, tstnum)

    except:
        logger.error("error in rdc_service_start")
        logger.exception("error in rdc_service_start")


def rdc_check_field_IDs(tstname,cmnd,test_string,tstnum):
    logger.info('Entered test: rdc_check_field_IDs_test')
    result = []
    try:
        res = os.popen("%s"%cmnd).read()
        if not "Supported fields Ids:" in res:
            result.append("Fail")
        elif "Supported fields Ids:" in res:
            fieldList = ['100', '101', '140', '150', '155', '200', '201', '203', '312', '313', '525']
            for i in fieldList:
                if i in res:
                    result.append("Pass")
                else:
                    result.append("Fail")
        if "Fail" in result:
            logger_fail(tstname, cmnd, tstnum)
        else:
            logger_pass(tstname, cmnd, tstnum)
    except:
        logger.error("error in rdc_check_field_IDs")
        logger.exception("error in rdc_check_field_IDs")
                    
        


def rdc_client_tests(tstname,cmnd,test_string,tstnum):
    global grpid, fgrpid
    logger.info('Entered test: %s'%tstname)
    try:      
        if "rdc_create_gpu_group_test_5" in tstname:
            res = os.popen("%s"%cmnd).read()
            logger.info('Result: %s'%res)
            print(res)
            print("entered rdc_create_gpu_group_test_5")
            if "Successfully created group" in res:
                logger.info('Entered to create group: %s'%tstname)
                print("entered : Successfully created group")
                grpid = res.split(" ")[-1].strip()
                logger.info('group id: %s'%grpid)                            

        elif "rdc_fieldgroup_create_test_12" in tstname:
            res = os.popen("%s"%cmnd).read()
            logger.info('Result: %s'%res)
            print(res)
            print("entered rdc_fieldgroup_create_test_12")
            if "Successfully created a field group" in res:
                logger.info('Entered to create field group: %s'%tstname)
                print("entered : %s"%tstname)
                fgrpid = res.split(" ")[-1].strip()
                logger.info('field group id: %s'%fgrpid)            

        else:
            res = os.popen("%s"%cmnd).read()        
            logger.info('Fetch env group id: %s'%grpid)
            logger.info('Result: %s'%res)
            print(res)
        matches = re.findall(test_string, str(res))
        print(len(matches))
        if len(matches) > 0:
            print("%s exist"%test_string)
            logger_pass(tstname,cmnd,tstnum)
        else:
            print("%s does not exist"%test_string)
            logger_fail(tstname,cmnd,tstnum)
    except:
        logger.error("error in rdc_service_start")
        logger.exception("error in rdc_service_start")



def rdc_stats_validate():
    result = []
    try:
        statField = ['Start Time','End Time','Total Execution Time']
        res = os.popen("%s"%cmnd).read()
        for i in statField:
            if i in res:
               result.append("Pass")
            else:
                result.append("Fail")
    except:

        


#def rdc_discover_group_gpu(tstname,cmnd,test_string,testnum):


def rdc_remote_execution(tstname,cmnd,test_string,testnum):
    logger.info('Entered test: %s'%tstname)
    try:
        print("rdc_discover_gpu")        
        print(cmnd)        
        res = execute_remotely("%s"%sys.argv[1],"taccuser","AH64_uh1",cmnd)
        print(res)
        logger.info('Result: %s'%res)
        # re.findall returns a list of matches
        matches = re.findall(test_string, str(res))
        print(len(matches))
        if len(matches) > 0:
            print("%s exist"%test_string)
            logger_pass(tstname,cmnd,testnum)
        else:
            print("%s does not exist"%test_string)
            logger_fail(tstname,cmnd,testnum)
    except:
        logger.error("error in rdc_remote_execution")
        logger.exception("error in rdc_remote_execution")



def execute_remotely(host,user,pwd,cmd):
    try:
        import pexpect
        from pexpect import pxssh
        import getpass        
        s = pxssh.pxssh()                        
        s.login(host, user, pwd)
        s.sendline(cmd)   # run a command
        s.prompt()             # match the prompt
        #print(s.before))        # print everything before the prompt.
        #s.logout()
        return s.before
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)




def rdc_run_tests():
    logger.info('Started running RDC test cases')
    try:
        testnum = 0
        for tstname in test_names:
            testnum = testnum + 1
            #command = test_commands[tstname]
            if tstname == "rdc_service_start_test_1":                
                test_string = "Accepting Authenticated connections only"
                command = "cd %s && ./server/rdcd"%rdcpath                
                rdc_remote_execution(tstname,command,test_string,testnum)
            elif tstname == "rdc_discover_gpu_test_4":
                fetch_fqdn()
                test_string = "GPU Index"
                command = "rdci discovery --host %s:50051 -l"%fqdn           
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_create_gpu_group_test_5":
                test_string = "Successfully created group"
                command = "rdci group -c GPU_GROUP --host %s:50051"%fqdn                
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_list_gpu_group_test_6":
                test_string = "group found"
                command = "rdci group --host %s:50051 -l"%fqdn             
                rdc_client_tests(tstname,command,test_string,testnum)            
            elif tstname == "rdc_attach_gpu_to_group_test_7":
                test_string = "Successfully added the GPU"
                command = "rdci group -g %s -a 0 --host %s:50051"%(grpid,fqdn)                
                rdc_client_tests(tstname,command,test_string,testnum)          
            elif tstname == "rdc_stats_job_create_test_8":
                test_string = "Successfully started recording job"
                command = "rdci stats --host %s:50051 -g %s -s 123"%(fqdn,grpid)                
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_stats_job_stop_test_9":
                test_string = "Successfully stopped recording job"
                command = "rdci stats --host %s:50051 -g %s -x 123"%(fqdn,grpid)
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_stats_show_summary_test_10":
                test_string = "Execution Stats"
                command = "rdci  stats --host %s:50051 -j 123"%fqdn                
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_stats_validate_statsfield_test_11":
                rdc_stats_validate()
            elif tstname == "rdc_fieldgroup_create_test_12":
                test_string = "Successfully created a field group"
                command = "rdci fieldgroup --host %s:50051 -c mg -f 50"%fqdn                
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_fieldgroup_list_test_13":
                test_string = "field group found"
                command = "rdci fieldgroup --host %s:50051 -l"%fqdn
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_fieldgroup_viewinfo_test_14":
                test_string = "Field Ids"
                command = "rdci fieldgroup --host %s:50051 -g %s -i"%(fqdn,fgrpid)                
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_check_invalid_field_group_test_15":
                test_string = "Invalid Input"
                command = "rdci fieldgroup --host %s:50051 -i -g 500"
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_monitor_telemetry_test_16":
                test_string = "TEMP"
                command = "rdci dmon --host %s:50051 -e 50 -i 0 -c 5 -d 1000"%fqdn            
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_fieldgroup_delete_test_17":
                test_string = "Successfully deleted the field group"
                command = "rdci fieldgroup --host %s:50051 -d %s"%(fqdn,fgrpid)                
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_delete_gpu_group_test_18":
                test_string = "Successfully deleted the group"
                command = "rdci group -d %s --host %s:50051"%(grpid,fqdn)                
                rdc_client_tests(tstname,command,test_string,testnum)
            #elif tstname == "rdc_monitor_telemetry_test_16":
                #test_string = "TEMP"
                #rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_connect_with_auth_test_19":
                test_string = "GPUs found"
                command = "rdci discovery --host %s:50051 -l"%fqdn                
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_connect_without_auth_test_20":
                test_string = "GPUs found"
                command = "rdci discovery --host %s:50051 -l"%fqdn
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_check_supported_field_IDs_test_21":
                test_string = "Supported fields Ids:"
                command = "rdci dmon --host %s:50051 -l"%fqdn
                rdc_check_field_IDs(tstname,command,test_string,testnum)
            elif tstname == "rdc_monitor_device_with_field_IDs_test_22":                
                rdc_monitor_device_with_field_IDs(tstname,testnum)

            elif tstname == "rdc_fieldgroup_with_invalid_fieldID_test_23":
                test_string = "Not supported"
                command = "rdci fieldgroup --host %s:50051 -c mygroupnew -f 120"%fqdn
                rdc_client_tests(tstname,command,test_string,testnum)
            elif tstname == "rdc_singleinstance_clientserver_setup_test_24":
                local_clientserver_setup(tstname,testnum)

                


        tab.add_rows(x)
        tab.set_cols_align(['r','r','r'])
        tab.header(['S.no', 'RDC-TestCases', 'Result'])
        print(tab.draw())
        summary_result()
        #print(pt)       
    except:
        logger.error("error in rdc_run_tests")
        logger.exception("error in rdc_run_tests")



def local_clientserver_setup(tstname,testnum):
    logger.info('Entered test: %s'%tstname)
    result = []
    try:
        command = "./server/rdcd && rdci group --host localhost:50051 -l"
        res = os.system("cd %s && ./server/rdcd"%rdcpath)
        if "Accepting Authenticated connections only" in res:
            result.append("Pass")
        else:
            result.append("Fail")
        res = os.system("rdci group --host localhost:50051 -l")
        if "group found" in res:
            result.append("Pass")
        else:
            result.append("Fail")

        if "Fail" in result:
            logger_fail(tstname,command,testnum)
        else:
            logger_pass(tstname,command,testnum)
    except:
        logger.error("error in %s"%tstname)
        logger.exception("error in %s"%tstname)



def load_defaults():
    global pt,tab,x
    pt = PrettyTable()
    pt.field_names = ["Test_name","Status"]
    pt.align["Test_name"] = "l"
    pt.align["Status"] = "l"
    
    #tab = tt.Texttable()
    #x = [[]]
    #tab.add_rows(x)
    #tab.set_cols_align(['r','r','r'])
    #tab.header(['S.no', 'RDC-TestCases', 'Result'])
    #print(tab.draw())


def logger_pass(test_string,command,testnum):
    try:        
        pt.add_row([test_string,"PASS"])
        logger.error('Run Test : %s'%test_string)
        logger.error('Run Command : %s'%command)
        logger.info('Test: %s is Passed'%test_string)
        x.append([testnum,test_string,"PASS"])
        results.append("pass")
        print("Hi")
    except:
        print("error in logger_pass")


def logger_fail(test_string,command,testnum):
    global steps,pt
    try:        
        pt.add_row([test_string,"FAIL"])
        logger.error('Run Command : %s'%test_string)
        logger.error('Run Command : %s'%command)
        logger.info('Test: %s is Failed'%test_string)
        logger.info('\n')
        x.append([testnum,test_string,"FAIL"])
        results.append("fail")
        print("Hi")
    except:
        print("error in logger_fail")

def summary_result():
    z = PrettyTable()
    z.field_names = ["TotalTests","TotalPass","TotalFail"]
    totpass=[]
    totfail=[]    
    for i in results:
        if i == "pass":
            totpass.append(i)        
        elif i == "fail":
            totfail.append(i)
        else:
            print("Notmentioned")
    z.add_row([len(results), len(totpass), len(totfail)])
    print(z)


def main():
    start = datetime.now()
    logging.info("starting test suite")
    load_defaults()
    rdc_run_tests()    
    end = datetime.now()-start
    endtime = end.total_seconds() / 60




if __name__ == '__main__':
    main()
