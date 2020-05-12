import os, sys, re, itertools, subprocess, shutil, json, logging
HOME = os.environ['HOME']


def install_gRPC_protoc_protocplugin():
    try:
        grpc = HOME + "/grpc"
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
    except:
        print("error in install_rdc()")




#install_gRPC_protoc_protocplugin()
install_rdc()
