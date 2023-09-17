#!/bin/bash

# install.sh: install the dog.py tools

TEMP=$(mktemp)
SVC_DIR="/etc/systemd/system/"
DOG_SVC="kdlp-dog.service"

echo "===[KDLP ORBIT: install.sh script for dog.py repository]==="

echo "[1] Installing ${DOG_SVC}"

if stat "${SVC_DIR}/${DOG_SVC}" > /dev/null; then
	echo "| - found installed kdlp-dog.service"

	if ! diff -up "${DOG_SVC}" "${SVC_DIR}/${DOG_SVC}" > ${TEMP}; then
		echo "| - update installed service file from repository"
		echo -e "\t--- begin raw patch ---"
		cat "${TEMP}"
		echo -e "\t---- end raw patch ----"
	else
		echo "| - installed file matches repository version"
	fi

fi

# the conditionals are just for making some nice output, either way we are just going to force overwrite the service file and restart it
cp -f "${DOG_SVC}" "${SVC_DIR}/${DOG_SVC}"
echo "| - ${SVC_DIR}/${DOG_SVC} up-to-date"

systemctl daemon-reload
systemctl restart kdlp-dog


if systemctl --quiet is-active ${DOG_SVC}; then
	echo "| - ${DOG_SVC} (re)started succesfully "
else
	echo ">>>ERROR: failed to (re)start ${DOG_SVC}<<<"
	exit 1
fi

echo "==================[install.sh finished]===================="
