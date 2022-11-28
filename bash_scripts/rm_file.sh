script_directory=$( sudo realpath $(cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.hdfs_script_directory'| tr -d \" ) )

if ! [[ -n "$1" ]]; then
	 echo "missing argument"
	 exit 
fi




if ! sudo -u hdoop $script_directory dfs -test -e $1; then echo "file not exixsts"; exit; fi



result=$(sudo -u hdoop $script_directory dfs -rm $1)

echo $result
# result = "Delitet $1" if all OK
