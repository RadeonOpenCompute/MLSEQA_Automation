import os, json, sys, re, itertools, subprocess



HOME = os.environ['HOME']
command = "HIP_VISIBLE_DEVICES=0,1,2,3 WORLD_SIZE=4 TEMP_DIR=/tmp BACKEND=nccl /opt/rocm/bin/rocprof -d $PWD/rocprof_pyt_sys_trace_mgpu_test_case_1 --sys-trace python3.6 $PWD/pytorch/test/test_distributed.py --verbose TestDistBackend.test_all_gather_multigpu"
commands = { 
"rocprof_hcc_invalidtime_marking":'/opt/rocm/bin/rocprof --hip-trace --obj-tracking on --timestamp on -d /root/driver/rocprof_hcc_trace_test_case_1 -o /root/driver/rocprof_hcc_trace_test_case_1/rocprof_hcc_trace_test_case_1.csv python3.6 micro_benchmarking_pytorch.py --network resnet50 --batch-size 128 --iterations 10',
"rocprof_DDP_multigpu":'/opt/rocm/bin/rocprof --hip-trace --roctx-trace --obj-tracking on --timestamp on -d ./rocprof_DDP_multigpu -o /rocprof_DDP_multigpu/rocprof_hcc_trace_test_case_1.csv python3.6 bind_launch.py'
}
file_types = ['/hsa_api_trace.txt','/roctx_trace.txt','/hcc_ops_trace.txt','/hip_api_trace.txt']
output_path = "/rocprof_hcc_trace_test_case_1"
pytorch_path = "/pytorch"


def clear_outputpath():
    if os.path.exists(output_path):
        os.system("sudo rm -r %s"%output_path)



def test_rocprof_DDP_multigpu():
    ouput_path="/root/rocprof_DDP_multigpu"	
    if systrace_printresult(ouput_path,file_types[2]) == Pass:
	print("Pass")
    else:
	print("Fail")



def rocprof_DDP_multigpu():
    ouput_path="/root/rocprof_DDP_multigpu"
    if os.path.isfile('~/bind_launch.py'):
    	#os.system("{command}".format(command=commands['rocprof_DDP_multigpu']))
    	if systrace_printresult(ouput_path,file_types[2]) and systrace_printresult(ouput_path,file_types[3]) == "Pass":
	    print("rocprof_DDP_mgpu is Pass")
        else:
            print("rocprof_DDP_mgpu is Fail")
    else:
        print("no bind_launch.py")
  
    #if os.path.isfile('~/bind_launch.py'):
	#print("{command}".format(command=commands['rocprof_DDP_multigpu'],ouput_dir="rocprof_hcc_trace_test_case_1"))
    #else:
        #print("no bind_launch.py")
    #systrace_printresult(file_types[2]) 
        
   

def hcc_invalid_timemarking():
    inputdir=[]
    try:
	#inputdir=[]
        os.system("sudo mkdir -p /tmp/barrier && pwd")
        if os.path.isfile('/micro_benchmarking_pytorch.py'):
            os.system("%s"%commands['rocprof_hcc_invalidtime_marking'])
            print("Hi")
    except:
        print("error in hcc_invalid_timemarking")



def validate_file():    
    inputdir=[]
    result=[]
    for (path, dirs, files) in os.walk(output_path):            	
         inputdir.append(dirs)
    hcctrace_file = output_path + "/" + inputdir[0][0] + "/" + inputdir[1][0] + "/hcc_ops_trace.txt"
    print(hcctrace_file)
    num_lines = 0
    with open(hcctrace_file, "r") as f:
        for line in f:
            time = line.split(" ")[0]
            begin_time = int(time.split(":")[0])
            end_time = int(time.split(":")[1])
            if end_time - begin_time < 0:
               print("Fail")
               result.append("Fail")
    if "Fail" in result:
       print("Fail")
    else:
       print("Pass")



def sys_trace_validation():
    try:
        pytorch_path = "/pytorch"
        print("Hi")
        os.system("sudo mkdir -p /tmp/barrier && pwd")
        print("json command fetching")
        if os.path.exists(pytorch_path):
            print("pytorch path exists")
            #os.system("cd %s/test"%pytorch_path)
            if os.path.isfile('/pytorch/test/test_distributed.py'):                
                os.system("%s"%command)
            else:
                os.system("git clone https://github.com/RadeonOpenCompute/MLSEQA_TestRepo.git")
                os.system("cp MLSEQA_TestRepo/ROCM_Tools/rocprofiler/test_distributed.py /pytorch/test/")                
                os.system("%s"%command)
    except:
        print("error in sys_trace_validation")



def systrace_printresult(output_path,fileprof):
    try:
       #x = PrettyTable()
       #x.field_names = ["OCL Components","TotalTests","TotalPass","TotalFail"]
       print(output_path) 
       inputdir = []
       print("Hi1")

       for (path, dirs, files) in os.walk(output_path):
           print("Hi2")
           print(dirs)
           inputdir.append(dirs)
       hsatrace_file = output_path + "/" + inputdir[0][0] + "/" + inputdir[1][0] + fileprof 
       print("Hi3")
       print(hsatrace_file)
       num_lines = 0
       with open(hsatrace_file, "r") as f:           
           for line in f:
               num_lines += 1
       if num_lines > 1:
          print("Pass")
          return "Pass"
       else:
          print("Fail")
          return "Fail"
    except:
       print("error in systrace_printresult")

       
	




#clear_outputpath()
#sys_trace_validation()
#systrace_printresult()
#validate_file()
#hcc_invalid_timemarking()
test_rocprof_DDP_multigpu()
