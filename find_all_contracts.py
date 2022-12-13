import os
import re
from termcolor import cprint
for file in filter(lambda x: re.match(r"^\w+\.py", x), os.listdir()):
    with open(file, 'r') as f:
        cprint("---->>>> file:" + file, "red")
        print("\n".join(map(lambda x: x.replace('def ', ""), filter(lambda x: "def" in x, f.readlines()))))
