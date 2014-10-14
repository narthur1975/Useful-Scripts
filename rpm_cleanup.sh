#!/bin/bash

#Read in how many builds to keep
read -p "How many previous builds do you wish to keep(Not including new one): " NUM_KEEP

case $NUM_KEEP in
''|*[!0-9]*)    
	echo "Must enter a valid number"
	exit 1 ;;
0 ) 
        echo "Cannot enter zero please choose valid number of builds to keep"
        exit 1 ;;
esac

home_dir=$PWD

#read in sudo password
echo -n "Remote sudo password: "
read -s SUDO_PASS

for dir in SecureAcceptance SecureAcceptanceListener; do
	cd $dir
	component_dir=$PWD
		for dir in app resources scripts; do
			cd $dir 
		#check number of current builds in directory
			buildsindir=$(ls -ltr | grep SecureAcceptance  | grep -v current | grep -v keystore | wc -l)
		#if there are less builds in dir than specifed to keep then skip dir and go to next one	
			if [ $NUM_KEEP -gt $buildsindir ] ; then 
					echo "Nothing to remove for: "$component_dir":"$dir
					cd $component_dir
				else
		#work out what rpms need removed then sudo yum remove them
					RPMS2DEL=$(ls -t | grep SecureAcceptance  | grep -v current | grep -v keystore | awk 'NR>v1' v1="${NUM_KEEP}" | xargs rpm -qf | grep -v "current is not owned")  
					echo $SUDO_PASS | sudo -S yum remove -y $RPMS2DEL   
					cd $component_dir
				fi
		done
	cd $home_dir
done


