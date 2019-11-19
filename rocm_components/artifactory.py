


def Artifactory():
    '''
    This fuction stor the test logs and summary table in artifactory with name of jenkins build.
    :return: it return nothing.
    '''

    artifactory_path = "http://10.130.166.180:8081/artifactory/qa_local_logpath/gromacs"
    try:
        artifactory_path = artifactory_path + os.environ['BUILD_ID']
    except KeyError:
        currentDT = datetime.now()
        artifactory_path=artifactory_path+currentDT.strftime("%Y-%m-%d_%H:%M")

    finally:
        path = ArtifactoryPath(artifactory_path,auth=('rocmqa','AH64_uh1'))
    path.mkdir()
    List=os.listdir(mail_dir)
    for i in List:
        if i.endswith('.html'):
            continue
        path.deploy_file(mail_dir+'/'+i)
    print ("Succesfully Uploaded in to http://10.130.166.180:8081/artifactory/qa_local_logpath/gromacs")
