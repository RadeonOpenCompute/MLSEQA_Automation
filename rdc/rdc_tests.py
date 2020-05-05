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
        #handler = file_handler,
        #filename = FileInfo['rdc_test.log'],
        #filename='rocpro_test.log',
        filename = 'rdc_test.log',
        filemode ='a+'
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



def rdc_service_start(cmnd):
    logger.info('Entered test: rdc_service_start_test_1')
    try:
        res = os.popen("{command}".filter(command = cmnd)).read()
        print(res)
    except:
        logger.error("error in rdc_service_start")
        logger.exception("error in rdc_service_start")


def rdc_run_tests():
    logger.info('Started running RDC test cases')
    try:
        for tstname in test_names:
            command = test_commands[tstname]
            if tstname == "rdc_service_start_test_1":
                rdc_service_start(command)
       
    except:
        logger.error("error in rdc_run_tests")
        logger.exception("error in rdc_run_tests")



def main():
    start = datetime.now()
    logging.info("starting test suite")
    rdc_run_tests()
    end = datetime.now()-start
    endtime = end.total_seconds() / 60




if __name__ == '__main__':
    main()
