import client 
import os
import  bash_scripts_exec as hdfs
client.set_up()
os.system(f'touch ./test/1.txt; echo "test data" > ./test/1.txt')
client.autarisation("test", "test")
a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
rep, ls_list = hdfs.ls_dir("/test/test")
print(rep)
client.autarisation("test", "test")
a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
rep, ls_list = hdfs.ls_dir("/test/test")
print(rep)
client.send(client.DISCONNECT_MESSAGE.encode(client.FORMAT))
