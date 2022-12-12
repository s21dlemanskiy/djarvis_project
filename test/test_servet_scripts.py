import pytest
import sys
sys.path.append("..")
import socket_djarvis_server as script


import os
#start HDFS
os.system("sudo bash ./bash_scripts/start_hdfs.sh")

@pytest.fixture(autouse=True)
def clear_hdfs_dir():
    #creating and clear test directory
    os.system("sudo bash ./bash_scripts/mk_dir.sh /test")
    os.system("sudo bash ./bash_scripts/mk_dir.sh /test/test")
    os.system("sudo bash ./bash_scripts/clear_dir.sh /test/test")



def test_put():
    os.system(f"touch ./test/1.txt; echo 1234 > ./test/1.txt")
    os.system(f"sudo bash ./bash_scripts/put_file.sh ./test/1.txt /test/test")
    with open("./test/1.txt", "rb") as f:
        data = f.read()
    
    
    
