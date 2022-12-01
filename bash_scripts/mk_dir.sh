script_directory=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.hdfs_script_directory'| tr -d \" ) )

if ! [[ -n "$1" ]]; then
	 echo "missing argument"
	 exit 
fi


if ! sudo -u hdoop $script_directory dfs -test -e $(dirname $1); then echo "parant directory not exists"; exit; fi

if sudo -u hdoop $script_directory dfs -test -d $1; then echo "directory exixsts"; exit; fi



result=$(sudo -u hdoop $script_directory dfs -mkdir $1)

echo ${result}
# result = "" if all OK
