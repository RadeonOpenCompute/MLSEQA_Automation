from prettytable import PrettyTable
import os, sys, re, itertools, subprocess
from subprocess import PIPE, run
#from automailer import *

#from datetime import datetime
from artifactory import ArtifactoryPath
#from dateutil.relativedelta import relativedelta


#def prerequisite():

#envpath="../../utils/Test_Framework_APIs/mlpmo_executor" 
#sys.path.append(envpath)
#from mlseqa_setup import MLSEQA_Setup
#mlseqa_setup = MLSEQA_Setup()
#mlseqa_setup.setup_path_and_check_python_prerequisites()
#mlseqa_setup.setup_pip_packages_requirements_txt()
#mlseqa_setup.setup_pip_packages_mysql_client_requirements_txt()
#from mlse_django.setup_django import SetupDjango
#SetupDjango().setup(start_django_mserver=False)
#from mlse_django.mlse_ws.api.db import OCLTestResult, AllDBAccess, ROCm_Component
#import datetime



#start=datetime.datetime.now()
os.system("sudo apt -y install unzip pciutils")
HOME = os.environ['HOME']
lkg_log_path= HOME + "/test.txt"
test_path = HOME + "/ocltst/x86_64"
ocl_logs=[test_path +'/oclregression.log', test_path +'/oclcompiler.log', test_path +'/oclprofiler.log', test_path +'/ocldebugger.log', test_path +'/oclfrontend.log',test_path +'/oclmediafunc.log', test_path +'/oclperf.log']
summary_files = [HOME + '/ocl_summary.html', HOME + '/ocl_summary.txt', HOME + '/ocl.log']
pkg_url = ["http://rocm-ci.amd.com/job/compute-rocm-dkms-no-npi/lastSuccessfulBuild/artifact/artifacts/","http://rocm-ci.amd.com/view/HIP-Clang/job/compute-rocm-dkms-no-npi-hipclang-int-bkc-2/25/artifact/artifacts/"]

regex=r'.*?Passed Tests:.*$'
regex1=r'.*?Failed Tests:.*$'
regex2=r'.*?Run Tests:.*$'
regex3=r'.*?Testing Module.*$'
regex4=r'^LKG = .*$'
totpass = []
totfail = []
tottests = []
testcategory = []
oclcategory = []
ocltottests = []
ocltotpass = []
ocltotfail = []


def clean_log():
    for filepath in summary_files:
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print("Can not delete the file as it doesn't exists")


def ocl_get_lkgnum():
    res=os.popen("wget http://ocltc.amd.com/cgi-bin/teamcity_opencl_lkg.pl?justcl=1 -q -O - | tee %s" %lkg_log_path).read()       
    match = re.findall(regex4, res)
    with open(lkg_log_path, "r") as file:
        for line in file:
            for match in re.finditer(regex4, line, re.S):
                if match:                    
                    var1 = match.group().split("=")
                    out = var1[1].strip()                    
                    ocl_get_lkgnum.var = out                                       
                else:
                    print("result not found")
                    

def ocl_get_lkgpkg():
    try:
        print(ocl_get_lkgnum.var)
        if os.path.exists("%s/ocltst.zip" %HOME):
            os.remove("%s/ocltst.zip" %HOME)
        elif os.path.exists("%s/ocltst" %HOME):
            os.rmdir("%s/ocltst" %HOME)
        os.system("cd $HOME && wget http://ocltc.amd.com:8111/guestAuth/repository/download/BuildsOpenCLHsaStaging_OpenCLLc_LinuxX8664Release/{0}/opencl/tests/ocltst.zip".format(ocl_get_lkgnum.var))
        os.system("cd $HOME/ && pwd && unzip -o ocltst.zip")
        #os.system("cd $HOME/ocltst/x86_64 && export LD_LIBRARY_PATH=$PWD")
        if "LD_LIBRARY_PATH" in os.environ:
            os.environ["LD_LIBRARY_PATH"] += HOME + "/ocltst/x86_64"
        else:
            os.environ["LD_LIBRARY_PATH"] = HOME + "/ocltst/x86_64"
    except:
        print("ERROR with LKG number picking")
        

def get_ocltest_info(oclcategory=oclcategory, ocltottests=ocltottests, ocltotpass=ocltotpass, ocltotfail=ocltotfail):    
    x = PrettyTable()
    x.field_names = ["OCL Components","TotalTests","TotalPass","TotalFail"]
    for ocl_logpath in ocl_logs:        
        with open(ocl_logpath, "r") as file:
            for line in file:
                #global y
                for match in re.finditer(regex, line, re.S):
                    str = match.group().split(" (")                  
                    str1 = str[0].split(" ")
                    str1.reverse()
                    totpass = str1[0]
                    ocltotpass.append(str1[0])

                for match in re.finditer(regex1, line, re.S):
                    str = match.group().split(" (")
                    str1 = str[0].split(" ")
                    str1.reverse()
                    totfail = str1[0]
                    ocltotfail.append(str1[0])

                for match in re.finditer(regex2, line, re.S):
                    str = match.group().split(" (")
                    str1 = str[0].split(" ")
                    str1.reverse()
                    tottests = str1[0]
                    ocltottests.append(str1[0])

                for match in re.finditer(regex3, line, re.S):
                    str = match.group().split(" ")                    
                    testcategory = str[4]                    
                    oclcategory.append(str[4])
            
             
            x.add_row([testcategory, tottests, totpass, totfail])
    
    hip_summary_print("OCL Overall Summary", x, mode='a')
    return(x)

def hip_summary_print(summary, value, mode):
    os.system("touch mail")
    with open(summary_files[0], mode) as t:
        t.write("</br><b>%s</b></br>" %summary)
        t.write(value.get_html_string())
        t.write("</br>")
    with open(summary_files[1], mode) as txtfile:
        txtfile.write("%s\n" %summary)
        txtfile.write(value.get_string())
        txtfile.write("\n")



def ocl_get_pkg_version():
    ocl_get_whichos()
    if ocl_get_whichos.osname == "ubuntu":
        rocmver = os.popen("dpkg -l | grep hsa-rocr-dev").read()
    elif ocl_get_whichos.osname == "centos":
        rocmver = os.popen("yum info rocm-utils | grep Version").read()
    elif ocl_get_whichos.osname == "rhel":
        rocmver = os.popen("yum info rocm-utils | grep Version").read()
    #print(re.findall(r'\S+', rocmver))
    pkg_name = re.findall(r'\S+', rocmver)[2]
    print(pkg_name)
    if "bkc" in pkg_name:
        print(ocl_hipclang_fetch_pkg(pkg_name))
        #print(pkg_name.split("-")[8])
        #hipclang_pkgname = "compute-rocm-dkms-no-npi-hipclang-int-bkc-%s-%s.tar.bz2" %(pkg_name.split("-")[8],pkg_name.split("-")[9])
        #pkg_details = pkg_url[1].split("/")[6]
        #print(pkg_details)
        #print(pkg_details.split("-")[-1])
        #res = [sub.replace(pkg_details.split("-")[-1], pkg_name.split("-")[8]) for sub in pkg_details.split("-")]
        #print('-'.join(res))
        #pkg_interchange = pkg_url[1].replace(pkg_url[1].split("/")[6], '-'.join(res))
        #print(pkg_interchange)
        #hipclang_pkgdetails = pkg_interchange + hipclang_pkgname
        #print(hipclang_pkgdetails)
        #return hipclang_pkgdetails
    elif "hipclang" not in pkg_name:
        hipclang_pkgname = "compute-rocm-dkms-no-npi-%s.tar.bz2" %pkg_name.split("-")[5]
        print(pkg_url[0].split("/"))
        return hipclang_pkgname
        print(hipclang_pkgname)
    elif "rel" in pkg_name:
        hipclang_pkgname = "compute-rocm-dkms-no-npi-hipclang-int-bkc-%s-%s.tar.bz2" %(pkg_name.split("-")[8],pkg_name.split("-")[9])
        print("release")
  
def ocl_hipclang_fetch_pkg(pkg_name):
    hipclang_pkgname = "compute-rocm-dkms-no-npi-hipclang-int-bkc-%s-%s.tar.bz2" %(pkg_name.split("-")[8],pkg_name.split("-")[9])
    pkg_details = pkg_url[1].split("/")[6]
    res = [sub.replace(pkg_details.split("-")[-1], pkg_name.split("-")[8]) for sub in pkg_details.split("-")]
    pkg_interchange = pkg_url[1].replace(pkg_url[1].split("/")[6], '-'.join(res))
    hipclang_pkgdetails = pkg_interchange + hipclang_pkgname
    return hipclang_pkgdetails

def ocl_hccbkc_fetch_pkg(pkg_name):
    print(pkg_name)
    pkg_url[0].split("/")


def ocl_download_pkg(pkg_link):
    #http://rocm-ci.amd.com/job/compute-rocm-dkms-no-npi/lastSuccessfulBuild/artifact/artifacts/compute-rocm-dkms-no-npi-2256.tar.bz2 
    pkg_details = ocl_get_pkg_version()
    


#def ocl_check_folderexists(pkg_name):    
    #if not os.path.isdir(pkg_name):
        #download package
        #untar
        
    #else:

    #print(string1.split("-")[5])

#def ocl_test_pkgname(string1):
    #hipclang_pkgname = "compute-rocm-dkms-no-npi-hipclang-int-bkc-%s-%s.tar.bz2" %(string1.split("-")[8],string1.split("-")[9])

def ocl_run_tests():

    os.system("export LD_LIBRARY_PATH='%s'" %test_path) 
    os.system("pwd")
    print("=====Running oclcompiler======")
    os.system("cd %s && ./ocltst -m oclcompiler.so -A oclcompiler.exclude | tee oclcompiler.log" %test_path)
    print("=====Running oclprofiler======")
    os.system("cd %s && ./ocltst -m oclprofiler.so -A oclprofiler.exclude | tee oclprofiler.log" %test_path)
    print("=====Running ocldebugger======")
    os.system("cd %s && ./ocltst -m ocldebugger.so -A ocldebugger.exclude | tee ocldebugger.log" %test_path)
    print("=====Running oclmediafunc======")
    os.system("cd %s && ./ocltst -m oclmediafunc.so -A oclmediafunc.exclude | tee oclmediafunc.log" %test_path)
    print("=====Running oclperf======")
    os.system("cd %s && ./ocltst -m oclperf.so -A oclperf.exclude | tee oclperf.log" %test_path)
    print("=====Running oclregression======")
    os.system("cd %s && ./ocltst -m oclregression.so -A oclregression.exclude | tee oclregression.log" %test_path)
    print("=====Running oclfrontend======")
    os.system("cd %s && ./ocltst -m oclfrontend.so -A oclfrontend.exclude | tee oclfrontend.log" %test_path)
    #os.system("cd %s && ./ocltst -m oclruntime.so -A oclruntime.exclude 2>&1 | tee oclruntime.log" %test_path)
    #hip_summary_print("System Info", sysinfo, mode='w')



def ocl_get_whichos():
    quates='"'
    osdet = os.popen("cat /etc/os-release").read()
    for item in osdet.split("\n"):
        if "ID" in item:
            ocl_get_whichos.os = item.split("=")[1]
            if ocl_get_whichos.os.startswith('"'):                                    
                ocl_get_whichos.osname = item.split("=")[1][1:-1]                
                print(ocl_get_whichos.osname)
            else:                
                ocl_get_whichos.osname = item.split("=")[1]
                print(ocl_get_whichos.osname)
            break


def ocl_get_rocmversion():
    ocl_get_whichos()
    if ocl_get_whichos.osname == "ubuntu":  
        rocmver = os.popen("dpkg -l | grep rocm-utils").read()
    elif ocl_get_whichos.osname == "centos":
        rocmver = os.popen("yum info rocm-utils | grep Version").read()
    elif ocl_get_whichos.osname == "rhel":
        rocmver = os.popen("yum info rocm-utils | grep Version").read()
    string1 = re.findall(r'\S+', rocmver)    
    rocver = string1[2].split(".")[2]    
    if int(rocver) > 300:
        ocl_get_rocmversion.dtb = True
        ocl_get_rocmversion.rel = False
        ocl_get_rocmversion.rocmversion = rocver
    elif int(rocver) < 300:
        ocl_get_rocmversion.rel = True
        ocl_get_rocmversion.dtb = False
        ocl_get_rocmversion.rocmversion = string1[2]
    print(ocl_get_rocmversion.rel)
    print(ocl_get_rocmversion.rocmversion)



def ocl_get_gpuinfo():
    res1 = os.popen("/opt/rocm/opencl/bin/x86_64/clinfo").read()    
    for item in res1.split("\n"):
        if "Number of devices:" in item:        
            ocl_get_gpuinfo.ngpu = re.findall(r'\S+', item)[3]           

        if "Board name:" in item:
            gpuname = re.findall(r'\S+', item)            
            if "Device" in gpuname:
                outres = gpuname[2] + ' ' + gpuname[3]
            else:
                outres = gpuname[2] + ' ' + gpuname[3]
    ocl_get_gpuinfo.gpu = outres.partition('\n')[0]
    print(ocl_get_gpuinfo.gpu)            



def ocl_get_hostdetails():
    ocl_get_hostdetails.hostname = os.popen("hostname").read().strip()   
    res2=os.popen("cat /etc/os-release").read()
    for item1 in res2.split("\n"):
        if "PRETTY_NAME" in item1:            
            ocl_get_hostdetails.osversion = eval(item1.split("=")[1])
            print(ocl_get_hostdetails.osversion)
 

def ocl_get_runtime():
    ocl_get_runtime.time = datetime.datetime.now()-start
    #print('Total ExecutionTime: ',datetime.datetime.now()-start)
    #totruntime = time.split(".")[0] 
    #print(totruntime)
    print(ocl_get_runtime.time)


def update_or_create():
    ocl_get_rocmversion()
    ocl_get_gpuinfo()
    ocl_get_hostdetails()
    #ocl_get_runtime()
    for (oclcoponents, ocltest, oclpass, oclfail) in zip(oclcategory, ocltottests, ocltotpass, ocltotfail):
        all_db_access = AllDBAccess()
        test_result = OCLTestResult()
        test_result.test_name = oclcoponents 
        test_result.gpu = ocl_get_gpuinfo.gpu 
        test_result.nGPU = ocl_get_gpuinfo.ngpu
        test_result.os = ocl_get_hostdetails.osversion
        test_result.is_dtb = ocl_get_rocmversion.dtb
        test_result.is_release = ocl_get_rocmversion.rel
        test_result.rocm_version = ocl_get_rocmversion.rocmversion
        test_result.hostname = ocl_get_hostdetails.hostname
        test_result.jira_id = ""
        test_result.start_datetime = datetime.datetime.now()
        test_result.run_time = float(10)
        test_result.artifactory_logs = ""
        test_result.n_total = ocltest
        test_result.n_passed = oclpass
        test_result.n_failed = oclfail
        test_result.n_skipped = 0
        test_result.n_error = 0
        import django
        try:
            all_db_access.update_or_create(comp=ROCm_Component.ocl, test_result=test_result)
        except django.db.utils.OperationalError:
            print("update/create failed::check MySQL connection")

def upload_aritifactory():

    artifactory_path = "http://10.128.142.190:8081/artifactory/qa_local_logpath/ocl/"
    #mail_dir = "/home/taccuser/MLSEQA_TestRepo/Sanity/driver_sanity/mail/"
    currentDT = datetime.datetime.now()
    artifactory_path=artifactory_path+currentDT.strftime("%Y-%m-%d_%H:%M")
    path = ArtifactoryPath(artifactory_path,auth=('rocmqa','AH64_uh1'))
    path.mkdir()
    #List=os.listdir(mail_dir)
    #for i in List:
        #if i.endswith('.html'):
            #continue
        #path.deploy_file(mail_dir+'/'+i)
    strs = [summary_files[0], summary_files[1]]
    for val in strs:
        print(val)
        path.deploy_file(val)
    print ("Succesfully Uploaded in to Artifactory")
        



ocl_get_pkg_version()

#clean_log()
#ocl_get_lkgnum()
#ocl_get_lkgpkg()
#ocl_run_tests()
#print(get_ocltest_info())
#print ('Total ExecutionTime: ',datetime.datetime.now()-start)
#update_or_create()
#Auto_mail(summary_files[0], "OCL", summary_files[1])
#upload_aritifactory()


