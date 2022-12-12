file = input("file:")
result = ""
with open(file, 'r') as f:
    print("\n".join(map(lambda x: x.replace('def ', ""), filter(lambda x: "def" in x, f.readlines()))))
