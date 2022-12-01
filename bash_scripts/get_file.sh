#загружаем переменые из конфигурационного файла

dir_temp_hdoop=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.dir_temp_hdoop' | tr -d \" ) )
script_directory=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.hdfs_script_directory'| tr -d \" ) )


# проверяем есть ли папка для временного хранения файла если нет то будем закидывать в папку test

if ! sudo test -d "${dir_temp_hdoop}"; then
	sudo mkdir $dir_temp_hdoop
	sudo chmod o+wr $dir_temp_hdoop
fi





#проверяем что все конфиругационные переменные правильные и существуют

if ! sudo test -f "${script_directory}" ;  then
	echo "some errore caused by mistake in config.json file or you may run not sudo(try: sudo bash ..."
	exit
fi



# проверяем что аргумент действительно введен и что он коректен

if ! [ -n "$1" ]; then
	echo "missing patametr(filenmae)"
	exit
fi


#созвем переменую для хранения пути по которому д=лежит файл или деректоии для загрузки в hdfs

file_path=$1

if ! sudo -u hdoop $script_directory dfs -test -d $file_path  | sudo -u hdoop $script_directory dfs -test -e $file_path; then
	echo "incorect file path(file not in hdfs)"
	exit
fi

#так же создаем переменую названия файла что бы назвать файл в hdfs так же
filename=$(basename ${file_path})

#sudo touch ${dir_temp_hdoop}/${filename}
#sudo chmod o+wr ${dir_temp_hdoop}/${filename}
# от имени hdoop кладем файл в hdfs
sudo -u hdoop  ${script_directory} dfs -get -f $file_path ${dir_temp_hdoop}/${filename}
# даем всем доступ на чтение и запись в файл
#sudo mv /home/hdoop/temp/${filename} ${dir_temp_hdoop}/${filename}
sudo chmod o+wr ${dir_temp_hdoop}/${filename}
echo ${dir_temp_hdoop}/${filename}
