import os, sys, re, itertools, subprocess, shutil, fileinput


if len(sys.argv) != 2:
    print("Please make sure you have entered ROCmValidationSuite path (e.g. /home/taccuser/ROCmValidationSuite/")
    sys.exit(1)


HOME = os.environ['HOME']
conf_path = sys.argv[1] + "rvs/conf/"
conf_files = ['gst_1.conf','gst_2.conf','gst_3.conf','gst_4.conf','gst_5.conf','gst_6.conf','gst_7.conf','gpup_1.conf','gpup_2.conf','gpup_3.conf','gpup_4.conf','gpup_5.conf','gpup_6.conf','gpup_7.conf','gm_1.conf','gm_2.conf','gm_3.conf']
regexp = r'^  device:.*$'


def rvs_change_device_ids():
    for files in conf_files:
        with open(conf_path + files, "r") as file:            
            for line in file:
                #print(line)
                for match in re.finditer(regexp, line, re.S):
                    if "all" not in match.group():
                        print(match.group().strip().split(" ")[1])
                        rvs_edit_conffile(conf_path + files,match.group().strip().split(":")[1]," all")


def rvs_edit_conffile(filename,oldvalue,newvalue):
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(oldvalue, newvalue), end='')
            


rvs_change_device_ids()
