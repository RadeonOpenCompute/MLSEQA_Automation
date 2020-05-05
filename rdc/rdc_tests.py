## Created by    : Rahul Mula
## Creation Date : 05/05/2020
## Description   : Script for RDC tool testing
import os, sys, re, itertools, subprocess, shutil, json, logging
import texttable as tt
from prettytable import PrettyTable
from datetime import datetime


HOME = os.environ['HOME']
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
        "rdc_discover_gpu_test_4"
        ]

test_commands = {"rdc_service_start_test_1":'sudo systemctl start rdc',
        "rdc_service_stop_test_2":'sudo systemctl stop rdc',
        "rdc_verify_rdc_daemon_test_3":'sudo ./rdcd',
        "rdc_discover_gpu_test_4":'rdci discovery -l'
        }



def rdc_service_start(tstname, cmnd):
    logger.info('Entered test: rdc_service_start_test_1')
    try:
        os.popen("%s"%cmnd).read()
        res = os.popen("sudo systemctl status rdc").read()
        for item in res.split("\n"):
            if "Active:" in item:
                status = item.split("(")[0].split(":")[1].strip()
                print(status)
                if status == "failed":
                    logger_fail(tstname, cmnd)
                elif status == "passed":
                    logger_pass(tstname, cmnd)

    except:
        logger.error("error in rdc_service_start")
        logger.exception("error in rdc_service_start")


def rdc_discover_gpu(tstname, cmnd):
    logger.info('Entered test: %s'%tstname)
    try:
        print("rdc_discover_gpu")        
        cmd="cd /home/taccuser/rdc/rdc/build && echo 'AH64_uh1' | sudo -S LD_LIBRARY_PATH=$PWD/rdc_libs/ ./rdci/rdci discovery --host singularity-node.amd.com:50051 -u -l"            
        res = execute_remotely("10.130.161.243","taccuser","AH64_uh1",cmd)
        print(res)
        logger.info('Result: %s'%res)
        # re.findall returns a list of matches
        matches = re.findall("GPU Index", str(res))
        print(len(matches))
        if len(matches) > 0:
            print("GPU Index exist")
            logger_pass(tstname, cmnd)
        else:
            print("GPU Index does not exist")
            logger_fail(tstname, cmnd)
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
        for tstname in test_names:
            command = test_commands[tstname]
            if tstname == "rdc_service_start_test_1":
                rdc_service_start(tstname,command)
            elif tstname == "rdc_discover_gpu_test_4":
                rdc_discover_gpu(tstname,command)

        print(pt)
       
    except:
        logger.error("error in rdc_run_tests")
        logger.exception("error in rdc_run_tests")


def load_defaults():
    global pt
    pt = PrettyTable()
    pt.field_names = ["Test_name","Status"]
    pt.align["Test_name"] = "l"
    pt.align["Status"] = "l"


def logger_pass(test_string,command):
    try:        
        pt.add_row([test_string,"PASS"])
        logger.error('Run Test : %s'%test_string)
        logger.error('Run Command : %s'%command)
        logger.info('Test: %s is Passed'%test_string)
    except:
        print("error in logger_pass")


def logger_fail(test_string,command):
    global steps,pt
    try:        
        pt.add_row([test_string,"FAIL"])
        logger.error('Run Command : %s'%test_string)
        logger.error('Run Command : %s'%command)
        logger.info('Test: %s is Failed'%test_string)
        logger.info('\n')
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
