#загружаем переменые из конфигурационного файла

dir_temp_hdoop=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.dir_temp_hdoop' | tr -d \" ) )
hdfs_script_directory=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.hdfs_script_directory'| tr -d \" ) )


# проверяем есть ли папка назначения в hdfs если нет то будем закидывать в папку test

if ! sudo test -d "${dir_temp_hdoop}"; then
	sudo mkdir $dir_temp_hdoop
	sudo chmod o+wr $dir_temp_hdoop
fi




if [ -n "$2" ]; then
	if ! sudo -u hdoop  ${hdfs_script_directory} dfs -test -e $2; then
		echo "target directory not exists";
		exit
	fi
	target_directory=$2
else
	target_directory="/test"
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

fullpath=$(sudo realpath $1)

if [ ! -f "${fullpath}" ] && [! -d "${fullpath}"]; then
	echo "incorect local path(filename to put in hdfs)"
	exit
fi

#так же создаем переменую названия файла что бы назвать файл в hdfs так же
filename=$(basename ${fullpath})

# проверяем лижит ли файл уже в общей  временной дериктории для hdoop и koly (лежит ли файл внутри tmp/djarvis_temp_files/)
# если нет то перебрасываем его туда
if ! [[ "${fullpath}" =~ "$dir_temp_hdoop".* ]]; then
	sudo cp -r ${fullpath} $dir_temp_hdoop/${filename}
	fullpath="${dir_temp_hdoop}/${filename}"
fi

# даем всем доступ на чтение и запись в файл
sudo chmod o+wr ${fullpath}
# от имени hdoop кладем файл в hdfs
sudo -u hdoop  ${hdfs_script_directory} dfs -put ${dir_temp_hdoop}/${filename} ${target_directory}/${filename}
# удаляем файл из временной дериктории
sudo rm -rf ${fullpath}
