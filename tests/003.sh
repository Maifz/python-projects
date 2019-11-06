#!/usr/bin/env bash

set -e
set -u
set -o pipefail

SCRIPTPATH="$( cd "$(dirname "${0}")" && pwd -P )"

EXCERCISE="003"
FILENAME="tree.py"

# -------------------------------------------------------------------------------------------------
# FUNCTIONS
# -------------------------------------------------------------------------------------------------

create_dirs() {
	local prefix
	prefix="$( mktemp -d )"
	mkdir -p "${prefix}/001/cytopia/aaa"
	mkdir -p "${prefix}/001/cytopia/.aaa"
	mkdir -p "${prefix}/001/001"
	mkdir -p "${prefix}/001/002"
	mkdir -p "${prefix}/001/_001"
	mkdir -p "${prefix}/001/.001"
	mkdir -p "${prefix}/001/.0.01"
	mkdir -p "${prefix}/001/.0.02"
	mkdir -p "${prefix}/001/_002"
	mkdir -p "${prefix}/001/.002"
	mkdir -p "${prefix}/001/.cytopia/aaa"
	mkdir -p "${prefix}/001/.cytopia/_mmm"
	mkdir -p "${prefix}/001/.cytopia/.zzz"
	mkdir -p "${prefix}/001/.maifz/bbb"
	mkdir -p "${prefix}/001/.maifz/_nnn"
	mkdir -p "${prefix}/001/.maifz/.xxx"
	mkdir -p "${prefix}/.002/cytopia"
	mkdir -p "${prefix}/.002/cytopia1"
	mkdir -p "${prefix}/.002/cytopia_"
	mkdir -p "${prefix}/.002/maifz/"
	mkdir -p "${prefix}/.002/_/"
	mkdir -p "${prefix}/.002/anabel/"
	mkdir -p "${prefix}/.002/_anabel/"
	mkdir -p "${prefix}/.002/__albert/"
	mkdir -p "${prefix}/.002/-/"
	mkdir -p "${prefix}/.002/test/"
	mkdir -p "${prefix}/.002/_test/"
	mkdir -p "${prefix}/.002/-test/"
	mkdir -p "${prefix}/.002/-+test/"
	mkdir -p "${prefix}/.002/--test/"
	mkdir -p "${prefix}/.002/-good/"
	mkdir -p "${prefix}/.002/--good/"
	mkdir -p "${prefix}/.002/--aha/"
	mkdir -p "${prefix}/.002/+/"
	mkdir -p "${prefix}/.002/helo/"
	mkdir -p "${prefix}/.002/+helo/"
	mkdir -p "${prefix}/.002/_helo/"
	mkdir -p "${prefix}/.002/-helo/"
	mkdir -p "${prefix}/.002/+zulu/"
	mkdir -p "${prefix}/.002/++zulu/"
	mkdir -p "${prefix}/.002/+-zulu/"

	seq 101   > "${prefix}/001/.cytopia/netcat.py"
	seq 102   > "${prefix}/001/.cytopia/.netcat.py"
	seq 102   > "${prefix}/001/.cytopia/_netcat.py"
	seq 103   > "${prefix}/001/.cytopia/_netcat.py1"
	seq 104   > "${prefix}/001/.cytopia/_netcat.py_"
	seq 105   > "${prefix}/001/.cytopia/__netcat.py"
	seq 106   > "${prefix}/001/.cytopia/__netcat.py"
	seq 107   > "${prefix}/001/.cytopia/_+netcat.py"
	seq 109   > "${prefix}/001/.cytopia/-+netcat.py"
	seq 118   > "${prefix}/001/.cytopia/+netcat.py"
	seq 112   > "${prefix}/001/.cytopia/+-netcat.py"
	seq 120   > "${prefix}/001/.cytopia/+_netcat.py"
	seq 1000  > "${prefix}/001/.cytopia/aaa/helper.py"
	seq 10000 > "${prefix}/001/.cytopia/aaa/args.py"
	seq 1000  > "${prefix}/001/.cytopia/.zzz/helper.py"
	seq 10000 > "${prefix}/001/.cytopia/.zzz/args.py"

	seq 100   > "${prefix}/001/.maifz/netcat.py"
	seq 150   > "${prefix}/001/.maifz/bbb/helper.py"
	seq 1510  > "${prefix}/001/.maifz/bbb/args.py"
	seq 1310  > "${prefix}/001/.maifz/.xxx/helper.py"
	seq 10    > "${prefix}/001/.maifz/.xxx/args.py"

	seq 1230 > "${prefix}/.002/cytopia/httpd.py"
	seq 120  > "${prefix}/.002/cytopia/.hidden"
	seq 107  > "${prefix}/.002/maifz/httpd.py"
	seq 1    > "${prefix}/.002/maifz/.hidden"

	# Return $prefix
	echo "${prefix}"
}


# -------------------------------------------------------------------------------------------------
# ENTRYPOINT
# -------------------------------------------------------------------------------------------------

if [ "${#}" -ne "1" ]; then
	echo "Error, required 1 argument (cytopia or maifz)"
	exit 1
fi

ABS_PATH="${SCRIPTPATH}/../${EXCERCISE}/${1}/${FILENAME}"
if [ ! -f "${ABS_PATH}" ]; then
	echo "Tree not available: '${ABS_PATH}'"
	exit 0
fi


CHANGES=0
PLAYGROUND="$( create_dirs )"

echo "#------------------------------------------------------------------------------------------"
echo "# tree ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree "${PLAYGROUND}") <("${ABS_PATH}" "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -h ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -h "${PLAYGROUND}") <("${ABS_PATH}" -H "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -L 2 ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -L 2 "${PLAYGROUND}") <("${ABS_PATH}" -L 2 "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -a ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -a "${PLAYGROUND}") <("${ABS_PATH}" -a "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -a -h ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -ah "${PLAYGROUND}") <("${ABS_PATH}" -aH "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -a -L 2 ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -a -L 2 "${PLAYGROUND}") <("${ABS_PATH}" -a -L 2 "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -d ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -d "${PLAYGROUND}") <("${ABS_PATH}" -d "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -d -h ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -dh "${PLAYGROUND}") <("${ABS_PATH}" -dH "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -d -L 2 ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -d -L 2 "${PLAYGROUND}") <("${ABS_PATH}" -d -L 2 "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi
echo

echo "#------------------------------------------------------------------------------------------"
echo "# tree -a -d ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -ad "${PLAYGROUND}") <("${ABS_PATH}" -ad "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi

echo "#------------------------------------------------------------------------------------------"
echo "# tree -a -d -h ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -adh "${PLAYGROUND}") <("${ABS_PATH}" -adH "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi

echo "#------------------------------------------------------------------------------------------"
echo "# tree -a -d -L 2 ${PLAYGROUND}"
echo "#------------------------------------------------------------------------------------------"
if ! diff -y <(tree -ad -L 2 "${PLAYGROUND}") <("${ABS_PATH}" -ad -L 2 "${PLAYGROUND}"); then
	CHANGES=$(( CHANGES + 1 ))
fi

exit ${CHANGES}
