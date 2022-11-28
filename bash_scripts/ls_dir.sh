script_directory=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.hdfs_script_directory'| tr -d \" ) )

if ! [[ -n "$1" ]]; then
	 echo "missing argument"
	 exit 
fi

if ! sudo -u hdoop $script_directory dfs -test -d $1; then echo "folder not exixsts"; exit; fi



result=$(sudo -u hdoop $script_directory dfs -ls $1)

echo $result
