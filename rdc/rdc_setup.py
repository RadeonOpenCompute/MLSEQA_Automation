import os, sys, re, itertools, subprocess, shutil, json, logging
HOME = os.environ['HOME']
#HOME = "/home/master/"
grpc = HOME + "/grpc"

#if len(sys.argv) != 2:
    #print("Please make sure you have entered HIP path, eg:/home/taccuser/HIP/")
    #sys.exit(1)


def install_gRPC_protoc_protocplugin():
    try:
        #grpc = HOME + "/grpc"
        print("entered install_gRPC_protoc_protocplugin")
        
        os.system("sudo apt-get install -y build-essential autoconf libtool pkg-config doxygen libcap-dev")
        os.system("sudo apt-get install -y libgflags-dev libgtest-dev")
        os.system("sudo apt-get install -y clang-5.0 libc++-dev curl")
        os.system("cd %s && git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc"%HOME)
        os.system("cd %s && git submodule update --init && make && sudo make install"%grpc)
        os.system("cd %s/third_party/protobuf && make && sudo make install"%grpc)
    except:
        print("error in install_gRPC_protoc_protocplugin()")


def install_rdc():
    try:
        rdc = HOME + "/rdc"
        os.system('cd %s && curl -uadmin:Admin@1234 -O "http://10.128.142.190:8081/artifactory/rdc_pkg/rdc_12.5.20.tar.gz"'%HOME)
        os.system('cd %s && tar xvzf rdc_12.5.20.tar.gz && cd %s && mkdir -p build && cd build && cmake -DROCM_DIR=/opt/rocm .. && make'%(HOME,rdc))
        os.system('cd %s && sudo LD_LIBRARY_PATH=$PWD/rdc_libs/ ./server/rdcd -u'%HOME + "/rdc/build/")
    except:
        print("error in install_rdc()")


def execute_remotely(host,user,pwd):
    try:
        import pexpect
        from pexpect import pxssh
        import getpass
        s = pxssh.pxssh()
        s.login(host, user, pwd)
        #s.sendline("sudo apt-get install -y build-essential autoconf libtool pkg-config doxygen libcap-dev")   # run a command
        #print(s.before)
        #s.sendline("sudo apt-get install -y libgflags-dev libgtest-dev")
        #print(s.before)
        #s.sendline("sudo apt-get install -y clang-5.0 libc++-dev curl")
        #print(s.before)
        s.sendline("cd %s && git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc"%HOME)
        print(s.before)
        s.sendline("cd %s && git submodule update --init && make && sudo make install"%grpc)
        print(s.before)
        s.sendline("cd %s/third_party/protobuf && make && sudo make install"%grpc)
        s.prompt()             # match the prompt
        print(s.before)        # print everything before the prompt.
        #s.logout()
        #return s.before
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)


#execute_remotely(sys.argv[1],"master","AH64_uh1")
install_gRPC_protoc_protocplugin()
install_rdc()
