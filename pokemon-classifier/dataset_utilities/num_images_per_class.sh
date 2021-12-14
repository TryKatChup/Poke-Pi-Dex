#!/bin/bash

if [[ $# -ne 3 || ! -d "$1" ]]
then
	echo "Usage: $0 <old_dir> <new_dir> <N>"
	exit 0
fi

(test -d "$2") || (mkdir "$2")

old_dir="$1"
new_dir="$2"

old_name=""
i=0
for f in $(find "${old_dir}" -type f -name "*")
do
	
	current_pkmn_name=$(echo "${f}" | cut -d '/' -f 2)
	
	if [ "${old_name}" != "${current_pkmn_name}" ]
	then
		mkdir "${new_dir}/${current_pkmn_name}"
		old_name="${current_pkmn_name}"
		i=1
	fi
	
	filename="${f##*/}"
	
	if [[ $i -le $3 ]]
	then
		echo "$f"
		cp "./${f}" "./${new_dir}/${current_pkmn_name}/${filename}"
	fi
	
	i=$(expr $i + 1)
done
