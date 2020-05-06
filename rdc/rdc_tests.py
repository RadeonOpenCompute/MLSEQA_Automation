## Created by    : Rahul Mula
## Creation Date : 05/05/2020
## Description   : Script for RDC tool testing
import os, sys, re, itertools, subprocess, shutil, json, logging
import texttable as tt
from prettytable import PrettyTable
from datetime import datetime
import texttable as tt


HOME = os.environ['HOME']
tab = tt.Texttable()
x = [[]]
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
        "rdc_delete_gpu_group_test_8",
        "rdc_stats_create_job_test_9",
        "rdc_stats_stop_job_test_10",
        "rdc_stats_show_summary_test_11",
        "rdc_fieldgroup_create_test_12",
        "rdc_fieldgroup_list_test_13",
        "rdc_fieldgroup_viewinfo_test_14",
        "rdc_fieldgroup_delete_test_15",
        "rdc_monitor_telemetry_test_16",
        "rdc_connect_with_auth_test_17",
        "rdc_connect_without_auth_test_18"
        ]

test_commands = {"rdc_service_start_test_1":'sudo systemctl start rdc',
        "rdc_service_stop_test_2":'sudo systemctl stop rdc',
        "rdc_verify_rdc_daemon_test_3":'sudo ./rdcd',
        "rdc_discover_gpu_test_4":'cd /home/taccuser/rdc/rdc/build && echo "AH64_uh1" | sudo -S LD_LIBRARY_PATH=$PWD/rdc_libs/ ./rdci/rdci discovery --host singularity-node.amd.com:50051 -u -l',
        "rdc_create_gpu_group_test_5":'rdci group -c GPU_GRP --host singularity-node.amd.com:50051 -u',
        "rdc_list_gpu_group_test_6":'rdci group --host singularity-node.amd.com:50051 -u -l',        
        "rdc_attach_gpu_to_group_test_7":'rdci group -g 10 -a 0 --host singularity-node.amd.com:50051 -u',
        "rdc_delete_gpu_group_test_8":'rdci group -d 6 --host singularity-node.amd.com:50051 -u',
        "rdc_stats_create_job_test_9":'rdci stats --host singularity-node.amd.com:50051 -u -g 2 -s 123',
        "rdc_stats_stop_job_test_10":'rdci stats --host singularity-node.amd.com:50051 -u -g 2 -x 123',
        "rdc_stats_show_summary_test_11":'rdci  stats --host singularity-node.amd.com:50051 -u -j 123',
        "rdc_fieldgroup_create_test_12":'rdci fieldgroup --host singularity-node.amd.com:50051 -u -c mg -f 50',
        "rdc_fieldgroup_list_test_13":'rdci fieldgroup --host singularity-node.amd.com:50051 -u -l',
        "rdc_fieldgroup_viewinfo_test_14":'rdci fieldgroup --host singularity-node.amd.com:50051 -u -g 1 -i',
        "rdc_fieldgroup_delete_test_15":'rdci fieldgroup --host singularity-node.amd.com:50051 -u -d 1',
        "rdc_monitor_telemetry_test_16":'rdci dmon --host singularity-node.amd.com:50051 -u -e 50 -i 0 -c 5 -d 1000',
        "rdc_connect_with_auth_test_17":'rdci discovery --host singularity-node.amd.com:50051 -l',
        "rdc_connect_without_auth_test_18":'rdci discovery --host singularity-node.amd.com:50051 -u -l'
        }



def rdc_service_start(tstname, cmnd, tstnum):
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


def rdc_discover_group_gpu(tstname,cmnd,test_string,testnum):
    logger.info('Entered test: %s'%tstname)
    try:
        print("rdc_discover_gpu")        
        cmd="cd /home/taccuser/rdc/rdc/build && echo 'AH64_uh1' | sudo -S LD_LIBRARY_PATH=$PWD/rdc_libs/ ./rdci/rdci discovery --host singularity-node.amd.com:50051 -u -l"            
        res = execute_remotely("10.130.161.243","taccuser","AH64_uh1",cmnd)
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
        logger.error("error in rdc_discover_gpu")
        logger.exception("error in rdc_discover_gpu")



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
            command = test_commands[tstname]
            if tstname == "rdc_service_start_test_1":                
                rdc_service_start(tstname,command,testnum)
            elif tstname == "rdc_discover_gpu_test_4":
                test_string = "GPU Index"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_create_gpu_group_test_5":
                test_string = "Successfully created group"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_list_gpu_group_test_6":
                test_string = "group found"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)            
            elif tstname == "rdc_attach_gpu_to_group_test_7":
                test_string = "Successfully added the GPU"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_delete_gpu_group_test_8":
                test_string = "Successfully deleted the group"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_stats_create_job_test_9":
                test_string = "Successfully started recording job"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_stats_stop_job_test_10":
                test_string = "Successfully stopped recording job"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_stats_show_summary_test_11":
                test_string = "Execution Stats"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_fieldgroup_create_test_12":
                test_string = "Successfully created a field group"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_fieldgroup_list_test_13":
                test_string = "field group found"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_fieldgroup_viewinfo_test_14":
                test_string = "Field Ids"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_fieldgroup_delete_test_15":
                test_string = "Successfully deleted the field group"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_monitor_telemetry_test_16":
                test_string = "TEMP"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_connect_with_auth_test_17":
                test_string = "GPUs found"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)
            elif tstname == "rdc_connect_without_auth_test_18":
                test_string = "GPUs found"
                rdc_discover_group_gpu(tstname,command,test_string,testnum)

        tab.add_rows(x)
        tab.set_cols_align(['r','r','r'])
        tab.header(['S.no', 'RDC-TestCases', 'Result'])
        print(tab.draw())
        #print(pt)
       
    except:
        logger.error("error in rdc_run_tests")
        logger.exception("error in rdc_run_tests")



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
    except:
        print("error in logger_fail")

def main():
    start = datetime.now()
    logging.info("starting test suite")
    load_defaults()
    rdc_run_tests()
    end = datetime.now()-start
    endtime = end.total_seconds() / 60




if __name__ == '__main__':
    main()
