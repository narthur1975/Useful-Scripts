#!/bin/sh

sudo cp /etc/sudoers /tmp/sudoers.tmp


grep -qi nagios /tmp/sudoers.tmp || echo 'nagios does not exist in sudo file'
grep -qi nagios /tmp/sudoers.tmp && echo 'nagios does exist in sudo file'

grep -qi nagios /tmp/sudoers.tmp || echo 'nagios ALL=(ALL) NOPASSWD:/usr/lib64/nagios/plugins/check_hosts.sh' >> /tmp/sudoers.tmp

grep -qi nagios /tmp/sudoers.tmp && echo 'nagios has either been added or already existed in sudo file'



sudo /usr/sbin/visudo -c -f /tmp/sudoers.tmp

if [[ $? == 0 ]] ;
    then echo "success"	
    sudo cp /tmp/sudoers.tmp /etc/sudoers
	if [[ $? == 0 ]] ;
          then echo "sudoers file copied successfully"
	  else echo "sudoers file not copied"
	fi
else
    echo "fail"
fi


sudo rm /tmp/sudoers.tmp
