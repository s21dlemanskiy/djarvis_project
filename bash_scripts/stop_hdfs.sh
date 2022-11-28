stop_hdfs_script=$( sudo cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.stop_hdfs' | tr -d \" )

sudo -u hdoop bash $stop_hdfs_script

