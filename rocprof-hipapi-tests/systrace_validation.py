import os, json, sys, re, itertools, subprocess

HOME = os.environ['HOME']
command = "HIP_VISIBLE_DEVICES=0,1,2,3 WORLD_SIZE=4 TEMP_DIR=/tmp BACKEND=nccl /opt/rocm/bin/rocprof -d $PWD/rocprof_pyt_sys_trace_mgpu_test_case_1 --sys-trace python3.6 $PWD/pytorch/test/test_distributed.py --verbose TestDistBackend.test_all_gather_multigpu"
output_path = "/rocprof_pyt_sys_trace_mgpu_test_case_1"

def clear_outputpath():
    if os.path.exists(output_path):
        os.system("sudo rm -r %s"%output_path)
   
        

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

def systrace_printresult():
    try:
       #x = PrettyTable()
       #x.field_names = ["OCL Components","TotalTests","TotalPass","TotalFail"]
       print(output_path) 
       inputdir = []
       for (path, dirs, files) in os.walk(output_path):
           print(dirs)
           inputdir.append(dirs)
       hsatrace_file = output_path + "/" + inputdir[0][0] + "/" + inputdir[1][0] + "/hsa_api_trace.txt" 
       print(hsatrace_file)
       num_lines = 0
       with open(hsatrace_file, "r") as f:
           print("hsatrace_file")
           for line in f:
               num_lines += 1
       if num_lines > 1:
          print("Pass")
       else:
          print("Fail")
    except:
       print("error in systrace_printresult")
   

clear_outputpath()
sys_trace_validation()
systrace_printresult()
