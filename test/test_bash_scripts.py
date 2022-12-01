import pytest
import sys
sys.path.append("..")
import bash_scripts_exec as script


import os
#start HDFS
os.system("sudo bash ./bash_scripts/start_hdfs.sh")

@pytest.fixture(autouse=True)
def clear_hdfs_dir():
    #creating and clear test directory
    os.system("sudo bash ./bash_scripts/mk_dir.sh /test")
    os.system("sudo bash ./bash_scripts/mk_dir.sh /test/test")
    os.system("sudo bash ./bash_scripts/clear_dir.sh /test/test")


@pytest.mark.parametrize("path, result", [("/test/test", []),
                                          ("/test", ["/test/test"]),
                                          ("/test/testtt", None),
                                          ("", None)
                                         ])
def test_ls_dir(path, result):
    report, script_result = script.ls_dir(path)
    if result is None:
        assert script_result is result
    else:
        script_result = script_result["files"] + script_result["folders"]
        assert (set(script_result) & set(result)) == set(result)


@pytest.mark.parametrize("path, file, result", [("/test/test", "1.txt", ["/test/test/1.txt"]),
                                                ("/test", "1.txt", ["/test/test", "/test/1.txt"])
                                                ])
def test_ls_dir2(path, file, result):
    os.system(f"touch ./test/{file}; echo 1234 > ./test/{file}")
    os.system(f"sudo bash ./bash_scripts/put_file.sh ./test/{file} {path}")
    report, script_result = script.ls_dir(path)
    if result is None:
        assert script_result is result
    else:
        script_result = script_result["files"] + script_result["folders"]
        assert (set(script_result) & set(result)) == set(result)


@pytest.mark.parametrize("path, dirname, result_ls, exit_status", [("/test/test", "test", ["/test/test/test"], True),
                                                ("/test/test", "test2", ["/test/test/test2"], True),
                                                ("/test/../test/tor", "test3", None, False)
                                                ])
def test_mk_dir(path, dirname, result_ls, exit_status):
    report, result = script.mk_dir(f"{path}/{dirname}")
    print("report:", report)
    assert  not script.mk_dir(f"{path}/{dirname}")[1]
    assert exit_status == result
    a, script_result = script.ls_dir(path)
    report += a
    if result_ls is None:
        assert script_result is result_ls
    else:
        script_result = script_result["files"] + script_result["folders"]
        assert (set(script_result) & set(result_ls)) == set(result_ls)




        
def test_clear_dir():
    os.system(f"touch ./test/1.txt; echo 1234 > ./test/1.txt")
    os.system(f"sudo bash ./bash_scripts/put_file.sh ./test/1.txt /test/test")
    
    report, script_result = script.ls_dir("/test/test")
    assert script_result["files"] == ["/test/test/1.txt"]
    
    assert script.clear_dir("/test/test")[1]
    
    report, script_result = script.ls_dir("/test/test")
    assert script_result["files"] == []
    
    assert not script.clear_dir("/test/test/smth")[1]


def test_del_dir():
    os.system(f"touch ./test/1.txt; echo 1234 > ./test/1.txt")
    os.system(f"sudo bash ./bash_scripts/put_file.sh ./test/1.txt /test/test")
    
    report, script_result = script.ls_dir("/test/test")
    assert script_result["files"] == ["/test/test/1.txt"], report
    
    report, script_result = script.del_dir("/test/test/1.txt")
    assert script_result, report
    
    report, script_result = script.ls_dir("/test/test")
    assert script_result["files"] == [], report
    
    report, script_result = script.mk_dir("/test/test/test")
    assert script_result, report 

    report, script_result = script.ls_dir("/test/test")
    assert "/test/test/test" in script_result["folders"] , report
    
    report, script_result = script.del_dir("/test/test/test")
    assert script_result, report 
    
    report, script_result = script.ls_dir("/test/test")
    assert len(script_result["files"]) == 0, report
    
    report, script_result = script.del_dir("/test/test/test/")
    assert not script_result, report
    

def test_get_put():
    os.system(f"touch ./test/1.txt; echo 1234 > ./test/1.txt")
    os.system(f"sudo bash ./bash_scripts/put_file.sh ./test/1.txt /test/test")
    with open("./test/1.txt", "rb") as f:
        data = f.read()
    report, script_result = script.put_file(data, "1.txt", "/test/test")
    assert script_result, report
 
    report, script_result = script.put_file(data, "1.txt", "/test/test/smth")
    assert not script_result, report
 
    
    report, script_result = script.test_file_dir("/test/test/1.txt")
    assert script_result, report

    report, script_result = script.get_file("/test/test/1.txt")
    assert script_result, report
    assert script_result == data
    assert not os.access("/tmp/djarvis_temp_files/1.txt", os.F_OK)
    
    
