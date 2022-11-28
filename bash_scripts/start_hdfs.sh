start_hdfs_script=$( sudo cat /home/koly/djarvis_project/bash_scripts/config_file.json | jq '.start_hdfs' | tr -d \" )

sudo -u hdoop $start_hdfs_script

