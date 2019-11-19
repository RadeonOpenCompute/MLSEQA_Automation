import os, sys, re, itertools, subprocess, json, logging
from subprocess import PIPE, run
from prettytable import PrettyTable

#regex1=r'.*?LKG =*$'
regex1=r'^LKG = .*$'
log_path="/home/taccuser/MLSEQA_Automation/rocm_components/test.log"
HOME = os.environ['HOME']
print(HOME)
#lkg=""

#wget http://ocltc.amd.com/cgi-bin/teamcity_opencl_lkg.pl?justcl=1 -q -O -

def last_known_good():
    res=os.popen("wget http://ocltc.amd.com/cgi-bin/teamcity_opencl_lkg.pl?justcl=1 -q -O - | tee test.log").read()
    #print(re#r1 = re.findall(regex1,res)
    match = re.findall(regex1, res)
    with open(log_path, "r") as file:
        for line in file:
            for match in re.finditer(regex1, line, re.S):
                if match:
                    #print(match.group())
                    var1 = match.group().split("=")
                    out = var1[1].strip()                    
                    last_known_good.var = out
                    #print(lkg)
                    #print("result found")

                else:
                    print("result not found")


def download_lkg():
    print(last_known_good.var)
    os.system("cd $HOME && wget -q -o /dev/null --user guest --password guest 'http://ocltc.amd.com:8111/repository/download/BuildsOpenCLHsaStaging_OpenCLLinuxPro_LinuxX8664ReleaseGfx9LinuxPro/%s:id/opencl/tests/ocltst.zip'" %last_known_good.var)
    os.system("cd $HOME/ && pwd && unzip -o ocltst.zip")
    os.system("cd $HOME/ocltst/x86_64 && export LD_LIBRARY_PATH=$PWD")


last_known_good()
download_lkg()

#with open(res, "r") as file:
#    for line in file:
#        for match in re.finditer(regex1, line, re.S):
#            print(match.group())


