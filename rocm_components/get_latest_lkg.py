import os, sys, re, itertools, subprocess, json, logging
from subprocess import PIPE, run


regex1=r'^LKG = .*$'
log_path="/home/taccuser/MLSEQA_Automation/rocm_components/test.log"
HOME = os.environ['HOME']


def ocl_get_lkgnum():
    res=os.popen("wget http://ocltc.amd.com/cgi-bin/teamcity_opencl_lkg.pl?justcl=1 -q -O - | tee test.log").read()   
    match = re.findall(regex1, res)
    with open(log_path, "r") as file:
        for line in file:
            for match in re.finditer(regex1, line, re.S):
                if match:                    
                    var1 = match.group().split("=")
                    out = var1[1].strip()                    
                    ocl_get_lkgnum.var = out                                       
                else:
                    print("result not found")


def ocl_get_lkgpkg():
    print(ocl_get_lkgnum.var)
    os.system("cd $HOME && wget -q -o /dev/null --user guest --password guest http://ocltc.amd.com:8111/repository/download/BuildsOpenCLHsaStaging_OpenCLLinuxPro_LinuxX8664ReleaseGfx9LinuxPro/{0}:id/opencl/tests/ocltst.zip".format(ocl_get_lkgnum.var))
    os.system("cd $HOME/ && pwd && unzip -o ocltst.zip")
    os.system("cd $HOME/ocltst/x86_64 && export LD_LIBRARY_PATH=$PWD")


ocl_get_lkgnum()
ocl_get_lkgpkg()

