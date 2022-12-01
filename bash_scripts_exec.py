import subprocess as sp
from os.path import normpath
from typing import Tuple, List
import re

#показывает содержание папки(полные пути до всего содержимого но не рекурсивно)
def ls_dir(path:str) -> Tuple[str, List[str]]:
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
        result = re.findall(reg, str(result))
        output = list(map(lambda x: x.split()[-1], result))
        return [report, output]


def mk_dir(path: str) -> str:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    result = sp.check_output(f"sudo bash ./bash_scripts/mk_dir.sh {path}", shell=True)
    if result == b"directory exixsts\n":
        report += "[Errore...]directory exixsts\n"
        return report
    elif result == b"missing argument\n":
        report += "[Errore...]empty folder argument\n"
        return report
    elif result == b"\n":
        return "directory secsessfull created"
    else:
        report += "[Errore]"
        report += str(result)
        return report



# удаляет все содержимое сохроняя саму папку(стоит учесть что rm выдает ошибку когда папрка пуста и в репорте она будет обозначена как ошибка)
def clear_dir(path: str) -> str:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    result = sp.check_output(f"sudo bash ./bash_scripts/clear_dir.sh {path}", shell=True)
    if result == b"file not exixsts\n":
        report += "[Errore...] file not exixsts\n"
        return report
    elif result == b"missing argument\n":
        report += "[Errore...]empty folder argument\n"
        return report
    elif b"Deleted" in result:
        report += str(result)
        return report
    else:
        report += "[Errore]"
        report += str(result)
        return report



#удаляет дерикторию и все ее содержание
def del_dir(path: str) -> str:
    report = ""
    if path != normpath(path):
        print(f"for path ware used normalizing: {path} -> {normpath(path)}")
        report += f"[Warning...] for path ware used normalizing: {path} -> {normpath(path)}\n"
        path = normpath(path)
    result = sp.check_output(f"sudo bash ./bash_scripts/rmr_dir.sh {path}", shell=True)
    if result == b"file not exixsts\n":
        report += "[Errore...] file not exixsts\n"
        return report
    elif result == b"missing argument\n":
        report += "[Errore...]empty folder argument\n"
        return report
    elif b"Deleted" in result:
        report += str(result)
        return report
    else:
        report += "[Errore]"
        report += str(result)
        return report


