import subprocess as sp
from os.path import normpath
from typing import Tuple, List, Dict
import re
import json
import os


def get_vars():
    with open("/home/koly/djarvis_project/bash_scripts/config_file.json", 'r') as f:
        data = json.load(f)
    return (data["dir_temp_hdoop"], data["hdfs_script_directory"], data["start_hdfs"], data["stop_hdfs"])

#показывает содержание папки(полные пути до всего содержимого но не рекурсивно)
def ls_dir(path:str) -> Tuple[str, None|Dict[str, None|List[str]]]:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    result = sp.check_output(f"sudo bash ./bash_scripts/ls_dir.sh {path}", shell=True)
    if result == b"folder not exixsts\n":
        report += "[Errore...]folder not exixsts\n"
        return [report, None]
    elif result == b"missing argument\n":
        report += "[Errore...]empty folder argument\n"
        return [report, None]
    else:
        report += "[+]ls done secsesfull\n"
        reg = r"[\w|\-]+ - hdoop \w+ \d+ \d{4}-\d{2}-\d{2} [\w|\:]+ [\w+|\/]+"
        folders = re.findall(reg, str(result))
        folders = list(map(lambda x: x.split()[-1], folders)) 
        reg = r"[\w|\-]+ \d+ hdoop \w+ \d+ \d{4}-\d{2}-\d{2} [\w|\:]+ [\w+|\/|\.]+"
        files = re.findall(reg, str(result))
        files = list(map(lambda x: x.split()[-1], files))
        return [report, {"folders": folders, "files": files}]


def mk_dir(path: str) -> Tuple[str, bool]:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    result = sp.check_output(f"sudo bash ./bash_scripts/mk_dir.sh {path}", shell=True)
    if result == b"directory exixsts\n":
        report += "[Errore...]directory exixsts\n"
        return [report, False]
    elif result == b"missing argument\n":
        report += "[Errore...]empty folder argument\n"
        return [report, False]
    elif result == b"\n":
        report += "directory secsessfull created"
        return [report, True]
    else:
        report += "[Errore...]"
        report += str(result)
        return [report, False]



# удаляет все содержимое сохроняя саму папку(стоит учесть что rm выдает ошибку когда папрка пуста и в репорте она будет обозначена как ошибка)
def clear_dir(path: str) -> Tuple[str, bool]:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    result = sp.check_output(f"sudo bash ./bash_scripts/clear_dir.sh {path}", shell=True)
    if result == b"file not exixsts\n":
        report += "[Errore...] file not exixsts\n"
        return [report, False]
    elif result == b"missing argument\n":
        report += "[Errore...]empty folder argument\n"
        return [report, False]
    elif b"Deleted" in result:
        report += str(result)
        return [report, True]
    else:
        report += "[Errore]"
        report += str(result)
        return [report, False]



#удаляет дерикторию и все ее содержание
def del_dir(path: str) -> Tuple[str, bool]:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    result = sp.check_output(f"sudo bash ./bash_scripts/rmr_dir.sh {path}", shell=True)
    if result == b"file not exixsts\n":
        report += "[Errore...] file not exixsts\n"
        return [report, False]
    elif result == b"missing argument\n":
        report += "[Errore...]empty folder argument\n"
        return [report, False]
    elif b"Deleted" in result:
        report += str(result)
        return [report, True]
    else:
        report += "[Errore]"
        report += str(result)
        return [report, False]




def put_file(file:bytes, name: str, target_dir:str) -> Tuple[str, bool]:
    report = ""
    dir_temp_hdoop, _, _, _ = get_vars()
    if os.access(f"{dir_temp_hdoop}/{name}", os.F_OK):
        report += f"[Errore...] file exist in temp directory {dir_temp_hdoop}/{name}"
        return [report, False]
    else:
        with open(f"{dir_temp_hdoop}/{name}", "wb") as f:
            f.write(file)
            report += f"[+] data writed in {dir_temp_hdoop}/{name}"
    result = sp.check_output(f"sudo bash ./bash_scripts/put_file.sh {dir_temp_hdoop}/{name} {target_dir}", shell=True)
    if result == b"":
        report += f"[+]secsesfully aded file in {dir_temp_hdoop}/{name}"
        return [report, True]
    else:
        report += "[Errore...] " + str(result)
        return [report, False]



def test_file_dir(path:str) -> Tuple[str, bool]:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    test = sp.check_output(f"sudo bash ./bash_scripts/test_dir_file.sh {path}", shell=True)
    if test == b"not exist\n":
        report += f"directory {path} not exist\n"
        return [report, False]
    elif test == b"exist\n":
        report += f"all ok dir {path} exists\n"
        return [report, True]
    else:
        report += f"unexpected answer from bash script:{test}\n"
        return [report, False]

def get_file(path: str) -> Tuple[str, None | bytes]:
    report = ""
    test_report, result = test_file_dir(path)
    if result:
        report += "[+]" + test_report
    else:
        report += "[Errore...]" + test_report
        return [report, None]
    result = sp.check_output(f"sudo bash ./bash_scripts/get_file.sh {path}", shell=True)
    if result == b"incorect file path(file not in hdfs)\n":
        report += f"incorect file path:(file {path} not in hdfs)\n"
        return [report, None]
    elif normpath(result.decode("utf-8").strip('\n')) == result.decode("utf-8").strip('\n'):
        result = result.decode("utf-8").strip('\n')
        with open(result, "br") as f:
            report += f"[+] copying file {result}"
            file = f.read()
        try:
            os.system(f"sudo rm {result}")
        except Exception as e:
            report += f"can't remove file{result} due {e}\n"
        return [report, file]
    else:
        report += f"[Errore] unexpected errore{result}"
        return [report, None]



#with open("add_user.py", "br") as f:
#    data1 = f.read()
#print(repr(put_file(data1, "test_file.py", "/test")))



