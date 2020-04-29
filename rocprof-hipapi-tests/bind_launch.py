import sys
import subprocess
import os
import socket
from argparse import ArgumentParser, REMAINDER
current_env = "eth0"

def main():
    processes = []

    for local_rank in range(0, 2):
        #rocprof_cmd='rocprof -d rocoutmgpu%d '%(local_rank)
        #rocprof_cmd='/opt/rocm/bin/rocprof --hip-trace --roctx-trace --timestamp on --obj-tracking on -d rocprof_bind_test_case_%d -o rocprof_bind_test_case_%d/rocprof_pyt_test_case_%d.csv '%(local_rank,local_rank,local_rank)
        cmd = 'python3.6 micro_benchmarking_pytorch.py --network resnet50 --batch-size 128  --distributed_dataparallel --dist-url="tcp://127.0.0.1:54321"  --device_ids %d --rank %d --dist-backend nccl --world-size 2'%(local_rank,local_rank)
        import shlex
        args = shlex.split(cmd)
        print("Binding:", args)
        process = subprocess.Popen(args)
        processes.append(process)

    for process in processes:
        process.wait()

if __name__ == "__main__":
    main()
