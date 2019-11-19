from prettytable import PrettyTable
import os, sys, re, itertools
from automailer import *
#from qa_testapi import *
from datetime import datetime
from artifactory import ArtifactoryPath

start=datetime.now()

if len(sys.argv) != 2:
    print("Please make sure you have entered one arguments")
    sys.exit(1)



test_path = "%s" %sys.argv[1]
ocl_logs=[test_path +'/oclruntime.log', test_path +'/oclregression.log', test_path +'/oclcompiler.log', test_path +'/oclprofiler.log', test_path +'/ocldebugger.log', test_path +'/oclfrontend.log',test_path +'/oclmediafunc.log', test_path +'/oclperf.log']
summary_files = ['/home/taccuser/MLSEQA_Automation/rocm_components/mail/ocl_summary.html', '/home/taccuser/MLSEQA_Automation/rocm_components/mail/ocl_summary.txt', '/home/taccuser/MLSEQA_Automation/rocm_components/mail/ocl.log']

regex=r'.*?Passed Tests:.*$'
regex1=r'.*?Failed Tests:.*$'
regex2=r'.*?Run Tests:.*$'
regex3=r'.*?Testing Module.*$'


totpass = []
totfail = []
tottests = []
testcategory = []

def get_ocltest_info():
    x = PrettyTable()
    x.field_names = ["OCL Components","TotalTests","TotalPass","TotalFail"]
    for ocl_logpath in ocl_logs:
        with open(ocl_logpath, "r") as file:
            for line in file:
                for match in re.finditer(regex, line, re.S):
                    str = match.group().split(" (")                  
                    str1 = str[0].split(" ")
                    str1.reverse()
                    totpass = str1[0]                    

                for match in re.finditer(regex1, line, re.S):
                    str = match.group().split(" (")
                    str1 = str[0].split(" ")
                    str1.reverse()
                    totfail = str1[0]                   

                for match in re.finditer(regex2, line, re.S):
                    str = match.group().split(" (")
                    str1 = str[0].split(" ")
                    str1.reverse()
                    tottests = str1[0]                   

                for match in re.finditer(regex3, line, re.S):
                    str = match.group().split(" ")                    
                    testcategory = str[4]

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




def ocl_run_tests():

    os.system("export LD_LIBRARY_PATH='%s'" %test_path)
    os.system("cd %s && ./ocltst -m oclruntime.so -A oclruntime.exclude 2>&1 | tee oclruntime.log" %test_path)
    os.system("pwd")
    #os.system("cd %s && ./ocltst -m oclregression.so -A oclregression.exclude | tee oclregression.log" %test_path)
    #os.system("cd %s && ./ocltst -m oclcompiler.so -A oclcompiler.exclude | tee oclcompiler.log" %test_path)
    #os.system("cd %s && ./ocltst -m oclprofiler.so -A oclprofiler.exclude | tee oclprofiler.log" %test_path)
    #os.system("cd %s && ./ocltst -m ocldebugger.so -A ocldebugger.exclude | tee ocldebugger.log" %test_path)
    #os.system("cd %s && ./ocltst -m oclfrontend.so -A oclfrontend.exclude | tee oclfrontend.log" %test_path)
    #os.system("cd %s && ./ocltst -m oclmediafunc.so -A oclmediafunc.exclude | tee oclmediafunc.log" %test_path)
    #os.system("cd %s && ./ocltst -m oclperf.so -A oclperf.exclude | tee oclperf.log" %test_path)

    #hip_summary_print("System Info", sysinfo, mode='w')

def upload_aritifactory():

    artifactory_path = "http://10.130.166.15:8081/artifactory/qa_local_logpath/ocl"
    mail_dir = "/home/taccuser/MLSEQA_Automation/rocm_components/mail/"
    currentDT = datetime.now()
    artifactory_path=artifactory_path+currentDT.strftime("%Y-%m-%d_%H:%M")
    path = ArtifactoryPath(artifactory_path,auth=('rocmqa','AH64_uh1'))
    path.mkdir()
    List=os.listdir(mail_dir)
    for i in List:
        if i.endswith('.html'):
            continue
        path.deploy_file(mail_dir+'/'+i)
    print ("Succesfully Uploaded in to Artifactory")
        
        

ocl_run_tests()
print(get_ocltest_info())
print ('Total ExecutionTime: ',datetime.now()-start)
Auto_mail(summary_files[0], "OCL", summary_files[2])
upload_aritifactory()
