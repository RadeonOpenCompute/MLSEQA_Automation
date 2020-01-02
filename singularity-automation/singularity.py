import os, sys, re, itertools, subprocess, docker, tempfile, shutil
from subprocess import PIPE, run, call
HOME = os.environ['HOME']
dockerpath = HOME + "/sing-dockerbuild"


def clean_log():    
    if os.path.isdir(dockerpath):
        shutil.rmtree(dockerpath)
    else:
        print("Can not delete the folder as it doesn't exists")


def get_rocmdock():
    try:
        #os.system("%s%s" %(com[0],"compute-rocm-rel-3.0:6"))
        res = os.popen("sudo docker ps -a").read()
        print(res)
        for item in res.split("\n"):
            if "singularity-image" in item:
                get_rocmdock.container = re.split('\s+', item)[0]
                get_rocmdock.imageid = re.split('\s+', item)[1]
                print(get_rocmdock.container)
    except Exception as e:
        print("[-] Error running command %s" %(str(e)))



def exec_rocmdock():
    try:
        os.system("mkdir %s && cp dockerfile %s" %(dockerpath,dockerpath))
        os.system("cd %s && sudo docker build -t singularity-image ." %dockerpath)
        os.system("sudo docker run --rm -d -i -t --network=host --device=/dev/kfd --device=/dev/dri --group-add video --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --privileged singularity-image:latest /bin/bash")
        get_rocmdock()
        os.system("sudo docker restart %s" %get_rocmdock.container)
        os.system("sudo docker exec %s /bin/sh -c 'cd /home/app/rccl-tests/ && make'" %get_rocmdock.container)
        os.system("sudo docker exec %s /bin/sh -c '/home/app/rccl-tests/build/all_reduce_perf -b 8 -e 128M -f 2 -g 2 -o sum -d float'" %get_rocmdock.container)
        os.system("sudo docker commit %s %s" %(get_rocmdock.container,get_rocmdock.imageid))
        os.system("sudo docker tag singularity-image:latest rmula/docksingularity:0201")
        os.system("sudo docker push rmula/docksingularity:0201")        
        os.system("singularity pull docker://rmula/docksingularity:0201")        
    except Exception as e:
        print("[-] Error running command %s" %(str(e)))


clean_log()
exec_rocmdock()
