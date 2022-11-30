#загружаем переменые из конфигурационного файла

dir_temp_hdoop=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.dir_temp_hdoop' | tr -d \" ) )
hdfs_script_directory=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.hdfs_script_directory'| tr -d \" ) )


# проверяем есть ли папка для временного хранения файла если нет то будем закидывать в папку test

if ! sudo test -d "${dir_temp_hdoop}"; then
	sudo mkdir $dir_temp_hdoop
fi





#проверяем что все конфиругационные переменные правильные и существуют

if ! sudo test -f "${hdfs_script_directory}" ;  then
	echo "some errore caused by mistake in config.json file or you may run not sudo(try: sudo bash ..."
	exit
fi



# проверяем что аргумент действительно введен и что он коректен

if ! [ -n "$1" ]; then
	echo "missing patametr(filenmae)"
	exit
fi


#созвем переменую для хранения пути по которому д=лежит файл или деректоии для загрузки в hdfs

PATH=$(sudo realpath $1)

if ( ! sudo -u hdoop $script_directory dfs -test -d $PATH ) && ( ! sudo -u hdoop $script_directory dfs -test -e $PATH ); then
	echo "incorect file path(file not in hdfs)"
	exit
fi

#так же создаем переменую названия файла что бы назвать файл в hdfs так же
filename=$(basename ${PATH})

# даем всем доступ на чтение и запись в файл
sudo chmod o+wr ${fullpath}
# от имени hdoop кладем файл в hdfs
sudo -u hdoop  ${hdfs_script_directory} dfs -put ${dir_temp_hdoop}/${filename} ${target_directory}/${filename}
# удаляем файл из временной дериктории
sudo rm -rf ${fullpath}
