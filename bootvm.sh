#!bin/bash

timecount = 300

# start VMs
echo ""
echo -e "BOOT UP VMs"
for vm in ${vms[@]}; do
	echo -e "booting up $vm"
	virsh start $vm
done

# wait untill all VMs are up running
echo -e "\n   checking VM state :\n"
_vms=( ${vms[@]} )
vmss=()
n=0
for (( i=0; i<timecount; i++ )); do
	echo -n "."
	for vm in ${_vms[@]}; do
		ping -c 1 -W 1 ${vm} >/dev/null 2>&1
		if [ $? = 0 ]; then
               		echo -e "\n   VM $vm is ready\n"
		else
			vmss[$n]=$vm
			(( n=$n+1 ))
		fi
	done

	# check all up ruuning
	[ $n = 0 ] && echo -e "\nVMs all up running\n" && break
	
	# rearrange vm list
	_vms=()
	_vms=( "${vmss[@]}" )
	vmss=()
	n=0

	sleep 1
done
