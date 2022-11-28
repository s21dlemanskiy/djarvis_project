script_directory=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.hdfs_script_directory'| tr -d \" ) )

if ! [[ -n "$1" ]]; then
	echo "missing argument"
	exit
fi

if sudo -u hdoop $script_directory dfs -test -d $1  | sudo -u hdoop $script_directory dfs -test -e $1; then 
	echo "exist"
else
	echo "not exist"
fi
